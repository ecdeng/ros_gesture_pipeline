"""Tilt stack: horn arms, carrier (igus bushing + pin boss), spine plate with tangential ball-stud ears."""
from build123d import *
import math
import params as P
from parts.common import cyl, box, polar

def horn_arm():
    """Flat arm from the XL330 horn to the M2 ball stud at HORN_ARM_R. Lies in the horn plane (XY here, Z = horn axis)."""
    a = cyl(P.SERVO.horn_hub_d + 6, 3) + box(P.HORN_ARM_R, 8, 3, P.HORN_ARM_R / 2, 0, 0)
    a += cyl(8, 3, 0, P.HORN_ARM_R, 0)
    a -= cyl(P.SERVO.horn_hub_d + 0.2, 4, -0.5)              # hub recess  (TODO: horn screw pattern from the STEP)
    a -= cyl(2.1, 4, -0.5, P.HORN_ARM_R, 0)                  # M2 ball stud
    a.label = "horn_arm"
    return a

def carrier():
    c = cyl(P.CARRIER_OD, P.CARRIER_H, P.CARRIER_BOTTOM_H)
    c -= cyl(P.BUSHING_BORE_D, P.BUSHING_RJ4JP["l"] + 0.2, P.CARRIER_BOTTOM_H - 0.01)   # bushing at the bottom
    c -= cyl(P.SHAFT_D + 1.0, P.CARRIER_H - P.CARRIER_PIN_BOSS - 0.0, P.CARRIER_BOTTOM_H - 0.5)  # shaft clearance above the bushing
    c += cyl(P.UJOINT["d"] + 4, P.CARRIER_PIN_BOSS, P.CARRIER_TOP_H - P.CARRIER_PIN_BOSS)   # pin boss (flush top)
    c -= cyl(P.UJOINT["bore"], P.CARRIER_PIN_BOSS + 2, P.CARRIER_TOP_H - P.CARRIER_PIN_BOSS - 1)   # Ø5 pin press fit
    c.label = "carrier"
    return c

def spine_plate():
    p = cyl(P.PLATE_D, P.PLATE_T, P.PLATE_BOTTOM_H)
    # hub under the plate for the U-joint upper bore
    p += cyl(P.PLATE_HUB_D, P.PLATE_HUB_DROP, P.PLATE_BOTTOM_H - P.PLATE_HUB_DROP)
    p -= cyl(P.UJOINT["bore"], P.PLATE_HUB_DROP + P.PLATE_T + 1, P.PLATE_BOTTOM_H - P.PLATE_HUB_DROP - 0.5)
    # three ears with tangential ball studs at BALL_R
    for az in P.TILT_SERVO_AZ:
        x, y = polar(P.BALL_R, az)
        ear = Pos(x, y, P.PLATE_TOP_H) * Rot(0, 0, az) * Box(6, 12, P.EAR_H + 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
        p += ear
        # stud hole along the tangent (local Y after Rot az)
        p -= Pos(x, y, P.PLATE_BALL_H) * Rot(0, 0, az) * Rot(90, 0, 0) * Cylinder(1.05, 20)
    # 4x M3 bolt circle for the head shell neck ring, and a rear cable slot
    for az in (45, 135, 225, 315):
        x, y = polar(P.NECK_D / 2 - 5, az)
        p -= cyl(3.4, 10, P.PLATE_BOTTOM_H - 1, x, y)
    p -= box(14, 8, 10, 0, -P.PLATE_D / 2 + 8, P.PLATE_BOTTOM_H - 1)
    p.label = "spine_plate"
    return p

def bought_tilt_parts():
    """Shaft, bushing, U-joint, pushrods and balls, for the assembly view only."""
    out = []
    out.append(cyl(P.SHAFT_D, P.SHAFT_L, P.SHAFT_H0))
    out.append(cyl(P.UJOINT["d"], P.UJOINT["l"], P.CARRIER_TOP_H))
    for az in P.TILT_SERVO_AZ:
        x, y = polar(P.BALL_R, az)
        out.append(cyl(2.0, P.ROD_L, P.HORN_AXIS_H, x, y))             # pushrod at neutral
        out.append(Pos(x, y, P.HORN_AXIS_H) * Sphere(P.BALL_STUD_D / 2))
        out.append(Pos(x, y, P.PLATE_BALL_H) * Sphere(P.BALL_STUD_D / 2))
        hx, hy = polar(P.TILT_SERVO_R, az)                              # horn arm at neutral (pointing inward)
        out.append(Pos(0, 0, 0) * (Pos(hx, hy, P.HORN_AXIS_H) * Rot(0, 0, az) * Rot(90, 0, 0) * Rot(0, 0, 180) * horn_arm()))
    return out
