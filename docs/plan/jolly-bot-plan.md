# "Jolly-bot" — tabletop fluffy social robot (plan v6 — final, after critic rounds 1–5)

Changelog v5→v6 (first-time-builder walkthrough): one height datum (h above the table) everywhere; igus plain bushing
(24 mm) instead of a ball bushing so the short shaft cannot jam; pinned 5×5 mm steel U-joint coupler specified;
hall-sensor yaw homing replaces the hard stop (no room for a stop pin inside the belt sweep); bearing mounting
defined (inner race on a tray boss with a clamp ring, outer race in a puck pocket); Operating Mode 5 named; 136T belt;
envelope reconciled to Ø160 at the waist (skirt over sleeve over the Ø128 puck); shoulder horn extension instead of a
widened shell; no ROS on the Pi (plain Python + zenoh/rosbridge to the laptop); mic ports moved below the skirt hem
with acoustic tubes; Pi header/standoffs; bring-up cheat sheet, three early tests and an MVP ordering added.

Changelog v4→v5 (character/mock critique): shoulders lowered to h 110 with a 15–20° downward arm axis (they sat at eye
height and read as ears); crown rounded to R 62–65 and body ≥Ø146 at the eye line; two front foot nubs on the sleeve
hem made official; skirt lengthened to h 33 and the puck sleeve raised to h 82 so a 28° lean never exposes the mesh
tube (needs ≈3 cm of extra skirt length, not 1–2); gore width corrected to ≈80 mm (π·76/3); cheeks feathered, smile
2 mm asymmetric; minky face panel is the baseline; sleep posture clarified (no eyelids: turn away + catchlights off).

## 0. Reference: Jolly (Meta Muse mascot, designed by Alex Cornell)
Cream/ivory dense plush fur, round egg/bean body (press compares it to Labubu, a Fall Guys bean, the Doctor Who
Adipose, a Teletubby), beady black eyes, soft pink cheeks, tiny upward smile, blank-but-pleasant face, stubby limbs,
no neck. In the Muse app it animates whole-body (e.g. typing) to show agent status; a plush version appears in ads.
Same gestalt as Keepon: **posture-driven expression, static face, one soft blob**.

## 1. Target spec (v4 numbers)
| | |
|---|---|
| Envelope | one bean: Ø148 at the bottom (h 12), widest Ø160 at h 60–82 (puck + sleeve + skirt), ≥Ø146 at the eye line, crown R 62–65 at h 198; sits 10 mm off the table |
| Static part | floor disc Ø130 × 14 mm, hidden under the puck's fur sleeve; reads as a shadow gap |
| Yaw | whole bean, ±180° (sleep = turn away); homed on boot with a hall sensor |
| Tilt | pivot at h≈90 (47 % of height): pitch −25° up / +15° down, roll ±18°, combined ≤28°, heave ±6 mm |
| Arms | 2 fabric-hinged paddles at h 110 (well below the eyes), axis 15–20° downward, 40 × 25 mm stubs, 0–45° normal, 90° "celebrate", torque-off at a 0° rest stop |
| Face | 2 glossy black domes 10–11 mm, interocular 50 mm, eye line h 123 (62 %), smile 20 mm wide 25 mm below with 2 mm asymmetry, dusty-pink cheeks Ø30 feathered 10 mm, 8 mm below / 12 mm outboard of the eyes |
| Fur | 8–12 mm high-density plush, warm ivory; face ellipse 80×60 = matching minky panel (shearing is the risky alternative); two Ø28 × 14 mm foot nubs on the sleeve hem at ±25° off front |
| Sensors | 2-mic HAT via acoustic tubes to ports at h 25 (onset + coarse angle), 720p UVC camera as the robot's-left pupil, MPR121 (4 pads), servo load, yaw hall sensor |
| Outputs | 6× Dynamixel XL330-M288-T, 2 cheek LEDs + 2 eye catchlights, 28 mm speaker (~1 W) |
| Power | 12 V 5 A brick, magnetic breakaway at the floor disc → 5 V 5.5 A servo rail + 5.1 V Pi rail |
| Brain | Pi Zero 2 W (plain Python, no ROS): 100 Hz animation engine, reflexes, audio, camera stream. ROS 2 host (laptop) over zenoh/rosbridge: perception, behaviour, LLM |
| Mass | ≈1.5 kg: floor disc ≈0.55 kg (450 g steel), puck ≈0.65 kg, head (moving) ≈0.28 kg; ≈0.95 kg rides on the bearing |

## 2. Architecture (heights above table, mm)
```
h 0–14   FLOOR DISC (static): printed tray Ø130, 2× steel discs Ø110×3 (≈450 g), 4 rubber feet at r 50,
         6810ZZ thin-section bearing (50×65×7): inner race clamped on a Ø50 tray boss by a clamp ring (h 7–14);
         static 120T GT2 ring (PD 76) at r 38–40 around it; Ø5 magnet flush at r 35 (yaw home);
         12 V magnetic-breakaway jack at the rear, 3 UHMWPE glide pads at r 60 against bearing rock
h 14–70  PUCK (rotates): PETG bowl Ø112 at the bottom → Ø128 above h 20; outer bearing race in a Ø65 pocket with a
         lip under the puck floor; hall sensor (A3144) on the floor underside at r 35 facing the magnet;
         2-wire 22 AWG clock spring in the Ø50 bore (2 turns, so a full homing search cannot over-twist it)
         lower storey h 14–48: 3 tilt XL330 standing (horn axis tangential at r 50, h 37), yaw XL330 horn-down with
           30T GT2 pulley through a floor slot at r 53, D36V50F5 + D24V22F5 bucks in the gaps
         upper storey h 50–70: Pi Zero 2 W (soldered 2×20 header, 11 mm standoffs) + ReSpeaker 2-Mic HAT, 17 mm
           stack lying tangential between two pushrods, OTG hub cable off the board edge; OpenRB-150 in gap 2;
           28 mm speaker firing forward through the front wall in gap 3; mic acoustic tubes to two 2 mm ports at h 25
h 37     horn balls (arm r 20 pointing inward) at r 30 → three M2 pushrods, 60 mm
h 17–80  8 mm hardened shaft at centre (63 mm); igus RJ4JP-01-08 plain bushing (8×15×24) in a printed carrier
         at h 62–86 (±6 heave) — a plain bushing cannot shed balls when the shaft end sits inside it;
         TPU bumpers for the −64° park
h ≈90    PIVOT: 5×5 mm steel universal-joint coupler on top of the carrier: lower bore pinned to a Ø5 steel pin
         pressed into the carrier, upper bore pinned to a Ø5 pin on the plate underside; cross at h 90
h ≈98    SPINE PLATE Ø76: three 8 mm ears with tangential M2 ball studs at r 30; = neck ring of the head shell
h 95–198 HEAD SHELL (two PETG half-shells, 1.6 mm): necks to Ø76 at h 95, Ø108 at h 100–130, crown; face plate,
         shoulder pockets with 20 mm horn extensions through the foam, arm servos, camera, MPR121, LEDs;
         10 mm open-cell foam jacket
h 33–95  SOFT WAIST: fur skirt (65 mm long) hangs from the neck over the puck's own fur sleeve ("dress over
         petticoat"); power-mesh tube inside keeps fur off the pushrods
h 10–82  PUCK SLEEVE: fur on the lower puck (h 10–33) and a smooth "petticoat" fabric (no pile) from h 33 to a soft
         foam collar at h 82, so the skirt does not double the fur; rolls down over the floor disc with 3 mm
         clearance. Skirt over sleeve over the Ø128 puck is what makes the waist the widest point (Ø160)
```
Why this split: the yaw joint carries only 12 V (2 wires); all six servos sit on one bus inside the rotating body;
the puck's 1.1 kg never tilts, so the tilt servos only move the ~280 g head.

## 3. Mechanisms
### 3.1 Yaw (whole bean)
- 6810ZZ thin-section bearing (Ø50 bore, Ø65 OD, 7 mm): it has no bolt holes, so the inner race is clamped onto a
  Ø50 boss on the tray by a printed clamp ring, and the outer race sits in a Ø65 pocket under the puck floor against a
  lip. Never clamp across both races. Print seat coupons first (start at Ø49.8 / Ø65.2 in PETG and tune). Three
  UHMWPE pads at r 60 take rocking from the ≈0.95 kg that rides on the bearing.
- Drive: static 120T GT2 ring (PD 76.4 mm) printed into the floor tray at r 38–40; yaw XL330 in the puck, horn down,
  30T GT2 pulley (PD 19.1) through a floor slot at r≈53; closed GT2 belt 136T (272 mm) — a 130T belt would pull the
  pulley into the ring — 4:1, ≈113° wrap. Print the ring and the pulley slot alone first and spin it by hand. Alternative with
  zero printed teeth: open belt clamped at two points 60° apart on a smooth ring (travel is finite anyway).
- XL330 in extended-position (current-based) mode: ±180° output = ±720° input. Turn count is lost at power-off, and
  there is no room for a stop pin inside the pulley's sweep, so: A3144 hall sensor on the puck floor underside at r 35,
  Ø5 magnet flush in the tray at r 35. On boot, rotate slowly (≤60°/s) until the hall triggers, then set the
  Homing Offset (addr 20) or a software offset; soft-limit ±180° after that.
- Only 12 V + GND cross the joint: 2× 22 AWG silicone, 2 turns in the Ø50 bore so a worst-case homing search
  (one full turn) plus ±0.5 turn of travel never binds.
- Torque: I ≈ 0.0025 kg·m²; 90° in 0.3 s → 0.23 N·m at the puck → 0.06 N·m at the servo. Velocity-profile it.

### 3.2 Tilt + heave: 3-RSS parallel platform on a P-U centre
- Three XL330 standing 34-high at 120°, horn axis tangential at r 50, h 37, all in Operating Mode 5 (current-based
  position) — Current Limit and goal-current yielding are ignored in plain position mode. Printed horn arm (modelled
  against the XL330-M288-T STEP from the Robotis e-manual; verify the horn hole pattern, M2 screws ≤0.1 N·m) carries an
  Align T-Rex 450 linkage ball (4.75 mm, M2) at r_h = 20 mm, pointing inward → ball at r 30.
- Pushrods: Align 450 plastic ball links on M2 all-thread, 60 mm centre-to-centre (cut 2×45 mm stock, adjust at assembly). Horn sweep ±64°
  moves the ball z ±18 mm and radially 30→41 mm → rod lean ≤ 11°; Cardan phase and roll add ≈4° → within ±25° sockets
  **only because the plate ball studs are horizontal (tangential) on 8 mm vertical ears**, never vertical in a flat plate.
- Centre: 8 mm hardened chromed shaft (63 mm, h 17–80) fixed to the puck floor; igus Drylin RJ4JP-01-08 plain bushing
  (8×15×24) in a printed carrier (bore from a 14.9/15.0/15.1 mm test coupon) — a ball bushing would drop balls when
  the short shaft end sits inside it; on top a BOUGHT 5×5 mm steel universal-joint coupler (tighter than RC driveshaft
  yokes), both bores pinned to Ø5 steel pins pressed into the carrier top and the plate underside, cross at h 90. Grübler: 9 bodies, 3R + 6S + P + U → M = 6 − 3 passive rod spins = **3 (pitch, roll, heave), yaw blocked**.
  A ball joint instead would leave yaw free — don't.
- Align the lower yoke with the pitch axis so pure pitch has no Cardan coupling; ≈4° apparent head yaw at combined
  extremes — compensate with the yaw servo or ignore.
- No gravity spring: there is no room under a 45 mm bearing at low heave, and the saving is only ≈50 mA/servo.
  Holding ≈0.3 A total. For torque-off sleep, park the horns at −64° on TPU bumpers.
- IK: exact sphere–circle loop closure (5 lines): for each servo, plate ball p_i = R(θp,θr)·b_i + [0,0,h]; find horn
  angle φ_i such that |p_i − horn_i(φ_i)| = 60 mm; clamp |z_i| ≤ 18. Small-angle version is ≈2° off at extremes.
- Load path: head bending moments go into the pushrods (axial), the U-joint takes shear + yaw, the slider takes radial.

### 3.3 Mass, torque, tip-over
Head (moving) ≈ 280 g: shells 90 + arm servos 36 + foam/skin share 70 + camera/boards/wires 40 + arms 35 + ears/plate 10.
CoM ≈ 45 mm above the pivot (h≈135). Static at 28°: 0.28·9.81·0.045·sin28 ≈ 0.06 N·m. Snappy nod 25° in 0.15 s
(α≈100 rad/s², I≈0.0009) adds ≈0.09 → **≈0.15 N·m at the plate**, through 1.5:1 over 2–3 rods → ≤0.07 N·m/servo
(13 % of XL330 stall). Yaw ≤0.06 N·m. Margin ≥4× everywhere.
Tip-over: 1.5 kg, feet at r 50 → crown push ≈1.5·9.81·0.05/0.2 ≈ 3.7 N; nod reaction 0.15 vs righting 0.74 N·m (5×).
Down-pitch capped at 15°. Cord yank is the real tip risk → magnetic breakaway on the 12 V jack.

### 3.4 Collision envelope
Neck ring r 38 sits 5 mm above the pivot; at 28° combined it dips 38·sin28 ≈ 18 mm → lid must be ≥20 mm below the
pivot: lid h 70, pivot h 90 ✓. The soft skirt may brush the puck sleeve — fabric on fabric, harmless.
Cage lid slots for the pushrods: 15×8 mm. Rods are ≥52 mm apart and clear the carrier (r 12) by >15 mm.

### 3.5 Arms
Horn flush under the skin; 45×20×3 mm printed paddle stitched inside the arm gore and bolted to the horn with 2× M2
through the fabric after the skin is on (the fabric is the hinge). Arm 40 mm long, 25 mm thick, tapered, foam core on
1.5 mm wire so the tip lags. 0–45° normal (15° forward sweep), 90° celebrate. Rest stop at 0° → torque-off between
gestures (thermal). Minky shoulder gaiter around the horn.

### 3.6 Head shell (printed)
- Two half-shells (front/back), 1.6 mm wall, 2 perimeters, lightening windows; ≈90 g; ≈4 h each; joined with 6× M3
  into heat-set inserts (M3×4×5). Neck ring Ø76 bolts to the spine plate (4× M3).
- Face plate is part of the front shell: 80×60 mm, 3 mm; two 16 mm eye wells with M4 heat-set inserts; 720p UVC
  board camera registers behind the left well (4 mm pupil hole in that dome), tilted 15–20° up; two 20 mm LED diffuser
  pockets (1.5 mm white PETG dome + 1 mm foam); bosses for the MPR121.
- Shoulder pockets at h 110 (13 mm below the eye line — arms at eye height read as ears), 70° from front, axis tilted
  15–20° downward; the shell is NOT widened (that would push the envelope to Ø164): a 20 mm printed horn extension
  passes through a slot in the foam to the arm paddle; 3 mm walls, 2 mm TPU pads under the servos.
- Thermal: 3–4 cm² unfoamed chin vent into the waist, 1 cm² mesh port at the crown whorl; camera copper-taped to the
  face plate; arms torque-off at rest. Expect ≈45–55 °C interior; leave the XL330 temperature limit at 70 °C, poll it.
- Layer stack outward from the shell: 2 mm air, 10 mm open-cell upholstery foam (not batting — it mats), fur backing,
  8–12 mm pile. The printed shell is therefore the skin's inner envelope minus 22 mm (Ø108 shell under Ø152 skin at
  the shoulders).

## 4. Skin
### 4.1 P0: gut a plush (proportion + motion only)
8" Squishmallow (~Ø160×200) or Jellycat Bashful-type egg in cream. Seam-rip the hand-laddered closing seam to 12–15 cm,
pull the fill, measure the interior at 3 heights with a cardboard gauge, scale the shells so shell + foam ≈ interior,
insert, screw together inside, close with hook-and-loop. The velour surface misrepresents the eye read — ignore the face.
### 4.2 Final: one-piece 6-gore skin
- Pattern from a 10-line script: for h in 1 mm steps from crown to hem, gore half-width = π·r(h)/6 plotted against
  meridian arc length → 1:1 PDF. For this envelope: gore ≈ 84 mm wide (π·80/3) × ≈225 mm long, widest ≈ 65 % down
  from the crown; add notches at the eye line and the waist. (Blender UV unwrap or a
  masking-tape wrap of the P0 mock also work; a CAD flatten won't — the surface isn't developable.)
- 8 mm seam allowance, 2–4 % negative ease for the knit backing, stretch running around the body, Ø25 crown cap.
  Face centred on one gore (both eyes fit: gore is ≈76 mm wide at the eye line); pile radiates from the crown whorl.
- Closure: 20–25 cm invisible zipper centre-back from hem to h≈130. Sequence: skin on → zip → screw M4 eyes in from
  outside through 4 mm holes → bolt arm paddles through the fabric → snap the hem to the puck sleeve.
- Waist: at 28° combined tilt the rear skirt anchor (r≈70) rises ≈33 mm, so the skirt must reach h 33 (65 mm long)
  and the sleeve collar must reach h 82; give the skirt ≈3 cm of gathered extra length and no foam. The front fold
  reads as a belly crease. Power-mesh tube cut 10 % short with elastic at both ends (or three TPU boots) keeps fur
  out of the pushrods.
- Eyes: 10–11 mm glossy black high-dome, M4 threaded shank; the robot's-left dome (viewer's right) has the camera pupil
  — size the hole to the lens front element (4 mm only if the lens is that small; a 6–8 mm module needs a 6–8 mm hole
  or the dome itself becomes the lens cover); polish both so the
  highlight matches. 0603 white catchlight LED behind each dome, off-centre.
- Face panel: 80×60 minky ellipse in matching ivory (baseline) or pile sheared to 3–4 mm with pet clippers, feathered
  over 10 mm (risk: a hard edge). Smile: 2–3 mm satin stitch, 20 mm wide, R≈25 curve with ~2 mm asymmetry so it is
  not a drawn arc. Cheeks: Ø30 dusty-pink minky under the pile, feathered 10 mm, appliquéd AFTER seaming (they
  straddle the gore seam).
- Touch pads: ≥40×60 mm conductive fabric sewn inside the skin at crown-L, crown-R, back, belly; metal sew-on snaps
  are the connector to the MPR121 leads.
- Sewing: razor-cut from the backing, comb pile inward, 3 mm zigzag or walking foot, brush seams out.

## 5. Electronics
### 5.1 Power
12 V 5 A brick → magnetic breakaway jack on the floor disc → 2-wire clock spring → puck.
Rail A: D36V50F5 (5 V 5.5 A) → OpenRB-150 power terminal, 2200 µF low-ESR at the bus head, 20 AWG.
Rail B: D24V22F5 (5.0 V, fixed) → Pi pads. Common ground, star at the bucks. OpenRB LOGIC powered from USB so a rail-A fold
never resets ttyACM0. XL330 Current Limit 600 mA each (6 × 0.6 = 3.6 A worst case < 5.5 A). Pi on overlayfs.
Bus wiring: ≤2 servos per OpenRB port (4 ports) — the 1.25 mm pigtails are ~1 A/pin.
### 5.2 Compute split
- OpenRB-150 (SAMD51) runs the Dynamixel protocol itself: receives 6×int16 goals at 100 Hz over CDC, sync-writes,
  sync-reads pos/current/temp (~20 % bus utilisation at 1 Mbaud, Return Delay 0). No byte-passthrough.
- Pi Zero 2 W: NO ROS on the Pi (ROS 2 is not an apt install on Raspberry Pi OS and is a weekend sink on 512 MB).
  One plain-Python process: animation engine (layers + exact IK + min-jerk) at 100 Hz, reflexes, GCC-PHAT onset/angle,
  MPR121/LEDs, audio out; ustreamer for MJPEG from a camera that emits MJPEG natively (720p). Talk to the laptop over
  zenoh (or rosbridge/UDP JSON); the laptop side is ROS 2. USB hub on the OTG port: OpenRB + camera.
- Host (laptop, ROS 2): face tracker, sound fusion, behaviour tree, chirp synth / LLM bridge, animation authoring.
  Sends intents only (`/anim/target` pose+duration+easing ≤10 Hz, `/anim/clip`), bridged to the Pi by zenoh/rosbridge.
  In P1 the laptop talks to the OpenRB directly over USB — bring the Pi in afterwards. Watchdog 500 ms → local idle;
  5 s → drowsy. chrony time sync so the Pi plays ahead.
### 5.3 Sensing & outputs
- Audio: ReSpeaker 2-Mic HAT on the in-kernel `wm8960-soundcard` overlay (check it exists in /boot/firmware/overlays;
  else the HinTak seeed-voicecard build), on grommets. The lid sits under the collar and the skirt (two fur layers), so
  the mics get 2 mm-ID silicone acoustic tubes to two 2 mm ports 65 mm apart in the puck's lower front wall at h 25,
  below the skirt hem, with mesh and gaskets, pile trimmed to 3 mm there; gate onset detection while any
  servo moves; 2-mic angle is a ±20° frontal cue with front/back ambiguity — confirm with the camera.
- Camera: 720p UVC board, 4× 28 AWG silicone, lens flush in the left dome, pile ≤3 mm within 12 mm.
- Touch: MPR121 (I2C-1 at 0x5A, ADDR→GND, 3.3 V; the WM8960 codec sits at 0x1A on the same bus; the breakout's own
  10 kΩ pull-ups in parallel with the Pi's 1.8 kΩ are fine) in the head; IRQ on GPIO 22/23/27 (free with the HAT); 4 electrodes on ELE0–3, 1 kΩ series
  each, anti-static spray, GND plane (aluminium tape ~150 cm² on the puck floor); ELE8–11 drive the 2 cheek LEDs +
  2 catchlights via raw GPIO register writes (0x73–0x7A; the Adafruit library does not expose them); ELE4–7 spare. Mask touch only while a joint moves >30°/s; auto-baseline + rate filter.
- Harness puck→head: 3 (bus to arm servos) + 4 (I2C) + 4 (USB cam) = 11 wires, one JST-PH at the neck ring, single-plane
  service loop at the back, ≥25 mm bend radius, sized at both extremes.

## 6. Behaviour, animation, interaction
### 6.1 Vocabulary
- Awake idle: Perlin breathing pitch ±2° + heave ±3 mm at 0.25–0.3 Hz; "notice" glances every 20–60 s; head-cock
  (roll 15–18° + pitch back 4°, 250 ms ease-in, hold ≥1.5 s); arm micro-lifts. Never still >2 s while awake.
- Blink-equivalents: catchlights dim 120 ms every 3–6 s (Poisson), sometimes with a 3 mm heave dip.
- Attention: onset (+12 dB in 200 ms, 2 s refractory) → 120 ms arm micro-lift + cheek flicker, then 200 ms yaw saccade
  with overshoot, 300 ms settle; re-estimate after turning.
- Gaze: saccade-and-fixate (dead-band ±3°, off-centre >150 ms → 200 ms saccade, hold), project with the COMMANDED pose,
  gaze aversion every 4–8 s for 300–600 ms.
- Sound: non-verbal first — 20–30 parametric chirps (rising = question, falling = sad, trill = joy, double = ack),
  800 Hz–4 kHz. LLM speech = Animalese-style gibberish; heave bob from the audio envelope (20 ms frames, 100 ms ahead).
- Reactions: stroke → lean to that side (roll 10°, pitch back 5°, 400 ms) + cheeks + trill; tap → heave hop;
  push (error >5° for >80 ms) → goal current 150 mA, follow, spring back 600 ms with ±4° roll shake-off;
  celebrate → arms 90° + 3 bounces.
- Lifecycle: awake (300 mA idle limit) → 3 min → drowsy (0.12 Hz, dim, pitch −8°) → 10 min → sleep: yaw 180° to face
  away, pitch down, catchlights off, park horns on bumpers, torque off, camera stream stopped (no eyelids exist). Wake ramp 1.5 s.
### 6.2 Engine (Pi, 100 Hz)
final = base + idle·(1 − w_react) + reactive + clip; clips cross-fade 150–250 ms and duck idle to 30 %; exact IK →
clamp → min-jerk (≥300 ms except saccades) → 6×int16 to OpenRB. Caps: joint, ≤300°/s, current.
### 6.3 Latency budget
touch → motion ≤100 ms (local) · onset → yaw start 200–300 ms · face → gaze ≤500 ms · audio/motion skew <40 ms.
### 6.4 Privacy
Sleep = physically turned away + stream off; "listening" cheek pattern whenever audio leaves the device; wake-word
gating on the Pi before any LLM; LAN-only, nothing persisted; hold the crown 2 s → mute toggle with a distinct chirp.

## 7. Build phases
P0 (weekend 1): print shell mock + puck bowl, gut the Squishmallow, hand-pose; check eye line / proportions.
P1: tilt platform on the bench using the P0 puck bowl as the fixture — 3 XL330, shaft, igus bushing, pinned U-joint,
    60 mm rods, ears; exact IK; 100 Hz engine on the LAPTOP talking to the OpenRB over USB (Pi comes in P3).
P2: floor disc + 6810 bearing (clamp ring / pocket) + 136T GT2 belt yaw + hall homing; puck two-storey packaging;
    two rails; clock spring; magnetic jack.
P3: head shells, face plate, M4 eyes + camera pupil, LEDs, MPR121, arm servos + paddles; thermal vents.
P4: gore script → one-piece skin, foam jacket, skirt + mesh tube, zipper, hem snaps, feet.
P5: chirp lexicon, idle life, onset/gaze, touch reactions, lifecycle + privacy, LLM bridge last.

## 8. BOM (primary path, approx.)
| Item | Qty | Est. |
|---|---|---|
| Dynamixel XL330-M288-T (yaw, 3 tilt, 2 arms) | 6 | $144 |
| OpenRB-150 | 1 | $25 |
| Raspberry Pi Zero 2 W + micro-USB hub | 1 | $25 |
| ReSpeaker 2-Mic HAT + 28 mm speaker | 1 | $17 |
| 720p UVC board camera (native MJPEG) | 1 | $20 |
| MPR121 + conductive fabric + LEDs + snaps | 1 | $22 |
| 12 V 5 A brick + magnetic breakaway + D36V50F5 + D24V22F5 | 1 | $50 |
| 6810ZZ bearing, 5×5 steel U-joint coupler, igus RJ4JP-01-08, 8 mm hardened shaft, A3144 + magnet, UHMWPE pads | — | $24 |
| GT2 belt 136T (272 mm) + 30T pulley, T-Rex 450 balls/links + M2 all-thread, heat-set inserts, M2/M3, TPU | — | $28 |
| Fur ½ yd + minky + M4-shank dome eyes + 10 mm foam + power mesh + zipper | — | $40 |
| PETG ≈400 g | — | $10 |
| 2× steel discs Ø110×3 | — | $12 |
| **Total** | | **≈ $420** |
Budget path (~$240): Feetech STS3215 (7.4 V) ×4 for yaw/tilt + Waveshare bus board + a 7.4 V buck of its own, 2× MG90S
arms, same Pi. Expect hum and no current-based compliance.

## 9. Risks (open) and first-timer traps
- Fur in mechanism → mesh tube / TPU boots, gaiters, pile trimmed near horns.
- Head heat → vents, arm torque-off, low-power camera; monitor servo temperature.
- Yaw homing lost at power-off → hall-sensor homing routine on boot, 2-turn clock spring.
- Wi-Fi dropouts → engine + idle live on the Pi.
- Cord yank → magnetic breakaway; down-pitch cap 15°.
- Traps: XL330 default ID 1 @ 57600 (configure one at a time); horn screws ≤0.1 N·m; print bearing/slider seats from
  test coupons; size cable loops at both extremes; common ground between rails; screw (don't glue) ballast; never
  mount ball studs vertically; cut the shaft so it clears the U-joint cross; "left eye" means the robot's left.

## 10. Three early tests (each catches a build-killer before the head is printed)
1. **Platform binding / links popping** — on the P1 rig, command a 28° cone with ±6 mm heave and log Present Current.
   Any spike >300 mA, or a visible rod lean >15°, means the ears are not tangential or a servo axis is off: fix first.
2. **Skirt drag pulling the head back** — tape a strip of fur + foam from the bowl to the plate at the rear, repeat the
   cone, compare current. This decides the 3 cm skirt gather before any fabric is cut.
3. **Camera pupil vignetting** — tape the UVC camera behind a 4 mm hole in card 15 mm ahead of the lens. A black ring in
   the frame means the hole must be at least the lens front element (6–8 mm), or the dome becomes the lens cover.
Runner-up: print the GT2 ring and the pulley slot alone and spin the 136T belt by hand before building the floor.

## 11. MVP ordering (moving, furry, cute fastest; every interface kept)
1. P0 as written, with the P1 servo fixture printed into the puck bowl.
2. P1 tilt platform: 3 XL330 + OpenRB, laptop over USB, bench 5 V 5 A supply; Perlin breathing + head-cock only.
   Keep the h 90 pivot, 60 mm rods and Ø76 plate interface untouched.
3. Bolt the bowl to a plywood disc — skip yaw, floor disc, ballast, bearing, belt, clock spring, bucks and 12 V (P2
   later; interfaces unchanged).
4. Drop the gutted Squishmallow over it; glue cheeks and two 10 mm black cabochons; sew foam stub arms (no servos).
5. Then Pi + OpenRB (plain Python), catchlight LEDs on MPR121 GPIO, one crown touch pad, chirps from the laptop.
   Yaw, camera, mic HAT, real skin, arm servos and the LLM come last.

## 12. Bring-up cheat sheet
- **Servo IDs/baud:** connect ONE XL330 at a time to the OpenRB-150 running the `usb_to_dynamixel` example; in
  Dynamixel Wizard 2.0 scan at 57600, set ID (yaw 1, tilt 2–4, arms 5–6), Baud Rate (addr 8) = 3 → 1 Mbps,
  Return Delay (addr 9) = 0, Operating Mode (addr 11) = 5, Current Limit (addr 38) ≈ 600 mA. Repeat per servo.
- **OpenRB-150 firmware:** Arduino IDE with board URL
  `https://raw.githubusercontent.com/ROBOTIS-GIT/OpenRB-150/master/package_openrb_index.json`, library
  Dynamixel2Arduino, `Dynamixel2Arduino dxl(Serial1, -1)`; sync-write Goal Position (116) ×6 at 100 Hz from six int16
  received over USB CDC; sync-read Present Current (126), Position (132), Temperature (146). Confirm from the manual
  that the board's DC input accepts 5 V and that USB can feed logic independently of VIN before relying on it.
- **Pi:** Raspberry Pi OS Lite 64-bit; in config.txt `dtparam=i2c_arm=on`, `dtoverlay=wm8960-soundcard`,
  `dtparam=audio=off`; overlayfs read-only root once set up. Camera: `apt install ustreamer` then
  `ustreamer --device=/dev/video0 --format=MJPEG --resolution=1280x720 --desired-fps=30 --host=0.0.0.0 --port=8080`.
- **MPR121:** SDA GPIO2, SCL GPIO3, 3.3 V, ADDR→GND (0x5A), IRQ GPIO 22; electrodes ELE0–3 through 1 kΩ; LEDs on
  ELE8–11 via GPIO registers 0x73–0x7A.
- **Yaw home:** on boot rotate ≤60°/s until the A3144 goes low, write Homing Offset (addr 20) or store the offset,
  then soft-limit ±180°.
- **Parts to download:** XL330-M288-T STEP (horn arm), OpenRB-150 pinout, igus RJ4JP-01-08 and 6810 datasheets.
