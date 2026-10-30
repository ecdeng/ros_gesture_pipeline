# Jolly-bot code-CAD (build123d)

Parametric model of the printed structure for the fluffy tabletop social robot. Every dimension lives in
`params.py` (mm, heights `h` above the table, front = +Y). Parts regenerate from those numbers.

```
pip install -r requirements.txt
python3 build.py                      # everything → out/step, out/stl, out/svg
python3 build.py --parts tilt,puck    # a subset; names: tray, puck, tilt, head, coupons, assembly
python3 params.py                     # derived heights + neck/lid clearance check
```

| Module | Parts | Notes |
|---|---|---|
| `parts/floor_tray.py` | `floor_tray`, `bearing_clamp_ring` | static disc: ballast pocket, feet, Ø49.8 boss for the 6810 inner race, static 120T GT2 ring, homing-magnet pocket, jack slot |
| `parts/puck.py` | `puck_bowl`, `puck_lid` (+ servo ghosts) | rotating bowl: Ø65.2 bearing pocket, Ø50 clock-spring bore, 3 standing XL330 cradles at 120°, yaw-servo cradle + pulley slot, shaft boss, hall pad; lid with pushrod slots |
| `parts/tilt_stack.py` | `horn_arm`, `carrier`, `spine_plate` | horn arm r 20 → M2 ball; carrier for the igus RJ4JP-01-08 bushing with a Ø5 pin boss; Ø76 plate with three tangential ball-stud ears and a hub for the U-joint |
| `parts/head_shell.py` | `head_front`, `head_back` | skin profile revolved, offset inward 22 mm, shelled to 1.6 mm, split on XZ; face plate, eye wells + M4 insert holes, cheek pockets, camera window, shoulder pockets, M3 bosses, vents |
| `parts/coupons.py` | 9 coupons | print first: bearing boss, bearing pocket, bushing bore at −0.2 / 0 / +0.2 mm |

## Derived heights (CAD supersedes the written plan where they differ)
`python3 params.py` prints them. With 60 mm rods and the horn axis at h 40 the plate sits at h 88–92 and the
U-joint cross at h ≈72, lower than the plan's h 90 estimate; the neck ring (h 92) still clears the lid (h 70) by
22 mm against a 16 mm dip at 28° combined tilt. Raise `ROD_L` or `EAR_H` to move the pivot up.

## Print notes
- Floor tray: flat, top up. Puck bowl: open side up (cradles print support-free). Carrier: vertical.
- Horn arms: flat, 100 % infill. Spine plate: flat, ears up. Head halves: open side down, 2 perimeters.
- Everything PETG except TPU servo pads and bumpers (not modelled).

## Still to do in CAD
- Horn arm hub against the real XL330-M288-T horn (download the STEP; `SERVO.horn_hub_d` is a guess).
- Servo cradle screw holes once the XL330 side-hole pattern is confirmed; currently friction pockets.
- Yaw pulley (30T GT2 on a horn adapter), TPU boots, puck lid mesh-collar ring, foot nubs.
- Exact kinematic check: sweep tilt/heave with the rods modelled and verify no rod touches the lid slots.
