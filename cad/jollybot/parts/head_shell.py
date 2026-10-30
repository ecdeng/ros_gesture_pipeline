"""Head shell: revolve the skin profile, offset inward by the layer stack, shell to 1.6 mm, cut features, split front/back."""
from build123d import *
import math
import params as P
from parts.common import cyl, box, polar

def _profile_face(radius_fn, h0, h1, n=40):
    pts = []
    for i in range(n + 1):
        h = h0 + (h1 - h0) * i / n
        r = radius_fn(h)
        pts.append((max(r, 0.01), h))
    pts[-1] = (0.01, h1)
    curve = Spline(*pts)
    closing = Polyline((0.01, h1), (0, h1), (0, h0), (pts[0][0], h0))
    return Plane.XZ * make_face(curve + closing)

def head_solid():
    return revolve(_profile_face(P.shell_r, P.NECK_H0, P.HEAD_TOP_H), Axis.Z, 360)

def head_shell(split=True):
    solid = head_solid()
    shell = solid - offset(solid, -P.SHELL_T)
    # open the neck: cut everything below NECK_H0 + 0.01 is already the base; remove the base face by cutting a disc slightly inside
    shell -= cyl(P.NECK_D - 2 * P.SHELL_T, 3, P.NECK_H0 - 1)
    # neck ring (bolts to the spine plate)
    neck = cyl(P.NECK_D, 4, P.NECK_H0) - cyl(P.NECK_D - 12, 6, P.NECK_H0 - 1)
    for az in (45, 135, 225, 315):
        x, y = polar(P.NECK_D / 2 - 5, az)
        neck -= cyl(3.4, 10, P.NECK_H0 - 1, x, y)
    shell += neck
    # face plate: a flat chord at the front (+Y) with eye wells, insert bosses and cheek pockets
    y_face = P.shell_r(P.EYE_LINE_H) - 3.0
    plate = box(84, 3, 62, 0, y_face + 1.5, P.EYE_LINE_H - 26)
    shell += plate
    for sx in (-1, 1):
        ex = sx * P.EYE_SPACING / 2
        shell -= Pos(ex, y_face - 2, P.EYE_LINE_H) * Rot(90, 0, 0) * Cylinder(P.EYE_WELL_D / 2, 2.0)      # 2 mm well
        shell -= Pos(ex, y_face + 6, P.EYE_LINE_H) * Rot(90, 0, 0) * Cylinder(P.EYE_INSERT_D / 2, 12)     # M4 insert
        shell -= Pos(ex + sx * P.CHEEK_DX - sx * P.EYE_SPACING / 2 * 0, y_face + 6, P.EYE_LINE_H + P.CHEEK_DY) * Rot(90, 0, 0) * Cylinder(P.CHEEK_D / 2, 12)
    # camera window behind the robot's-left eye (robot left = -X when front is +Y)
    shell -= box(26, 12, 26, -P.EYE_SPACING / 2, y_face - 6, P.EYE_LINE_H - 13)
    # shoulder pockets with horn extension bores at SHOULDER_H, 70° from front
    for sx in (-1, 1):
        az = 90 - sx * P.SHOULDER_AZ_FROM_FRONT
        r = P.shell_r(P.SHOULDER_H)
        x, y = polar(r - 16, az)
        pocket = Pos(x, y, P.SHOULDER_H - P.SERVO.h / 2) * Rot(0, 0, az) * Box(P.SERVO.w + 6, P.SERVO.d + 6, P.SERVO.h + 6, align=(Align.CENTER, Align.CENTER, Align.MIN))
        hole = Pos(x, y, P.SHOULDER_H - P.SERVO.h / 2 + 2) * Rot(0, 0, az) * Box(P.SERVO.w + 0.6, P.SERVO.d + 0.6, P.SERVO.h + 1, align=(Align.CENTER, Align.CENTER, Align.MIN))
        shell += pocket
        shell -= hole
        shell -= Pos(0, 0, P.SHOULDER_H) * Rot(0, 0, az) * Pos(r + 10, 0, 0) * Rot(0, 90, 0) * Cylinder(6, 40)   # horn extension bore
    # six M3 insert bosses on the split plane (XZ), three per side
    for sx in (-1, 1):
        for h in (P.NECK_H0 + 20, P.EYE_LINE_H + 10, P.HEAD_TOP_H - 22):
            r = P.shell_r(h) - 4
            shell += Pos(sx * r, 0, h) * Rot(0, 0, 0) * Box(8, 8, 10, align=(Align.CENTER, Align.CENTER, Align.CENTER))
            shell -= Pos(sx * r, 0, h) * Rot(90, 0, 0) * Cylinder(2.3, 10)
    # crown mesh port + chin vent
    shell -= cyl(12, 10, P.HEAD_TOP_H - 5)
    shell -= box(30, 10, 12, 0, P.shell_r(P.NECK_H0 + 8) - 2, P.NECK_H0 + 6)
    shell.label = "head_shell"
    if not split:
        return [shell]
    front = split_shape(shell, Plane.XZ, Keep.BOTTOM)   # +Y side (front)
    back = split_shape(shell, Plane.XZ, Keep.TOP)
    front.label, back.label = "head_front", "head_back"
    return [front, back]

def split_shape(shape, plane, keep):
    return split(shape, bisect_by=plane, keep=keep)

def skin_ghost():
    """Translucent skin envelope for the assembly view."""
    s = revolve(_profile_face(P.skin_r, P.SKIN_H_BOTTOM, P.SKIN_H_TOP), Axis.Z, 360)
    s.label = "skin_envelope"
    return s
