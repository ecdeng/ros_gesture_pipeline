# "Jolly-bot" — a tabletop fluffy social robot (plan v1)

## 0. Reference: what we are imitating
Meta's Muse AI agent ships with a mascot named **Jolly** (also "Jollybot"), designed by Alex Cornell.
Press descriptions converge on: cream / ivory plush fur, round rounded-edge body (compared to a Labubu,
a Fall Guys bean, a Teletubby, the Doctor Who "Adipose"), small beady black eyes, soft pink cheeks, a tiny
upward smile, blank-but-pleasant expression, stubby limbs. In the app it animates to show agent status
(e.g. tapping a keyboard). A plush version exists in ads; a 2" screen "Muse Charm" keychain is planned.

Design takeaways: a single blob (no neck, no distinct head), expression comes from body posture + tiny face.
This is the same gestalt as Keepon (Kozima/Michalowski), which proved a 4-DOF blob with a static face is
highly expressive. So: **posture-driven expression, static or near-static face.**

## 1. Target spec
- Size: body ~150 mm wide x 170 mm tall incl. fur; sits on a 160 mm dia x 40 mm fur-covered base puck.
  Overall ~210 mm tall. Desk-friendly.
- Look: cream long-ish pile faux fur (15–20 mm pile), 2 black domed eyes (12–14 mm), pink cheek patches,
  tiny stitched smile, two stubby arms, two stubby static feet nubs on the base.
- Motion DOF (5 total):
  1. Yaw (turn to face you)  ±110°
  2. Pitch (nod / lean forward-back)  −15° / +25°
  3. Roll (head-cock side tilt)  ±15°
  4. Left arm flap 0–90°
  5. Right arm flap 0–90°
- Other outputs: pink cheek LED glow, speaker (chirps / TTS), optional idle "breathing".
- Inputs: 2-mic array (sound direction), camera in one eye (face detection), capacitive touch (petting),
  servo load sensing (pushed / hugged).
- Power: tethered USB-C 5 V 3 A (battery is a later option).
- Brain: Raspberry Pi Zero 2 W (or Pi 4/5 if you want ROS 2 + vision on-board). Robot "cloud-brained" via your
  own server for LLM/voice.

## 2. Architecture: static lower body + moving upper body
Split the bean at ~1/3 height.
- **Lower body ("haunch", static):** printed puck containing Pi, power, speaker, mic array, ballast,
  the yaw servo and the pitch/roll gimbal. Covered in matching fur so it reads as the bean's bottom.
- **Upper body ("torso/head", moving):** printed ribbed cage on a spine plate driven by the gimbal.
  Carries eyes, cheeks, arm servos, touch pads. Fur skin hems over the lower body with ~15 mm overlap
  so the waist crease is hidden by pile.

Why: keeps all heavy things (Pi, speaker, ballast, 3 body servos) low and static → low CoM, no cable fatigue
for most wiring, only 2 arm servos + eye camera + touch + LEDs cross the moving joint.

## 3. Kinematic chain (bottom to top)
```
[Base plate + ballast]
  └─ Yaw servo (vertical axis) → printed lazy-susan ring (6 mm BBs or 6806 thin-section bearing) carries
     the off-axis load so the servo shaft only sees torque
       └─ Yaw platform
            └─ Pitch servo (horizontal axis, left-right) → U-bracket
                 └─ Roll servo (horizontal axis, front-back) mounted inside U-bracket → spine plate
                      └─ Upper-body cage (ribbed ellipsoid shell, 2 halves)
                           ├─ L arm servo (micro) → printed arm bone inside plush arm
                           ├─ R arm servo (micro) → printed arm bone
                           ├─ Eye camera + dummy eye (safety-eye style, washer locks skin to cage)
                           ├─ Cheek LEDs behind pink minky patches
                           └─ Touch pads (conductive fabric) on inside of skin crown & back
```
Pivot center of pitch/roll is ~55 mm above the table, at the "waist". A 25° lean moves the crown ~60 mm.

### Torque sanity check
Moving upper body mass estimate: cage 100 g + 2 micro servos 36 g + batting/fur 80 g + eyes/cam/wires 40 g ≈ 260 g.
CoM ~70 mm above pitch pivot. Static gravity torque at 25°: 0.26·9.81·0.07·sin25° ≈ 0.075 N·m (0.77 kg·cm).
Add 3x for dynamics/friction → ~0.25 N·m. Any 0.5 N·m-class servo is fine; a 25 kg·cm servo is overkill but harmless.

### Servo choice
Primary recommendation: **Dynamixel XL330-M288-T** for all 5 joints (5 V, 0.52 N·m, 18 g, 20x34x26 mm, ~$24 ea).
- one daisy-chained TTL bus, one 5 V rail shared with the Pi
- quiet, position+velocity+current feedback, "current-based position" mode = compliant joints (robot yields
  when petted/pushed, and you can *sense* touch from load) — a huge social-robot win
- ROS 2 / Dynamixel SDK / Python support
Controller: OpenRB-150 (~$25) or U2D2, or a 74LVC2G241 half-duplex buffer on the Pi UART.

Budget alternative: Feetech STS3215 (7.4 V version) x3 for body + 2x MG90S for arms via Pi PWM/PCA9685.
Cheapest: MG996R x3 + MG90S x2 + PCA9685 — works but hobby PWM servos hum/jitter at idle; use "detach at rest".

## 4. Designing the inner shell to fit the plush
### Option A (prototype 0): gut a stuffed animal
Find a cream bean/egg-shaped plush ~7–8" (Squishmallow 8", chonky seal, egg plush). Open the bottom seam,
remove stuffing, measure interior. Print cage sized to interior minus 8–12 mm radial gap. Insert cage halves
through the bottom slit, snap together, re-stuff the gap with original poly-fil. Good for validating
proportions and motion in a weekend; fur type/colour may not be right.

### Option B (final): sew a custom fur skin from the cage
- Model the upper body in CAD as an ellipsoid (e.g. 125 W x 125 D x 120 H mm visible above waist).
- Skin = cage + 10 mm batting + fur backing. Generate a 6-gore pattern (like a beach ball) from the ellipsoid
  circumference; add 6 mm seam allowance; pile direction downward.
- Features: 2 eye holes reinforced with buttonhole stitch; pink minky cheek circles (25 mm) appliquéd;
  smile = 3 stitches of black embroidery floss; arm tubes sewn as separate gores with open shoulder.
- Bottom: elastic channel + 3 snaps to the cage lip; hem overlaps the static fur puck.
- Anchoring: safety-eye posts pass through fur and cage front, washer on the inside → face stays aligned.
- Removable for washing/repairs (snaps + eyes pull off).

### Cage design rules
- Two halves (front/back) printed in PETG, 2.4 mm ribs, 4–5 longitudinal ribs + 3 hoops; ~100 g.
- Flat spine plate at the bottom with 4x M3 to roll-servo horn; channel for cables.
- Shoulder bosses at ~65% height, 35° from front, taking the micro servo body; horn exits via a 22 mm slot.
- Front face plate (solid area 60x40 mm) for eyes/camera/cheek LEDs so they don't sag into fur.
- Bottom aperture larger than gimbal swing envelope (+5 mm) at max pitch/roll.
- Wrap cage in 10 mm quilt batting (spray adhesive) → squishy feel, hides ribs.

## 5. Static base (lower body) design
- 160 mm dia x 40 mm puck, printed in two parts (tray + lid ring). ~300 g steel ballast (washers) glued in.
- Lid carries yaw servo & lazy-susan ring; vent slots on underside; rubber feet.
- Houses Pi Zero 2 W + ReSpeaker 2-Mic HAT (mics, speaker amp), 28 mm 3 W speaker firing out the front
  through a fur-covered grille, USB-C power in at the back.
- Fur sleeve glued/snapped around the puck sides; two small stuffed feet nubs stitched on the front.
- Cables to upper body: 1 XL330 bus (3 wires) + camera FFC/USB + 4-wire touch/LED harness, routed around
  the gimbal in a service loop sized for full range.

## 6. Electronics
- Pi Zero 2 W (or Pi 5 for on-board vision). 5 V 3 A USB-C PD-less supply.
- Dynamixel bus: 5 V direct from supply (not through Pi), ~1 A peak budget for 5 servos.
- ReSpeaker 2-Mic HAT: sound direction (2-mic TDOA) + speaker out.
- Camera: Pi Camera Module 3 (wide) behind the left eye; a 10 mm black trim ring = the "eye".
- Touch: MPR121 + conductive fabric pads on skin crown, back, belly (petting detection).
- Cheeks: 2 pink LEDs (or 2 WS2812) behind 25 mm pink minky circles.
- Optional IMU (not needed; servo encoders know pose).

## 7. Software / behaviour (brief)
- Layers: idle (slow breathing pitch ±2°, occasional head-cock, arm micro-twitch), attention (yaw to sound
  DOA, then face-track with camera), reaction (petting → lean into hand + cheek glow + chirp;
  push → yield via compliance), speech (bob on syllables).
- ROS 2 nodes: dynamixel driver, audio DOA, face tracker, behaviour tree, cloud LLM bridge.
- Safety: software joint limits, velocity caps, torque limits; no pinch points reachable through fur.

## 8. Build phases
P0 (weekend 1): print cage + puck mock, gut plush, fit; hand-pose it for look checks.
P1: yaw+pitch+roll stack, XL330s, Pi; scripted gestures; tune ranges.
P2: arms, eyes, cheeks, speaker, mics; first behaviours.
P3: custom fur skin; batting; hide the waist seam; feet.
P4: voice/LLM, touch, polish, idle life.

## 9. BOM (primary path, approx.)
| Item | Qty | Est. |
|---|---|---|
| Dynamixel XL330-M288-T | 5 | $120 |
| OpenRB-150 or U2D2 | 1 | $25–32 |
| Raspberry Pi Zero 2 W | 1 | $15 |
| ReSpeaker 2-Mic HAT | 1 | $12 |
| Pi Camera Module 3 wide | 1 | $35 |
| 28 mm 3 W speaker | 1 | $5 |
| MPR121 breakout + conductive fabric | 1 | $12 |
| LEDs, wire, M2/M3 hardware, bearing/BBs | — | $15 |
| 5 V 3 A USB-C supply | 1 | $10 |
| Faux fur 1/2 yd cream + pink minky scrap + 12 mm safety eyes + batting | — | $25 |
| PETG filament | ~300 g | $8 |
| Steel washers ballast | ~300 g | $5 |
| **Total** | | **~$290** (budget path ~$150) |

## 10. Known risks
- Fur fibres into servo gears / joints → fabric gaiters, keep servo horns inside cage.
- Servo noise at idle → bus servos + torque-off / low-gain idle.
- Heat inside fur → Pi and speaker in vented base; servos low duty.
- Tip-over → ballast + base dia ≥ body dia; limit pitch forward.
- Skin bunching at waist → elastic hem + overlap + pile length ≥ 15 mm.
- Cable fatigue at gimbal → silicone wire, service loop, limited yaw.
