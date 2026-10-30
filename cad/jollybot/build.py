#!/usr/bin/env python3
"""Build Jolly-bot parts.  python3 build.py [--parts tray,puck,tilt,head,coupons,assembly] [--no-svg]
Outputs: out/step/*.step, out/stl/*.stl, out/svg/*.svg (orthographic views for a visual check)."""
import argparse, os, sys, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import *
import params as P

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

def export(shape, name, svg=True, views=("front", "iso")):
    for sub in ("step", "stl", "svg"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    export_step(shape, os.path.join(OUT, "step", f"{name}.step"))
    export_stl(shape, os.path.join(OUT, "stl", f"{name}.stl"), tolerance=0.05, angular_tolerance=0.2)
    if svg:
        for v in views:
            write_svg(shape, os.path.join(OUT, "svg", f"{name}_{v}.svg"), v)

def write_svg(shape, path, view):
    bb = shape.bounding_box()
    c = bb.center()
    size = max(bb.size.X, bb.size.Y, bb.size.Z)
    dist = size * 4
    if view == "front":
        origin = (c.X, c.Y - dist, c.Z); up = (0, 0, 1)
    elif view == "top":
        origin = (c.X, c.Y, c.Z + dist); up = (0, 1, 0)
    elif view == "side":
        origin = (c.X + dist, c.Y, c.Z); up = (0, 0, 1)
    else:  # iso
        origin = (c.X + dist * 0.6, c.Y - dist * 0.6, c.Z + dist * 0.45); up = (0, 0, 1)
    visible, hidden = shape.project_to_viewport(origin, viewport_up=up, look_at=(c.X, c.Y, c.Z))
    ex = ExportSVG(scale=3)
    ex.add_layer("Visible", line_weight=0.35)
    ex.add_layer("Hidden", line_color=(160, 160, 160), line_weight=0.2, line_type=LineType.ISO_DASH)
    ex.add_shape(visible, layer="Visible")
    ex.add_shape(hidden, layer="Hidden")
    ex.write(path)

def build(parts, svg=True):
    t0 = time.time()
    made = {}
    if "tray" in parts:
        from parts.floor_tray import floor_tray, clamp_ring
        made["floor_tray"] = floor_tray(); made["bearing_clamp_ring"] = clamp_ring()
    if "puck" in parts:
        from parts.puck import puck_bowl, puck_lid
        made["puck_bowl"] = puck_bowl(); made["puck_lid"] = puck_lid()
    if "tilt" in parts:
        from parts.tilt_stack import horn_arm, carrier, spine_plate
        made["horn_arm"] = horn_arm(); made["carrier"] = carrier(); made["spine_plate"] = spine_plate()
    if "head" in parts:
        from parts.head_shell import head_shell
        for s in head_shell(split=True):
            made[s.label] = s
    if "coupons" in parts:
        from parts.coupons import coupons
        for s in coupons():
            made[s.label] = s
    for name, shape in made.items():
        vol = shape.volume
        print(f"  {name:28s} volume {vol/1000:7.1f} cm³  ≈ {vol*1.27/1000:6.0f} g PETG solid   bbox {fmt(shape.bounding_box())}")
        export(shape, name, svg=svg, views=("front", "iso") if "coupon" not in name else ())
    if "assembly" in parts:
        from parts.floor_tray import floor_tray, clamp_ring
        from parts.puck import puck_bowl, puck_lid, servos_in_puck
        from parts.tilt_stack import carrier, spine_plate, bought_tilt_parts
        from parts.head_shell import head_shell, skin_ghost
        children = [floor_tray(), clamp_ring(), puck_bowl(), puck_lid(), carrier(), spine_plate()] + servos_in_puck() + bought_tilt_parts() + head_shell(split=False)
        asm = Compound(children=children); asm.label = "jollybot_assembly"
        export_step(asm, os.path.join(OUT, "step", "jollybot_assembly.step"))
        if svg:
            # section-like view: front, with the skin ghost drawn in a separate layer
            write_svg(asm, os.path.join(OUT, "svg", "jollybot_assembly_front.svg"), "front")
            write_svg(asm, os.path.join(OUT, "svg", "jollybot_assembly_iso.svg"), "iso")
        print(f"  assembly: {len(children)} bodies")
    print(f"done in {time.time()-t0:.1f}s → {OUT}")

def fmt(bb):
    return f"{bb.size.X:.0f}×{bb.size.Y:.0f}×{bb.size.Z:.0f} mm, z {bb.min.Z:.0f}..{bb.max.Z:.0f}"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts", default="tray,puck,tilt,head,coupons,assembly")
    ap.add_argument("--no-svg", action="store_true")
    a = ap.parse_args()
    print(P.report()); print()
    build([p.strip() for p in a.parts.split(",")], svg=not a.no_svg)
