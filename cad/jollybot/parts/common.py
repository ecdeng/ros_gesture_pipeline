"""Shared helpers and models of bought parts (for pockets and for the assembly view)."""
from build123d import *
import math
import params as P

def cyl(d, h, z0=0.0, x=0.0, y=0.0):
    """Cylinder of diameter d from z0 up to z0+h."""
    return Pos(x, y, z0) * Cylinder(d / 2, h, align=(Align.CENTER, Align.CENTER, Align.MIN))

def box(l, w, h, x=0.0, y=0.0, z0=0.0):
    return Pos(x, y, z0) * Box(l, w, h, align=(Align.CENTER, Align.CENTER, Align.MIN))

def polar(r, az_deg):
    a = math.radians(az_deg)
    return r * math.cos(a), r * math.sin(a)

def servo_xl330(clearance=0.0):
    """XL330 standing on Z=0, horn axis along +X (tangential when placed at azimuth az with Rot Z=az).
    Body footprint: w (Y, radial when rotated) x d (X). Horn boss on the +X face, horn_from_top below the top."""
    S = P.SERVO
    c = clearance
    body = Pos(0, 0, 0) * Box(S.d + c, S.w + c, S.h + c, align=(Align.CENTER, Align.CENTER, Align.MIN))
    horn_z = S.h - S.horn_from_top
    horn = Pos(S.d / 2, 0, horn_z) * Rot(0, 90, 0) * Cylinder(S.horn_hub_d / 2 + c / 2, S.horn_boss_h + c,
                                                            align=(Align.CENTER, Align.CENTER, Align.MIN))
    return body + horn

def place_tilt_servo(shape, az):
    """Move a servo built by servo_xl330 (horn along +X) so its horn axis is tangential at radius TILT_SERVO_R
    and the horn face points toward +tangent. Servo stands on the puck floor top."""
    x, y = polar(P.TILT_SERVO_R, az)
    # horn axis along local X; rotate so local X is tangential (az + 90), local Y radial
    return Pos(x, y, P.PUCK_FLOOR_TOP) * Rot(0, 0, az + 90) * shape

def ring(d_out, d_in, h, z0=0.0):
    return cyl(d_out, h, z0) - cyl(d_in + 0.0, h + 2, z0 - 1)

def gt2_external_pulley(teeth, h, z0=0.0, groove_w=1.0):
    """Simplified GT2 pulley: cylinder at OD with rectangular grooves (good enough for a printed ring)."""
    pd = teeth * P.GT2["pitch"] / math.pi
    od = pd - 2 * P.GT2["pld"]
    body = cyl(od, h, z0)
    depth = P.GT2["tooth_depth"]
    grooves = Sketch()
    for loc in PolarLocations(od / 2 - depth / 2 + 0.3, teeth):
        grooves += loc * Rectangle(depth + 0.6, groove_w)
    body -= Pos(0, 0, z0 - 1) * extrude(grooves, h + 2)
    return body
