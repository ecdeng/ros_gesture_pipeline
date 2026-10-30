#!/usr/bin/env python3
"""Shaded renders of the full assembly (printed parts + fasteners + bought hardware + electronics).
Writes out/render/scene.json + scene.html, then screenshots with Playwright (node render.js)."""
import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import *
import params as P
from parts.floor_tray import floor_tray, clamp_ring
from parts.puck import puck_bowl, puck_lid, servos_in_puck
from parts.tilt_stack import carrier, spine_plate
from parts.head_shell import head_shell, skin_ghost
from parts import hardware as H

COLORS = {"tray": "#8FA8BF", "puck": "#A6C4A0", "tan": "#D9B58C", "head": "#C7B5D8",
          "steel": "#8A94A0", "black": "#2A2A2E", "brass": "#C9A24A", "red": "#C8553D", "plastic": "#3C3C3C",
          "rubber": "#1E1E1E", "servo": "#22303C", "pcb": "#2E7D5B", "speaker": "#444444", "skin": "#F3EADA"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "render")

def tess(shape, tol=0.12, ang=0.35):
    verts, tris = shape.tessellate(tol, ang)
    return [round(c, 2) for v in verts for c in (v.X, v.Y, v.Z)], [i for t in tris for i in t]

def main():
    os.makedirs(OUT, exist_ok=True)
    bodies = []
    def add(shape, color, group, name=""):
        v, t = tess(shape)
        bodies.append(dict(name=name or getattr(shape, "label", ""), color=COLORS[color], group=group, v=v, t=t))
    add(floor_tray(), "tray", "tray"); add(clamp_ring(), "tray", "tray")
    add(puck_bowl(), "puck", "puck"); add(puck_lid(), "puck", "puck")
    for s in servos_in_puck(): add(s, "servo", "puck", "servo")
    add(carrier(), "tan", "tilt"); add(spine_plate(), "tan", "tilt")
    for s in head_shell(split=True): add(s, "head", "head")
    for fn in (H.tray_hardware, H.puck_hardware, H.tilt_hardware, H.head_hardware, H.electronics):
        for shape, color, group in fn():
            add(shape, color, group, color)
    skin = skin_ghost(); v, t = tess(skin, 0.08, 0.2)
    bodies.append(dict(name="skin", color=COLORS["skin"], group="skin", v=v, t=t))
    ntri = sum(len(b["t"]) // 3 for b in bodies)
    json.dump(bodies, open(os.path.join(OUT, "scene.json"), "w"))
    print(f"{len(bodies)} bodies, {ntri} triangles")
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["node", os.path.join(here, "render.js"), OUT], check=True)

if __name__ == "__main__":
    main()
