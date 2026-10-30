"""All Jolly-bot dimensions in one place (mm). Heights `h` are above the table (Z=0 = table).
Front of the robot = +Y. Change a number here and every part regenerates."""
from dataclasses import dataclass
import math

# ---------------- global envelope (skin outer surface)
SKIN_R_WAIST = 80.0      # widest radius, h 60..82
SKIN_R_BOTTOM = 74.0     # radius at h 12
SKIN_H_BOTTOM = 12.0
SKIN_H_TOP = 198.0
LAYER_STACK = 22.0       # pile + backing + foam + air between skin and printed shell

def skin_r(h: float) -> float:
    """Outer skin radius at height h (same curve as the deck mocks)."""
    if h <= 60:
        return math.sqrt(max(0.0, SKIN_R_WAIST**2 - ((60 - h) * SKIN_R_WAIST / 152.6) ** 2))
    if h <= 82:
        return SKIN_R_WAIST
    t = (h - 82) / (SKIN_H_TOP - 82)
    return SKIN_R_WAIST * math.sqrt(max(0.0, 1 - t ** 2.6))

# ---------------- bought parts
@dataclass(frozen=True)
class XL330:
    w: float = 20.0          # radial footprint when standing
    d: float = 23.0          # depth along the horn axis
    h: float = 34.0          # standing height
    horn_from_top: float = 11.0
    horn_hub_d: float = 10.0 # TODO verify against the XL330-M288-T STEP (horn hole pattern too)
    horn_boss_h: float = 2.5
SERVO = XL330()

BEARING_6810 = dict(id=50.0, od=65.0, w=7.0)
BEARING_BOSS_D = 49.8        # tray boss for the inner race  (tune with coupons/)
BEARING_POCKET_D = 65.2      # puck pocket for the outer race (tune with coupons/)
BUSHING_RJ4JP = dict(id=8.0, od=15.0, l=24.0)
BUSHING_BORE_D = 15.0        # carrier bore (tune with coupons/)
SHAFT_D = 8.0
UJOINT = dict(d=11.0, l=23.0, bore=5.0)   # 5x5 steel universal-joint coupler as sold: Ø11 × 22–23 mm with M4 grub screws
BALL_STUD_D = 4.75           # Align T-Rex 450 linkage ball, M2
MAGNET = dict(d=5.0, t=2.0)
GT2 = dict(pitch=2.0, tooth_depth=0.75, pld=0.254)   # pitch-line offset

# ---------------- floor tray (static)
TRAY_D = 130.0
TRAY_H = 14.0
TRAY_FLOOR_T = 2.0
STEEL_D, STEEL_T, STEEL_N = 110.0, 3.0, 2
FEET_R, FEET_D, FEET_DEPTH = 50.0, 10.0, 1.0
RING_TEETH = 120
RING_PD = RING_TEETH * GT2["pitch"] / math.pi          # 76.39
RING_OD = RING_PD - 2 * GT2["pld"]
RING_H0, RING_H1 = 14.0, 22.0
MAGNET_R = 35.0
JACK_W, JACK_H = 12.0, 9.0

# ---------------- puck (rotates)
PUCK_H0 = 14.0
PUCK_LID_H = 70.0
PUCK_D = 130.0
PUCK_BOTTOM_D = 112.0        # narrower skirt below h 20 so it clears the ring
PUCK_STEP_H = 20.0
PUCK_WALL = 2.4
PUCK_FLOOR_T = 3.0
PUCK_FLOOR_TOP = PUCK_H0 + PUCK_FLOOR_T      # 17
SHELF_H = 48.0
TILT_SERVO_R = 50.0
TILT_SERVO_AZ = (90.0, 210.0, 330.0)        # 90 = front (+Y)
HORN_AXIS_H = PUCK_FLOOR_TOP + SERVO.h - SERVO.horn_from_top   # 40
HORN_ARM_R = 20.0
BALL_R = 30.0
ROD_L = 60.0
YAW_SERVO_R, YAW_SERVO_AZ = 49.8, 150.0   # centre distance for a stocked 130T/260 mm GT2 belt with a 20T pulley (6:1); yaw servo = XL330-M077-T
YAW_PULLEY_TEETH = 20
YAW_PULLEY_PD = YAW_PULLEY_TEETH * GT2["pitch"] / math.pi
HALL_R = 35.0
BORE_D = 50.0                 # clock-spring bore through the puck floor
CABLE_SLOT = (15.0, 8.0)      # lid slots for the pushrods

# ---------------- tilt stack (derived heights)
PLATE_D = 76.0
PLATE_T = 4.0
EAR_H = 8.0                   # ball-stud centre above the plate top
PLATE_BALL_H = HORN_AXIS_H + ROD_L                 # 100 at neutral (horn horizontal, rod vertical)
PLATE_TOP_H = PLATE_BALL_H - EAR_H                 # 92
PLATE_BOTTOM_H = PLATE_TOP_H - PLATE_T             # 88
PLATE_HUB_D, PLATE_HUB_DROP = 20.0, 4.0            # hub under the plate that takes the U-joint upper bore
PIVOT_H = PLATE_BOTTOM_H - PLATE_HUB_DROP - UJOINT["l"] / 2   # cross of the U-joint  (≈72.5)
CARRIER_TOP_H = PLATE_BOTTOM_H - PLATE_HUB_DROP - UJOINT["l"] # ≈61
CARRIER_PIN_BOSS = 4.0
CARRIER_OD = 24.0
CARRIER_H = 36.0
CARRIER_BOTTOM_H = CARRIER_TOP_H - CARRIER_H       # ≈21 at neutral
HEAVE = 6.0
SHAFT_H0 = PUCK_FLOOR_TOP
SHAFT_TOP_H = CARRIER_TOP_H - CARRIER_PIN_BOSS - HEAVE - 1.0  # must stay below the pin boss at +heave
SHAFT_L = SHAFT_TOP_H - SHAFT_H0

# ---------------- head shell
NECK_D = 76.0
NECK_H0 = PLATE_TOP_H                              # shell starts on top of the plate
SHELL_T = 1.6
SHELL_SPLIT_PLANE = "XZ"                            # front / back halves
EYE_LINE_H = 123.0
EYE_SPACING = 50.0
EYE_WELL_D = 16.0
EYE_INSERT_D = 5.6                                  # M4 heat-set insert hole; eye = 10 mm glass cabochon epoxied to an M4 pan-head screw
CHEEK_D, CHEEK_DX, CHEEK_DY = 20.0, 37.0, -8.0      # LED diffuser pockets
SHOULDER_H = 110.0
SHOULDER_AZ_FROM_FRONT = 70.0
HEAD_TOP_H = SKIN_H_TOP - LAYER_STACK               # 176 (shell crown)

def shell_r(h: float) -> float:
    return max(0.0, skin_r(h) - LAYER_STACK)

def report() -> str:
    lines = [
        f"horn axis h        {HORN_AXIS_H:6.1f}",
        f"plate ball h       {PLATE_BALL_H:6.1f}  (rods {ROD_L} mm, neutral)",
        f"plate top/bottom   {PLATE_TOP_H:6.1f} / {PLATE_BOTTOM_H:6.1f}",
        f"pivot (U-joint) h  {PIVOT_H:6.1f}",
        f"carrier h          {CARRIER_BOTTOM_H:6.1f} .. {CARRIER_TOP_H:6.1f}  (heave ±{HEAVE})",
        f"shaft h            {SHAFT_H0:6.1f} .. {SHAFT_TOP_H:6.1f}  (L {SHAFT_L:.1f})",
        f"neck ring h        {NECK_H0:6.1f}  lid h {PUCK_LID_H}  gap {NECK_H0 - PUCK_LID_H:.1f}",
    ]
    gap = NECK_H0 - PUCK_LID_H
    neck_r = NECK_D / 2
    # neck edge dips (neck_r * sin(tilt)) + (NECK_H0 - PIVOT_H) * (1 - cos(tilt)) ... conservative: edge dip ≈ neck_r*sin + drop of the ring centre
    for tilt in (20, 25, 28):
        t = math.radians(tilt)
        dip = neck_r * math.sin(t) - (NECK_H0 - PIVOT_H) * (1 - math.cos(t))
        lines.append(f"neck dip at {tilt:2d}°    {dip:6.1f}  -> {'OK' if dip < gap else 'HITS LID'}")
    return "\n".join(lines)

if __name__ == "__main__":
    print(report())
