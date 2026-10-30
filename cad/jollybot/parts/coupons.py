"""Print-first test coupons: bearing boss, bearing pocket, bushing bore. Three sizes each."""
from build123d import *
import params as P
from parts.common import cyl, ring

def coupons():
    out = []
    for i, dd in enumerate((-0.2, 0.0, 0.2)):
        boss = ring(P.BEARING_BOSS_D + dd, 30, 8, 0); boss.label = f"coupon_boss_{P.BEARING_BOSS_D + dd:.1f}"
        pocket = ring(P.BEARING_POCKET_D + dd + 8, P.BEARING_POCKET_D + dd, 8, 0); pocket.label = f"coupon_pocket_{P.BEARING_POCKET_D + dd:.1f}"
        bore = ring(P.BUSHING_BORE_D + dd + 8, P.BUSHING_BORE_D + dd, 12, 0); bore.label = f"coupon_bore_{P.BUSHING_BORE_D + dd:.1f}"
        out += [boss, pocket, bore]
    return out
