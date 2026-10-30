"""Static floor tray: ballast pocket, feet, bearing boss + clamp ring, static GT2 ring, homing magnet, jack slot."""
from build123d import *
import params as P
from parts.common import cyl, box, ring, gt2_external_pulley, polar

def floor_tray():
    t = cyl(P.TRAY_D, P.TRAY_H, 0)
    # ballast pocket from below (open at the bottom, discs sit on the feet plane)
    t -= cyl(P.STEEL_D + 0.6, P.STEEL_T * P.STEEL_N + 0.4, -1)
    # feet recesses
    for az in (45, 135, 225, 315):
        x, y = polar(P.FEET_R, az)
        t -= cyl(P.FEET_D + 0.4, P.FEET_DEPTH + 1, -1, x, y)
    # bearing boss for the 6810 inner race (h 7..14) and a through bore for the clock spring
    B = P.BEARING_6810
    t -= cyl(P.TRAY_D, P.TRAY_H - 7 + 1, 7)                       # drop the top down to h 7 ...
    t += cyl(P.BEARING_BOSS_D, 7, 7)                              # ... and raise the boss back up
    t += ring(P.RING_OD + 6, P.RING_OD - 10, 7, 7)                # support wall under the static GT2 ring
    t -= cyl(P.BORE_D - 6, P.TRAY_H + 2, -1)                      # Ø44 bore for the 2-wire clock spring
    # static GT2 ring h 14..22 (belt wraps outside it)
    t += gt2_external_pulley(P.RING_TEETH, P.RING_H1 - P.RING_H0, P.RING_H0) - cyl(P.RING_OD - 10, 20, P.RING_H0 - 1)
    # clamp ring screw holes (3x M3) in the boss
    for az in (30, 150, 270):
        x, y = polar(P.BEARING_BOSS_D / 2 - 4, az)
        t -= cyl(2.5, 12, 3, x, y)
    # homing magnet pocket at r 35, rear (-Y), between bearing OD (32.5) and ring (38)
    x, y = polar(P.HALL_R, 270)
    t -= cyl(P.MAGNET["d"] + 0.2, P.MAGNET["t"] + 0.2, 7 - P.MAGNET["t"] - 0.2 + 0.0, x, y)
    # jack slot at the rear rim
    t -= box(P.JACK_W, 12, P.JACK_H, 0, -P.TRAY_D / 2 + 5, 3)
    t.label = "floor_tray"
    return t

def clamp_ring():
    r = ring(P.BEARING_BOSS_D + 12, P.BEARING_BOSS_D - 6, 3, 14)   # sits on the inner race at h 14..17? -> on top of boss
    for az in (30, 150, 270):
        x, y = polar(P.BEARING_BOSS_D / 2 - 4, az)
        r -= cyl(3.4, 6, 13, x, y)
    r.label = "bearing_clamp_ring"
    return r
