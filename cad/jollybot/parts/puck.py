"""Rotating puck: bowl with bearing pocket, servo cradles, shaft boss, yaw pulley slot, hall pad; and the lid."""
from build123d import *
import math
import params as P
from parts.common import cyl, box, ring, polar, servo_xl330, place_tilt_servo

def puck_bowl():
    h_total = P.PUCK_LID_H - P.PUCK_H0
    outer = cyl(P.PUCK_BOTTOM_D, P.PUCK_STEP_H - P.PUCK_H0, P.PUCK_H0) + cyl(P.PUCK_D, P.PUCK_LID_H - P.PUCK_STEP_H, P.PUCK_STEP_H)
    inner = cyl(P.PUCK_BOTTOM_D - 2 * P.PUCK_WALL, P.PUCK_STEP_H - P.PUCK_FLOOR_TOP + 1, P.PUCK_FLOOR_TOP) \
          + cyl(P.PUCK_D - 2 * P.PUCK_WALL, P.PUCK_LID_H - P.PUCK_STEP_H + 1, P.PUCK_STEP_H)
    b = outer - inner
    # bearing pocket for the 6810 outer race (open at the bottom, with a 1.5 mm lip inside)
    b -= cyl(P.BEARING_POCKET_D, P.BEARING_6810["w"] + 0.2, P.PUCK_H0 - 0.01)
    b -= cyl(P.BORE_D, P.PUCK_FLOOR_T + 2, P.PUCK_H0 - 1)           # Ø50 bore (clock spring passes here)
    # central shaft boss with 8 mm hole and a grub-screw hole
    b += cyl(16, 12, P.PUCK_FLOOR_TOP)
    b -= cyl(P.SHAFT_D + 0.1, 14, P.PUCK_FLOOR_TOP - 0.5)
    b -= Pos(0, 0, P.PUCK_FLOOR_TOP + 7) * Rot(0, 90, 0) * Cylinder(1.7, 20)   # M4 tap drill, through the boss
    # tilt-servo cradles: 2.4 mm walls around a clearance pocket, open top, open toward the horn
    for az in P.TILT_SERVO_AZ:
        cradle = place_tilt_servo(Pos(0, 0, 0) * Box(P.SERVO.d + 0.6 + 4.8, P.SERVO.w + 0.6 + 4.8, 12,
                                                     align=(Align.CENTER, Align.CENTER, Align.MIN)), az)
        pocket = place_tilt_servo(Box(P.SERVO.d + 0.6, P.SERVO.w + 0.6, 40, align=(Align.CENTER, Align.CENTER, Align.MIN)), az)
        b += cradle
        b -= pocket
    # yaw servo cradle (horn down through the floor) + pulley slot
    x, y = polar(P.YAW_SERVO_R, P.YAW_SERVO_AZ)
    b += Pos(x, y, P.PUCK_FLOOR_TOP) * Rot(0, 0, P.YAW_SERVO_AZ) * Box(P.SERVO.w + 5.4, P.SERVO.d + 5.4, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
    b -= Pos(x, y, P.PUCK_FLOOR_TOP) * Rot(0, 0, P.YAW_SERVO_AZ) * Box(P.SERVO.w + 0.6, P.SERVO.d + 0.6, 40, align=(Align.CENTER, Align.CENTER, Align.MIN))
    b -= cyl(P.YAW_PULLEY_PD + 6, P.PUCK_FLOOR_T + 2, P.PUCK_H0 - 1, x, y)     # pulley passes through the floor
    # hall sensor pad (3 mm slot) on the floor underside at r 35, front-right so it never meets the magnet's rear position at home
    hx, hy = polar(P.HALL_R, 270)
    b -= box(5, 4, 2, hx, hy, P.PUCK_H0 - 0.01)
    # cable notch at the rear rim top for the head harness
    b -= box(14, 8, 10, 0, -P.PUCK_D / 2 + 2, P.PUCK_LID_H - 8)
    b.label = "puck_bowl"
    return b

def puck_lid():
    L = cyl(P.PUCK_D, 3, P.PUCK_LID_H - 3)
    L -= cyl(P.CARRIER_OD + 4, 5, P.PUCK_LID_H - 4)                      # carrier passes through
    for az in P.TILT_SERVO_AZ:                                           # pushrod slots at r 30 (radial 15 x tangential 8)
        x, y = polar(P.BALL_R, az)
        L -= Pos(x, y, P.PUCK_LID_H - 4) * Rot(0, 0, az) * Box(P.CABLE_SLOT[0], P.CABLE_SLOT[1], 6, align=(Align.CENTER, Align.CENTER, Align.MIN))
    L -= cyl(P.SHAFT_D, 6, P.PUCK_LID_H - 4)
    L.label = "puck_lid"
    return L

def servos_in_puck():
    """Visualisation only: the three tilt servos and the yaw servo in place."""
    parts = [place_tilt_servo(servo_xl330(), az) for az in P.TILT_SERVO_AZ]
    x, y = polar(P.YAW_SERVO_R, P.YAW_SERVO_AZ)
    yaw = Pos(x, y, P.PUCK_FLOOR_TOP + P.SERVO.h) * Rot(180, 0, P.YAW_SERVO_AZ + 90) * servo_xl330()  # horn down
    return parts + [yaw]
