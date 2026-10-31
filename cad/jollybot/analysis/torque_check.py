#!/usr/bin/env python3
"""Torque and speed check for every Jolly-bot joint, using the CAD geometry in params.py.

Method
- Mass properties: printed parts from the CAD solids (PETG 1.27 g/cm³ × fill factor), foam and fur integrated as
  thin revolved surfaces, everything else as point masses (list below, each one an estimate).
- Tilt platform: exact loop closure for each pushrod (horn arm r_h, rod L, tangential horn axis), Jacobian by finite
  differences, servo torques by virtual work  tau = J^-T * Q  with  Q = dV/dq + M*qdd + drag.
- Each motion is a min-jerk profile (or sinusoid); every sample is checked against the servo's torque-speed line
  tau_avail(w) = tau_stall * (1 - |w|/w_noload) and against the Current Limit cap  tau_cap = Kt * (I_lim - I0).
- Yaw: rotating inertia about Z through the belt ratio, plus friction allowances.  Arms: lumped arm on the horn.
Numbers marked ASSUMPTION are not measured; the report lists them so the bench tests can replace them.
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import params as P

G = 9.81
RHO_PETG = 1.27e-6           # kg/mm³
SIGMA_FUR = 0.45e-6          # kg/mm²  (≈450 g/m² heavy minky / faux fur)          ASSUMPTION
SIGMA_FOAM = 0.30e-6         # kg/mm²  (10 mm of 30 kg/m³ upholstery foam)          ASSUMPTION
I0 = 0.10                    # A, servo no-load / electronics current inside the measured input current  ASSUMPTION

SERVOS = {  # e-Manual values at 5.0 V
    "XL330-M288": dict(tau_s=0.52, w_nl=103 * 2 * math.pi / 60, kt=0.354, i_s=1.47),
    "XL330-M077": dict(tau_s=0.215, w_nl=383 * 2 * math.pi / 60, kt=0.146, i_s=1.47),
}
LIMITS_MA = {"awake-idle 300 mA": 300, "awake-idle 400 mA (recommended)": 400, "motion 600 mA": 600}

# ------------------------------------------------------------------ mass model
class Body:
    def __init__(self, name, m, com, I=None, group="tilt"):
        self.name, self.m, self.com, self.group = name, m, np.array(com, float), group
        self.I = np.zeros((3, 3)) if I is None else np.array(I, float)   # kg·mm² about own CoM

def cad_body(name, shape, fill, group):
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    pr = GProp_GProps(); BRepGProp.VolumeProperties_s(shape.wrapped, pr)
    vol = pr.Mass(); c = pr.CentreOfMass(); Mi = pr.MatrixOfInertia()
    I = np.array([[Mi.Value(i, j) for j in (1, 2, 3)] for i in (1, 2, 3)]) * RHO_PETG * fill
    return Body(name, vol * RHO_PETG * fill, (c.X(), c.Y(), c.Z()), I, group)

def surface_rings(name, radius_fn, h0, h1, sigma, group, step=1.0):
    out, h, r_prev = [], h0, radius_fn(h0)
    while h < h1:
        h2 = min(h + step, h1); r2 = radius_fn(h2); r = (r_prev + r2) / 2; hm = (h + h2) / 2
        dm = sigma * 2 * math.pi * r * math.hypot(h2 - h, r2 - r_prev)
        if dm > 0:
            out.append(Body(name, dm, (0, 0, hm), np.diag([dm * r * r / 2, dm * r * r / 2, dm * r * r]), group))
        h, r_prev = h2, r2
    return out

def polar(r, az, h):
    a = math.radians(az); return (r * math.cos(a), r * math.sin(a), h)

def build_mass_model():
    from parts.head_shell import head_shell
    from parts.tilt_stack import spine_plate, carrier
    from parts.puck import puck_bowl, puck_lid
    B = []
    # --- tilting head (everything above the U-joint cross)
    B.append(cad_body("head shell (both halves, 1.6 mm walls ≈ solid)", head_shell(split=False)[0], 1.0, "tilt"))
    B.append(cad_body("spine plate (80 % effective fill)", spine_plate(), 0.8, "tilt"))
    for sx in (-1, 1):
        az = 90 - sx * P.SHOULDER_AZ_FROM_FRONT
        B.append(Body("arm servo XL330", 0.018, polar(P.shell_r(P.SHOULDER_H) - 16, az, P.SHOULDER_H), group="tilt"))
        B.append(Body("arm: horn extension + paddle + foam stub + fur  (ASSUMPTION 22 g)", 0.022,
                      polar(P.shell_r(P.SHOULDER_H) + 28, az, P.SHOULDER_H - 4), group="tilt"))
        B.append(Body("eye: cabochon + M4 screw + insert", 0.004, (sx * P.EYE_SPACING / 2, P.skin_r(P.EYE_LINE_H) - 8, P.EYE_LINE_H)))
    B.append(Body("camera board", 0.010, (-P.EYE_SPACING / 2 + 3, P.shell_r(P.EYE_LINE_H) - 15, P.EYE_LINE_H)))
    B.append(Body("MPR121 + LEDs", 0.005, (0, 0, P.HEAD_TOP_H - 16)))
    B.append(Body("head harness + JST (ASSUMPTION)", 0.015, (0, -20, P.NECK_H0 + 8)))
    B.append(Body("inserts + screws in shell", 0.016, (0, 0, 135)))
    B.append(Body("U-joint upper yoke + pin", 0.010, (0, 0, P.PIVOT_H + 6)))
    B += surface_rings("foam jacket on head", lambda h: P.shell_r(h) + 7, P.NECK_H0, P.HEAD_TOP_H + 8, SIGMA_FOAM, "tilt")
    B += surface_rings("fur skin on head", P.skin_r, P.NECK_H0, P.SKIN_H_TOP, SIGMA_FUR, "tilt")
    # skirt: carried by the neck but drapes, so it is heave load + inertia, not a rigid gravity lever
    B += surface_rings("fur skirt (drapes)", lambda h: P.skin_r(h) - 3, 33.0, P.NECK_H0, SIGMA_FUR, "skirt")
    # --- heave-only (below the cross: carrier, bushing, lower yoke)
    B.append(cad_body("carrier (80 % fill)", carrier(), 0.8, "heave"))
    B.append(Body("igus bushing + lower yoke + pin", 0.016, (0, 0, P.CARRIER_TOP_H), group="heave"))
    # --- yaw-only rotating parts (puck and contents)
    B.append(cad_body("puck bowl", puck_bowl(), 1.0, "puck"))
    B.append(cad_body("puck lid", puck_lid(), 1.0, "puck"))
    for az in P.TILT_SERVO_AZ:
        B.append(Body("tilt servo + horn arm + link", 0.024, polar(P.TILT_SERVO_R, az, 30), group="puck"))
    B.append(Body("yaw servo + pulley", 0.028, polar(P.YAW_SERVO_R, P.YAW_SERVO_AZ, 30), group="puck"))
    B.append(Body("Pi Zero 2 W + HAT + hub", 0.035, polar(42, 270, 58), np.diag([0, 0.035 * 65**2 / 12, 0.035 * 65**2 / 12]), "puck"))
    B.append(Body("OpenRB-150 / U2D2", 0.012, polar(50, 30, 56), group="puck"))
    B.append(Body("speaker", 0.020, polar(48, 62, 56), group="puck"))
    B.append(Body("two bucks + capacitor", 0.020, polar(54, 210, 22), group="puck"))
    B.append(Body("shaft + grub screw", 0.014, (0, 0, 35), group="puck"))
    B.append(Body("bearing outer race (half the bearing)", 0.020, (0, 0, 10), np.diag([0, 0, 0.020 * 29**2]), "puck"))
    B.append(Body("puck wiring (ASSUMPTION)", 0.015, polar(40, 0, 40), group="puck"))
    B += surface_rings("fur + foam sleeve on puck", lambda h: P.skin_r(h) - 4, 12.0, 82.0, SIGMA_FUR + SIGMA_FOAM, "puck")
    return B

def mass_props(bodies, about):
    m = sum(b.m for b in bodies)
    com = sum(b.m * b.com for b in bodies) / m
    I = np.zeros((3, 3)); a = np.array(about, float)
    for b in bodies:
        d = b.com - a
        I += b.I + b.m * (np.dot(d, d) * np.eye(3) - np.outer(d, d))
    return m, com, I * 1e-6   # kg, mm, kg·m²

# ------------------------------------------------------------------ tilt kinematics
AZ = [math.radians(a) for a in P.TILT_SERVO_AZ]
PIV = np.array([0, 0, P.PIVOT_H])

def rot(pitch_down_deg, roll_deg):
    tx = math.radians(-pitch_down_deg); ty = math.radians(roll_deg)
    Rx = np.array([[1, 0, 0], [0, math.cos(tx), -math.sin(tx)], [0, math.sin(tx), math.cos(tx)]])
    Ry = np.array([[math.cos(ty), 0, math.sin(ty)], [0, 1, 0], [-math.sin(ty), 0, math.cos(ty)]])
    return Rx @ Ry      # lower yoke = pitch axis, upper yoke = roll axis

def horn_angles(q):
    """q = (pitch_down deg, roll deg, heave mm) -> horn angles (rad, 0 = arm horizontal pointing inward, + = up)."""
    R = rot(q[0], q[1]); out = []
    for a in AZ:
        er = np.array([math.cos(a), math.sin(a), 0]); ez = np.array([0, 0, 1.0])
        b = np.array([P.BALL_R * math.cos(a), P.BALL_R * math.sin(a), P.PLATE_BALL_H])
        p = PIV + np.array([0, 0, q[2]]) + R @ (b - PIV)
        c = np.array([P.TILT_SERVO_R * math.cos(a), P.TILT_SERVO_R * math.sin(a), P.HORN_AXIS_H])
        d = p - c; dr, dz = d @ er, d @ ez
        K = (d @ d + P.HORN_ARM_R**2 - P.ROD_L**2) / (2 * P.HORN_ARM_R); rho = math.hypot(dr, dz)
        if abs(K / rho) > 1: return None
        out.append(math.atan2(dr, dz) + math.asin(K / rho))
    return np.array(out)

def rod_lean_deg(q):
    """Ball-link swing: a link turns freely about its stud, so the limited angle is the rod's tilt OUT of the plane
    perpendicular to the stud. Both studs are tangential (horn stud parallel to the horn axis; plate stud on a tangential
    ear). Returns (worst link swing, worst rod angle from vertical) in degrees."""
    R = rot(q[0], q[1]); phi = horn_angles(q); swing = 0; lean = 0
    for a, f in zip(AZ, phi):
        er = np.array([math.cos(a), math.sin(a), 0]); ez = np.array([0, 0, 1.0]); et = np.array([-math.sin(a), math.cos(a), 0])
        b = np.array([P.BALL_R * math.cos(a), P.BALL_R * math.sin(a), P.PLATE_BALL_H])
        p = PIV + np.array([0, 0, q[2]]) + R @ (b - PIV)
        c = np.array([P.TILT_SERVO_R * math.cos(a), P.TILT_SERVO_R * math.sin(a), P.HORN_AXIS_H])
        hb = c + P.HORN_ARM_R * (-math.cos(f) * er + math.sin(f) * ez)
        rod = (p - hb) / np.linalg.norm(p - hb)
        swing = max(swing, math.degrees(math.asin(min(1, abs(rod @ et)))), math.degrees(math.asin(min(1, abs(rod @ (R @ et))))))
        lean = max(lean, math.degrees(math.acos(min(1, abs(rod @ ez)))))
    return swing, lean

def to_si(q):        # generalized coords in SI: (rad, rad, m)
    return np.array([math.radians(q[0]), math.radians(q[1]), q[2] / 1000])

def jacobian(q, eps=(0.05, 0.05, 0.05)):
    J = np.zeros((3, 3))
    for k in range(3):
        dq = np.zeros(3); dq[k] = eps[k]
        a, b = horn_angles(q + dq), horn_angles(q - dq)
        if a is None or b is None: return None
        J[:, k] = (a - b) / (to_si(q + dq) - to_si(q - dq))[k]
    return J   # d(phi)/d(q_SI)

def potential(q, tilt, heave_m):
    R = rot(q[0], q[1]); V = 0.0
    for b in tilt:
        z = (PIV + np.array([0, 0, q[2]]) + R @ (b.com - PIV))[2]
        V += b.m * G * z / 1000
    return V + heave_m * G * q[2] / 1000

def gen_gravity(q, tilt, heave_m, eps=(0.05, 0.05, 0.05)):
    Q = np.zeros(3)
    for k in range(3):
        dq = np.zeros(3); dq[k] = eps[k]
        Q[k] = (potential(q + dq, tilt, heave_m) - potential(q - dq, tilt, heave_m)) / (to_si(q + dq) - to_si(q - dq))[k]
    return Q

def minjerk(q0, q1, T, n=60):
    q0, q1 = np.array(q0, float), np.array(q1, float)
    for i in range(n + 1):
        t = T * i / n; s = t / T
        pos = q0 + (q1 - q0) * (10 * s**3 - 15 * s**4 + 6 * s**5)
        vel = (q1 - q0) * (30 * s**2 - 60 * s**3 + 30 * s**4) / T
        acc = (q1 - q0) * (60 * s - 180 * s**2 + 120 * s**3) / T**2
        yield pos, vel, acc

def sinusoid(q_mid, amp, f, n=60):
    q_mid, amp = np.array(q_mid, float), np.array(amp, float); w = 2 * math.pi * f
    for i in range(n + 1):
        t = i / (n * f)
        yield q_mid + amp * math.sin(w * t), amp * w * math.cos(w * t), -amp * w * w * math.sin(w * t)

def check_motion(profile, tilt, heave_m, Mgen, drag, servo, lim_ma):
    S = SERVOS[servo]; cap = S["kt"] * (lim_ma / 1000 - I0)
    worst = dict(margin=1e9)
    for pos, vel, acc in profile:
        J = jacobian(pos)
        if J is None or horn_angles(pos) is None:
            return dict(unreachable=True, pose=pos.copy())
        vel_si = np.array([math.radians(vel[0]), math.radians(vel[1]), vel[2] / 1000])
        acc_si = np.array([math.radians(acc[0]), math.radians(acc[1]), acc[2] / 1000])
        Q = gen_gravity(pos, tilt, heave_m) + Mgen @ acc_si + drag * np.sign(vel_si)
        tau = np.linalg.solve(J.T, Q); w = J @ vel_si
        for i in range(3):
            avail = min(S["tau_s"] * max(0.0, 1 - abs(w[i]) / S["w_nl"]), cap)
            m = avail / abs(tau[i]) if abs(tau[i]) > 1e-9 else 1e9
            if m < worst["margin"]:
                worst = dict(margin=m, tau=abs(tau[i]), avail=avail, w_rpm=abs(w[i]) * 60 / (2 * math.pi),
                             speed_frac=abs(w[i]) / S["w_nl"], cap=cap, servo_i=i, pose=pos.copy())
    return worst

def verdict(m):
    return "PASS" if m >= 1.5 else ("MARGINAL" if m >= 1.0 else "FAIL")

# ------------------------------------------------------------------ main report
def main():
    bodies = build_mass_model()
    tilt = [b for b in bodies if b.group == "tilt"]
    skirt = [b for b in bodies if b.group == "skirt"]
    heave_only = [b for b in bodies if b.group == "heave"]
    puck = [b for b in bodies if b.group == "puck"]
    m_tilt, com_tilt, I_tilt = mass_props(tilt, PIV)
    m_skirt = sum(b.m for b in skirt); m_heave_only = sum(b.m for b in heave_only)
    heave_extra = m_skirt + m_heave_only            # moves in heave but not a rigid tilt lever
    _, _, I_skirt = mass_props(skirt, PIV)
    I_ang = (I_tilt + I_skirt)[:2, :2]
    m_heave = m_tilt + heave_extra
    Mgen = np.zeros((3, 3)); Mgen[:2, :2] = I_ang; Mgen[2, 2] = m_heave
    DRAG = np.array([0.03, 0.03, 0.5])   # N·m, N·m, N  skin/skirt drag + bushing friction   ASSUMPTION
    L = []
    w = L.append
    w("# Jolly-bot torque and speed check\n")
    w("Generated by `analysis/torque_check.py` from the geometry in `params.py`. Servo data from the Robotis e-Manual at 5.0 V. "
      "A motion passes at margin ≥ 1.5 (available torque ÷ needed torque, at the speed it is moving), is marginal at 1.0–1.5, "
      "and fails below 1.0. Available torque is the lower of the torque-speed line and the Current Limit cap, "
      f"Kt × (I_limit − {I0:.2f} A).\n")
    w("## Mass model\n")
    w("| Group | Mass | CoM height | Notes |\n|---|---|---|---|")
    w(f"| Tilting head (above the U-joint) | {m_tilt*1000:.0f} g | h {com_tilt[2]:.0f} mm ({com_tilt[2]-P.PIVOT_H:.0f} mm above the pivot at h {P.PIVOT_H:.1f}), {com_tilt[1]:+.1f} mm fore-aft | I_pitch {I_ang[0,0]*1e3:.2f} g·m², I_roll {I_ang[1,1]*1e3:.2f} g·m² about the pivot |")
    w(f"| Skirt (drapes, carried by the neck) | {m_skirt*1000:.0f} g | — | heave load and inertia only |")
    w(f"| Heave-only (carrier, bushing, lower yoke) | {m_heave_only*1000:.0f} g | — | |")
    m_puck, _, _ = mass_props(puck, (0, 0, 0))
    w(f"| Puck and contents (yaw only) | {m_puck*1000:.0f} g | — | |\n")
    w("Largest single items in the head:\n")
    agg = {}
    for b in tilt: agg[b.name] = agg.get(b.name, 0) + b.m
    for n, m in sorted(agg.items(), key=lambda kv: -kv[1])[:8]:
        w(f"- {n}: {m*1000:.0f} g")
    w("")
    # ---- workspace sweep: reachability, rod lean, static hold
    w("## Tilt platform: static hold over the whole workspace\n")
    worst_static = {k: dict(tau=0) for k in ("tau",)}
    worst = (0, None); worst_lean = (0, None); unreachable = 0; n = 0; unreach_list = []; worst_rod_lean = 0
    for pd in range(-25, 16, 1):
        for rl in range(-18, 19, 2):
            if math.degrees(math.acos(math.cos(math.radians(pd)) * math.cos(math.radians(rl)))) > 28.01: continue
            for hv in (-6, 0, 6):
                q = np.array([pd, rl, hv], float); n += 1
                J = jacobian(q)
                if horn_angles(q) is None or J is None:
                    unreachable += 1; unreach_list.append(q); continue
                tau = np.abs(np.linalg.solve(J.T, gen_gravity(q, tilt, heave_extra)))
                if tau.max() > worst[0]: worst = (tau.max(), q)
                sw, ln = rod_lean_deg(q)
                if sw > worst_lean[0]: worst_lean = (sw, q)
                worst_rod_lean = max(worst_rod_lean, ln)
    tau_neutral = np.abs(np.linalg.solve(jacobian(np.zeros(3)).T, gen_gravity(np.zeros(3), tilt, heave_extra)))
    S = SERVOS["XL330-M288"]
    w(f"- Poses checked: {n} (pitch −25…+15°, roll ±18°, combined ≤ 28°, heave −6/0/+6 mm). Out of reach: {unreachable}.")
    if unreach_list:
        hv = sorted(set(int(u[2]) for u in unreach_list)); comb = min(math.degrees(math.acos(math.cos(math.radians(u[0]))*math.cos(math.radians(u[1])))) for u in unreach_list)
        w(f"  All out-of-reach poses are at heave {hv} mm with combined tilt ≥ {comb:.0f}°: a horn would pass vertical. The engine's per-rod clamp already trades heave for tilt there.")
    w(f"- Holding torque at rest: {tau_neutral.max():.3f} N·m per servo, about {tau_neutral.max()/S['kt']*1000+I0*1000:.0f} mA each.")
    w(f"- Worst static hold: {worst[0]:.3f} N·m at pitch {worst[1][0]:+.0f}°, roll {worst[1][1]:+.0f}°, heave {worst[1][2]:+.0f} mm.")
    w(f"- Worst ball-link swing (rod tilt across the stud axis): {worst_lean[0]:.1f}° at pitch {worst_lean[1][0]:+.0f}°, roll {worst_lean[1][1]:+.0f}°, heave {worst_lean[1][2]:+.0f} mm. Links allow about ±25°: {'PASS' if worst_lean[0] <= 25 else 'FAIL'}.")
    w(f"- Worst rod angle from vertical: {worst_rod_lean:.1f}° (in the horn plane, where the link turns freely about its stud).\n")
    w("| Current limit | Torque cap | Worst static need | Margin | Verdict |\n|---|---|---|---|---|")
    for lbl, ma in LIMITS_MA.items():
        cap = S["kt"] * (ma / 1000 - I0)
        w(f"| {lbl} | {cap:.3f} N·m | {worst[0]:.3f} N·m | {cap/worst[0]:.2f} | {verdict(cap/worst[0])} |")
    w("")
    # ---- motions
    w("## Tilt platform: motions (3 × XL330-M288, 600 mA limit)\n")
    w(f"Drag allowance on every tilt motion (ASSUMPTION until the skirt-drag test): {DRAG[0]} N·m pitch, {DRAG[1]} N·m roll, {DRAG[2]} N heave.\n")
    w("| Motion | Profile | Peak servo speed | Needed | Available | Margin | Verdict |\n|---|---|---|---|---|---|---|")
    motions = [
        ("Snappy nod", "pitch −10° → +15° in 0.15 s", minjerk((-10, 0, 0), (15, 0, 0), 0.15)),
        ("Nod, relaxed", "pitch −10° → +15° in 0.25 s", minjerk((-10, 0, 0), (15, 0, 0), 0.25)),
        ("Look up at a seated face", "pitch 0 → −25° in 0.25 s", minjerk((0, 0, 0), (-25, 0, 0), 0.25)),
        ("Head-cock", "roll 0 → 16°, pitch 0 → −4° in 0.25 s", minjerk((0, 0, 0), (-4, 16, 0), 0.25)),
        ("Nod while cocked and raised", "roll 18°, heave +6, pitch −10° → +10° in 0.15 s", minjerk((-10, 18, 6), (10, 18, 6), 0.15)),
        ("Nod while cocked", "roll 18°, heave 0, pitch −10° → +10° in 0.15 s", minjerk((-10, 18, 0), (10, 18, 0), 0.15)),
        ("Speech bob", "heave ±3 mm at 5 Hz", sinusoid((0, 0, 0), (0, 0, 3), 5.0)),
        ("Celebrate bounce", "heave −6 → +6 mm in 0.12 s", minjerk((0, 0, -6), (0, 0, 6), 0.12)),
        ("Breathing (idle, 300 mA)", "pitch ±2°, heave ±3 mm at 0.3 Hz", sinusoid((0, 0, 0), (2, 0, 3), 0.3)),
        ("Breathing (idle, 400 mA)", "pitch ±2°, heave ±3 mm at 0.3 Hz", sinusoid((0, 0, 0), (2, 0, 3), 0.3)),
    ]
    results = {}
    for name, desc, prof in motions:
        lim = 300 if "300 mA" in name else (400 if "400 mA" in name else 600)
        r = check_motion(prof, tilt, heave_extra, Mgen, DRAG, "XL330-M288", lim)
        results[name] = r
        if r.get("unreachable"):
            p_ = r["pose"]; w(f"| {name} | {desc} | — | — | — | — | OUT OF REACH at pitch {p_[0]:+.0f}°, roll {p_[1]:+.0f}°, heave {p_[2]:+.1f} mm |"); continue
        w(f"| {name} | {desc} | {r['w_rpm']:.0f} rpm ({r['speed_frac']*100:.0f} % of no-load) | {r['tau']:.3f} N·m | {r['avail']:.3f} N·m | {r['margin']:.2f} | {verdict(r['margin'])} |")
    w("")
    # ---- external pushes
    w("## Tilt platform: how hard a hand can push before the head yields\n")
    w("In current-based position mode the servo gives way instead of fighting once its current cap is reached. "
      "This is the force at the crown (h 198) at which the first servo reaches its cap, on top of gravity at rest.\n")
    w("| Push | 300 mA idle | 400 mA idle | 600 mA motion |\n|---|---|---|---|")
    lever = (P.SKIN_H_TOP - P.PIVOT_H) / 1000
    for label, Qunit in (("Backward, at the crown", np.array([lever, 0, 0])),
                         ("Sideways, at the crown", np.array([0, lever, 0])),
                         ("Straight down, on the crown", np.array([0, 0, 1.0]))):
        J = jacobian(np.zeros(3)); tau_g = np.linalg.solve(J.T, gen_gravity(np.zeros(3), tilt, heave_extra))
        tau_u = np.linalg.solve(J.T, Qunit); cells = []
        for ma in (300, 400, 600):
            cap = S["kt"] * (ma / 1000 - I0)
            F = min(((cap - np.sign(tu) * tg) / abs(tu)) for tu, tg in zip(tau_u, tau_g) if abs(tu) > 1e-9)
            cells.append(f"{F:.1f} N ({F/G*1000:.0f} gf)")
        w(f"| {label} | {cells[0]} | {cells[1]} | {cells[2]} |")
    w("\nA light pet is about 1–3 N. At 300 mA a 1 N sideways touch already moves the head, so the stroke detector would fight the compliance; 400 mA roughly doubles that threshold while still yielding to a firm press. "
      "A push harder than this back-drives the plastic gears slowly; it does not need to be resisted.\n")
    # ---- yaw
    w("## Yaw (whole bean on the 6810 bearing)\n")
    m_head_all = m_tilt + m_skirt + m_heave_only
    _, _, I_head_z = mass_props(tilt + skirt + heave_only, (0, 0, 0))
    _, _, I_puck_z = mass_props(puck, (0, 0, 0))
    Iz = I_head_z[2, 2] + I_puck_z[2, 2]
    fric = 0.05 + 0.02 + 0.01   # 2RS seal drag + glide pads + fur brushing the floor disc   ASSUMPTION
    w(f"Rotating inertia about the yaw axis: {Iz*1e3:.2f} g·m² (puck {I_puck_z[2,2]*1e3:.2f}, head {I_head_z[2,2]*1e3:.2f}). "
      f"Friction allowance at the puck: {fric:.2f} N·m (sealed-bearing drag, glide pads, fur brushing; ASSUMPTION). Belt efficiency 0.95.\n")
    w("| Servo, ratio | Saccade | Peak servo speed | Needed | Available (600 mA) | Margin | Verdict |\n|---|---|---|---|---|---|---|")
    yaw_cases = [("XL330-M077", 6.0), ("XL330-M288", 6.0)]
    sacc = [(30, 0.20), (45, 0.25), (60, 0.30), (90, 0.40), (90, 0.50), (180, 1.20)]
    yaw_rows = {}
    for sv, ratio in yaw_cases:
        Sv = SERVOS[sv]; cap = Sv["kt"] * (0.6 - I0)
        for ang, T in sacc:
            th = math.radians(ang)
            worst = (1e9, 0, 0, 0)
            for i in range(61):
                s = i / 60
                vel = th * (30 * s**2 - 60 * s**3 + 30 * s**4) / T
                acc = th * (60 * s - 180 * s**2 + 120 * s**3) / T**2
                tau = (Iz * abs(acc) + fric) / ratio / 0.95
                wsv = vel * ratio
                avail = min(Sv["tau_s"] * max(0.0, 1 - wsv / Sv["w_nl"]), cap)
                m = avail / tau
                if m < worst[0]: worst = (m, tau, avail, wsv)
            yaw_rows[(sv, ang, T)] = worst
            w(f"| {sv}, {ratio:.0f}:1 | {ang}° in {T:.2f} s | {worst[3]*60/(2*math.pi):.0f} rpm ({worst[3]/Sv['w_nl']*100:.0f} %) | {worst[1]:.3f} N·m | {worst[2]:.3f} N·m | {worst[0]:.2f} | {verdict(worst[0])} |")
    w("")
    # fastest feasible saccade times with M077 at 6:1, margin >= 1.5
    w("Fastest yaw turn with the XL330-M077 at 6:1 and margin ≥ 1.5:\n")
    w("| Turn | Minimum time |\n|---|---|")
    Sv = SERVOS["XL330-M077"]; cap = Sv["kt"] * (0.6 - I0)
    for ang in (15, 30, 45, 60, 90, 180):
        th = math.radians(ang); T = 0.05
        while T < 3:
            ok = True
            for i in range(61):
                s = i / 60
                vel = th * (30 * s**2 - 60 * s**3 + 30 * s**4) / T
                acc = th * (60 * s - 180 * s**2 + 120 * s**3) / T**2
                tau = (Iz * abs(acc) + fric) / 6.0 / 0.95
                avail = min(Sv["tau_s"] * max(0.0, 1 - vel * 6.0 / Sv["w_nl"]), cap)
                if avail < 1.5 * tau: ok = False; break
            if ok: break
            T += 0.01
        w(f"| {ang}° | {T:.2f} s |")
    w("")
    # ---- arms
    w("## Arms (2 × XL330-M288, horn axis horizontal through the shoulder)\n")
    m_arm, lever_arm, L_arm = 0.022, 0.025, 0.040                   # ASSUMPTION: arm CoM 25 mm from the horn axis
    I_arm = m_arm * (lever_arm**2 + L_arm**2 / 12)
    skin_hinge = 0.03                                              # N·m, fur fold resisting the flap   ASSUMPTION
    w(f"Arm assembly {m_arm*1000:.0f} g with its CoM {lever_arm*1000:.0f} mm from the horn axis (ASSUMPTION), "
      f"inertia {I_arm*1e6:.1f} g·cm², fur-hinge resistance allowance {skin_hinge} N·m (ASSUMPTION).\n")
    w("| Motion | Peak servo speed | Needed | Available (600 mA) | Margin | Verdict |\n|---|---|---|---|---|---|")
    Sa = SERVOS["XL330-M288"]; cap = Sa["kt"] * (0.6 - I0)
    arm_rows = {}
    for label, ang, T in (("Wave 0 → 45° in 0.25 s", 45, 0.25), ("Celebrate 0 → 90° in 0.30 s", 90, 0.30),
                          ("Celebrate 0 → 90° in 0.40 s", 90, 0.40), ("Twitch 0 → 15° in 0.12 s", 15, 0.12)):
        th = math.radians(ang); worst = (1e9, 0, 0, 0)
        for i in range(61):
            s = i / 60
            pos = th * (10 * s**3 - 15 * s**4 + 6 * s**5)
            vel = th * (30 * s**2 - 60 * s**3 + 30 * s**4) / T
            acc = th * (60 * s - 180 * s**2 + 120 * s**3) / T**2
            tau = m_arm * G * lever_arm * abs(math.sin(pos + math.radians(10))) + I_arm * abs(acc) + skin_hinge
            avail = min(Sa["tau_s"] * max(0.0, 1 - vel / Sa["w_nl"]), cap)
            m = avail / tau
            if m < worst[0]: worst = (m, tau, avail, vel)
        arm_rows[label] = worst
        w(f"| {label} | {worst[3]*60/(2*math.pi):.0f} rpm ({worst[3]/Sa['w_nl']*100:.0f} %) | {worst[1]:.3f} N·m | {worst[2]:.3f} N·m | {worst[0]:.2f} | {verdict(worst[0])} |")
    w("")
    # ---- assumptions
    w("## Assumptions to replace with measurements\n")
    w(f"- Fur areal mass {SIGMA_FUR*1e6*1000:.0f} g/m², foam {SIGMA_FOAM*1e6*1000:.0f} g/m² (10 mm of 30 kg/m³). Weigh a 10 × 10 cm swatch of each.")
    w("- Skin and skirt drag on tilt: 0.03 N·m per axis. Measure with the skirt-drag test on the P1 rig (current with and without a taped fur strip).")
    w("- Arm fur-hinge resistance 0.03 N·m and arm mass 22 g at 25 mm. Measure by hanging a weight on a sewn arm.")
    w(f"- Servo current not producing torque (I0) = {I0:.2f} A. Read Present Current with the horn free to find it.")
    w("- Yaw friction 0.08 N·m at the puck, dominated by the sealed bearing (a shielded ZZ bearing drags far less).")
    w("- Torque scales with supply voltage; these numbers are at 5.0 V at the servo.")
    out = "\n".join(L)
    open(os.path.join(HERE, "TORQUE_CHECK.md"), "w").write(out)
    print(out)

if __name__ == "__main__":
    main()
