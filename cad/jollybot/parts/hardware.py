"""Fasteners and bought hardware, positioned in the assembly. Each function returns a list of (shape, colour_key, group)."""
from build123d import *
import math
import params as P
from parts.common import cyl, box, polar, ring
from parts.tilt_stack import horn_arm

STEEL, BLACK, BRASS, RED, PLASTIC, RUBBER = "steel", "black", "brass", "red", "plastic", "rubber"

def screw(d, length, head_d=None, head_h=None):
    """Socket-cap screw along +Z: head from z=0 up, shank going down to -length."""
    head_d = head_d or (d * 1.8); head_h = head_h or d
    s = cyl(head_d, head_h, 0) + cyl(d, length, -length)
    s -= cyl(d * 0.75, head_h * 0.7, head_h * 0.3 + 0.01)   # hex socket (round, close enough)
    return s

def insert(d_outer, length):
    return cyl(d_outer, length, 0) - cyl(d_outer - 1.6, length + 1, -0.5)

def at(x, y, z, rot=None):
    return (Pos(x, y, z) * rot) if rot is not None else Pos(x, y, z)

def tray_hardware():
    out = []
    # steel ballast discs, rubber feet, bearing, clamp-ring screws, magnet, jack
    for i in range(P.STEEL_N):
        out.append((cyl(P.STEEL_D, P.STEEL_T, i * P.STEEL_T), STEEL, "tray"))
    for az in (45, 135, 225, 315):
        x, y = polar(P.FEET_R, az)
        out.append((cyl(P.FEET_D, 4, -3, x, y), RUBBER, "tray"))
    B = P.BEARING_6810
    out.append((ring(B["od"], B["id"], B["w"], 7), STEEL, "tray"))
    for az in (30, 150, 270):
        x, y = polar(P.BEARING_BOSS_D / 2 - 4, az)
        out.append((at(x, y, 17) * screw(3, 8), BLACK, "tray"))
    x, y = polar(P.HALL_R, 270)
    out.append((cyl(P.MAGNET["d"], P.MAGNET["t"], 7 - P.MAGNET["t"], x, y), STEEL, "tray"))
    out.append((box(11, 10, 8, 0, -P.TRAY_D / 2 + 6, 3.5), BLACK, "tray"))   # magnetic jack
    return out

def puck_hardware():
    out = []
    # hall sensor on the floor underside
    hx, hy = polar(P.HALL_R, 270)
    out.append((box(4, 3, 1.5, hx, hy, P.PUCK_H0 + 0.0), BLACK, "puck"))
    # shaft, grub screw
    out.append((cyl(P.SHAFT_D, P.SHAFT_L, P.SHAFT_H0), STEEL, "puck"))
    out.append((at(8, 0, P.PUCK_FLOOR_TOP + 7, Rot(0, 90, 0)) * cyl(4, 6, -6), BLACK, "puck"))
    # tilt-servo cradle screws: M2 through the outer cradle wall into the servo side, two per servo
    for az in P.TILT_SERVO_AZ:
        for dt in (-7, 7):
            a = math.radians(az)
            r_out = P.TILT_SERVO_R + P.SERVO.w / 2 + 0.3 + 2.4          # outer face of the cradle wall
            x = r_out * math.cos(a) - dt * math.sin(a); y = r_out * math.sin(a) + dt * math.cos(a)
            out.append((at(x, y, P.PUCK_FLOOR_TOP + 7, Rot(0, 0, az) * Rot(0, 90, 0)) * screw(2, 6), BLACK, "puck"))
    # yaw pulley (30T) on the yaw servo horn, below the floor, and a simplified belt
    x, y = polar(P.YAW_SERVO_R, P.YAW_SERVO_AZ)
    out.append((cyl(P.YAW_PULLEY_PD - 0.5, 6.5, P.PUCK_H0 + 0.5, x, y), STEEL, "puck"))
    belt_ring = ring(P.RING_OD + 2.8, P.RING_OD, 6, 15)
    belt_pul = ring(P.YAW_PULLEY_PD + 2.8, P.YAW_PULLEY_PD, 6, 15) ; belt_pul = Pos(x, y, 0) * belt_pul
    # two straight tangents (approximate as thin boxes between the two circles)
    d = math.hypot(x, y); ang = math.degrees(math.atan2(y, x))
    R1 = P.RING_OD / 2 + 1.4; R2 = P.YAW_PULLEY_PD / 2 + 1.4
    L = math.sqrt(max(d * d - (R1 - R2) ** 2, 1))
    tang = []
    for sgn in (1, -1):
        off = math.degrees(math.acos((R1 - R2) / d))
        t = math.radians(ang + sgn * off)
        p1 = (R1 * math.cos(t), R1 * math.sin(t)); p2 = (x + R2 * math.cos(t), y + R2 * math.sin(t))
        cx, cy = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        a2 = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
        tang.append(Pos(cx, cy, 15) * Rot(0, 0, a2) * Box(L, 1.4, 6, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    out.append((belt_ring + belt_pul + tang[0] + tang[1], RUBBER, "puck"))
    # puck lid screws (4x M3 into the rim)
    for az in (0, 90, 180, 270):
        x, y = polar(P.PUCK_D / 2 - 4, az)
        out.append((at(x, y, P.PUCK_LID_H) * screw(3, 10), BLACK, "puck"))
    return out

def tilt_hardware():
    out = []
    # bushing in the carrier, pins, U-joint
    out.append((ring(P.BUSHING_RJ4JP["od"], P.BUSHING_RJ4JP["id"], P.BUSHING_RJ4JP["l"], P.CARRIER_BOTTOM_H), PLASTIC, "tilt"))
    out.append((cyl(P.UJOINT["bore"], 10, P.CARRIER_TOP_H - 5), STEEL, "tilt"))
    out.append((cyl(P.UJOINT["bore"], 10, P.PLATE_BOTTOM_H - P.PLATE_HUB_DROP - 5), STEEL, "tilt"))
    uj = cyl(P.UJOINT["d"], P.UJOINT["l"], P.CARRIER_TOP_H)
    uj -= box(P.UJOINT["d"] + 2, 3, 6, 0, 0, P.PIVOT_H - 3)       # a slot to read as a cross joint
    out.append((uj, STEEL, "tilt"))
    # horn arms with 4x M2 screws and the ball stud, pushrods with ball links, plate studs with nuts
    for az in P.TILT_SERVO_AZ:
        hx, hy = polar(P.TILT_SERVO_R, az)
        T = Pos(hx, hy, P.HORN_AXIS_H) * Rot(0, 0, az) * Rot(90, 0, 0) * Rot(0, 0, 180)
        out.append((T * horn_arm(), "tan", "tilt"))
        for k in range(4):
            a = math.radians(45 + 90 * k)
            out.append((T * (Pos(3 * math.cos(a), 3 * math.sin(a), 5) * screw(2, 5)), BLACK, "tilt"))
        stud_local = Pos(P.HORN_ARM_R, 0, 3) * (cyl(2, 3, 0) + Pos(0, 0, 3 + 2.0) * Sphere(P.BALL_STUD_D / 2)) 
        out.append((T * stud_local, RED, "tilt"))
        out.append((T * (Pos(P.HORN_ARM_R, 0, -2) * cyl(4, 1.6, 0)), STEEL, "tilt"))          # M2 nut behind the arm
        bx, by = polar(P.BALL_R, az)
        # ball links (plastic sockets) and the rod
        out.append((cyl(6, 9, P.HORN_AXIS_H + 1, bx, by) - Pos(bx, by, P.HORN_AXIS_H + 5) * Sphere(2.5), PLASTIC, "tilt"))
        out.append((cyl(6, 9, P.PLATE_BALL_H - 10, bx, by), PLASTIC, "tilt"))
        out.append((cyl(2, P.ROD_L - 20, P.HORN_AXIS_H + 10, bx, by), STEEL, "tilt"))
        # plate stud: M2 through the ear along the tangent, ball on the outer face, nut on the inner face
        Tp = Pos(bx, by, P.PLATE_BALL_H) * Rot(0, 0, az) * Rot(90, 0, 0)
        out.append((Tp * (cyl(2, 14, -7) + Pos(0, 0, 7 + 2.0) * Sphere(P.BALL_STUD_D / 2)), RED, "tilt"))
        out.append((Tp * cyl(4, 1.6, -8.6), STEEL, "tilt"))
    # neck ring screws (4x M3) through the neck ring into the plate
    for az in (45, 135, 225, 315):
        x, y = polar(P.NECK_D / 2 - 5, az)
        out.append((at(x, y, P.NECK_H0 + 4) * screw(3, 10), BLACK, "head"))
    return out

def head_hardware():
    out = []
    # split-line inserts and screws (6), eye inserts + eyes (2), arm servos, horn extensions, paddles, camera, MPR121
    for sx in (-1, 1):
        for h in (P.NECK_H0 + 20, P.EYE_LINE_H + 10, P.HEAD_TOP_H - 22):
            r = P.shell_r(h) - 4
            out.append((at(sx * r, 0, h, Rot(-90, 0, 0)) * insert(4.6, 5), BRASS, "head"))        # insert in the front half (y 0..5)
            out.append((at(sx * r, -4, h, Rot(90, 0, 0)) * screw(3, 10), BLACK, "head"))          # screw from the back half, head at y -4
    y_face = P.shell_r(P.EYE_LINE_H) - 3.0
    for sx in (-1, 1):
        ex = sx * P.EYE_SPACING / 2
        out.append((at(ex, y_face + 6, P.EYE_LINE_H, Rot(90, 0, 0)) * insert(5.6, 6), BRASS, "head"))
        eye = Pos(ex, y_face + 2, P.EYE_LINE_H) * Sphere(5.5) + Pos(ex, y_face - 6, P.EYE_LINE_H) * Rot(90, 0, 0) * Cylinder(2, 10)
        out.append((eye, BLACK, "head"))
    for sx in (-1, 1):
        az = 90 - sx * P.SHOULDER_AZ_FROM_FRONT
        r = P.shell_r(P.SHOULDER_H)
        x, y = polar(r - 16, az)
        from parts.common import servo_xl330
        servo = Pos(x, y, P.SHOULDER_H - P.SERVO.h / 2 + 2) * Rot(0, 0, az) * Rot(0, 0, 90) * servo_xl330()
        out.append((servo, "servo", "head"))
        ext = Pos(0, 0, P.SHOULDER_H) * Rot(0, 0, az) * Pos(r - 6, 0, 0) * Rot(0, 90, 0) * Cylinder(4, 28, align=(Align.CENTER, Align.CENTER, Align.MIN))
        out.append((ext, "tan", "head"))
        paddle = Pos(0, 0, P.SHOULDER_H) * Rot(0, 0, az) * Pos(r + 24, 0, -4) * Box(3, 20, 45, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        out.append((paddle, "tan", "head"))
        for dz in (-12, 12):
            out.append((Pos(0, 0, P.SHOULDER_H) * Rot(0, 0, az) * Pos(r + 25.5, 0, dz) * Rot(0, 90, 0) * screw(2, 6), BLACK, "head"))
    out.append((box(18, 2, 18, -P.EYE_SPACING / 2 + 3, y_face - 13, P.EYE_LINE_H - 9), "pcb", "head"))     # camera board, inside the shell
    out.append((box(20, 20, 2, 0, 0, P.HEAD_TOP_H - 16), "pcb", "head"))                               # MPR121
    return out

def electronics():
    out = []
    x, y = polar(42, 270)
    out.append((Pos(x, y, 51) * Box(65, 30, 17, align=(Align.CENTER, Align.CENTER, Align.MIN)), "pcb", "puck"))    # Pi Zero 2 W + HAT
    x, y = polar(50, 30)
    out.append((Pos(x, y, 51) * Rot(0, 0, 120) * Box(60, 25, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)), "pcb", "puck"))  # OpenRB
    x, y = polar(48, 62)
    out.append((Pos(x, y, 54) * Rot(0, 0, 62) * Rot(0, 90, 0) * Cylinder(14, 5), "speaker", "puck"))
    x, y = polar(54, 190)
    out.append((Pos(x, y, 17) * Rot(0, 0, 280) * Box(33, 20, 8, align=(Align.CENTER, Align.CENTER, Align.MIN)), "pcb", "puck"))   # D36V50F5
    x, y = polar(55, 250)
    out.append((Pos(x, y, 17) * Rot(0, 0, 340) * Box(18, 18, 7, align=(Align.CENTER, Align.CENTER, Align.MIN)), "pcb", "puck"))   # D24V22F5
    return out
