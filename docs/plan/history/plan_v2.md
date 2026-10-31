# "Jolly-bot" — tabletop fluffy social robot (plan v2, after critic round 1)

Changelog v1→v2 (from aesthetic, mechanical and electrical critiques):
- Whole bean now yaws on a hidden floor ring (feet rotate with body; no twisted waist; one-piece skin).
- Serial pitch/roll gimbal replaced by a Keepon-style 3-pushrod parallel platform: pitch + roll + 10 mm heave (bob),
  all 3 tilt servos stay low in the puck, head no longer hangs off plastic servo horns, stack height drops.
- Head mass recomputed (~280 g), gravity-compensation spring added, torque re-done with dynamics.
- Power: 12 V brick → two 5 V rails (Pi / servos), common ground, 2200 µF at bus head, current limits on servos.
- Pi Zero 2 W becomes a thin client (streams camera+audio to your ROS 2 host); Pi 4B is the on-board-vision option.
- Camera: USB board camera on silicone wire as the "pupil" of a glossy dome, both eyes identical. No FFC across joints.
- Skin: single egg envelope 140 W × 190 H, 8–12 mm dense pile, sheared face panel, eyes 10–11 mm, 50 mm interocular,
  one-piece skin with a slack "bellows" band at the waist, Lycra under-tube keeps fur out of the mechanism.
- Arms: fabric-hinged paddles, 0–45° normal range, foam/wire tips; heave-based speech bob instead of pecking.
- Thermal/ESD/touch electrode/mic grounding fixes; MPR121 drives cheek LEDs; 11-wire harness, one connector.

## 0. Reference: Jolly (Meta Muse mascot)
Cream/ivory dense plush fur, round egg body (compared to Labubu, Fall Guys bean, Adipose, Teletubby), beady black
eyes, soft pink cheeks, tiny upward smile, blank-but-pleasant face, stubby limbs, no neck. Expression in the app comes
from whole-body animation (e.g. typing). Same gestalt as Keepon: posture-driven expression, static face.

## 1. Target spec
| | |
|---|---|
| Envelope | one egg: 140 W × 140 D × 190 H mm incl. fur; widest at 75–80 mm up; crown R≈55, bottom R≈70 tucked under |
| Static part | 12–15 mm dark floor disc (Ø150) under the bean — reads as a shadow |
| Yaw | whole bean, ±110° |
| Tilt | pitch −15°/+25°, roll ±15°, heave ±8 mm (combined tilt ≤ 29°) |
| Arms | 2 × fabric-hinged paddles, 0–45° normal, 90° "celebrate" |
| Face | 2 glossy black domes 10–11 mm, interocular 50 mm, eye line at 62% of height (~118 mm up), satin-stitch smile 20 mm wide ~25 mm below eye line, dusty-pink cheek glow 30 mm, centres 8 mm below / 12 mm outboard of eyes |
| Fur | 8–12 mm high-density plush (Jellycat-type), warm ivory, face ellipse 80×60 sheared to 3–4 mm or minky panel |
| Sensors | 2-mic array (coarse DOA), USB camera in one eye, MPR121 touch (crown, back, belly), servo load (push/hug) |
| Outputs | 6 servos, cheek LEDs, 1 W speaker |
| Power | tethered 12 V 5 A brick → 5 V servo rail + 5.1 V Pi rail |
| Brain | Pi Zero 2 W thin client + your ROS 2 host (laptop); Pi 4B 2 GB if you want vision on-board |

## 2. Architecture (bottom → top)
```
Table
└─ FLOOR DISC (static, Ø150 × 12–15 mm, dark): 3 mm steel plate (ballast ~360 g) + printed tray, 4 rubber feet at r≥70,
   yaw servo (XL330) with 20T pinion, 76 mm steel lazy-susan bearing, 12 V jack at rear
   └─ LOWER BODY "PUCK" (rotates, Ø~135 × 45 mm, printed PETG tray+lid): internal 60T ring gear on its floor (3:1),
      Pi Zero 2 W + ReSpeaker 2-Mic HAT, two bucks, OpenRB-150, 28 mm speaker (front), 3 tilt servos at 120°,
      8 mm steel post (centre) with LM8UU slider + gravity spring, ~200 g extra ballast low at rim
      └─ TILT PLATFORM: slider carrier → cross U-joint (4 mm shafts, 4× 684ZZ) → SPINE PLATE (4 mm PETG, 3 ball-link
         pushrod studs at r=30 mm, 120° apart)
         └─ HEAD CAGE (6 flat-printed T-ribs + 3 hoops, screwed; ~95 g): face plate 80×60, shoulder pockets,
            2 arm servos, MPR121 + LEDs, camera board, touch pads; 10 mm batting jacket
            └─ ONE-PIECE FUR SKIN crown→hem, slack band at waist, hem snapped to puck bottom edge
```
Waist crease sits at ~45 mm (≈24% of height) and is hidden by pile + bellows; it never twists because yaw moves everything.

## 3. Kinematics & mechanism detail
### 3.1 Yaw (whole bean)
- 76 mm (3") steel lazy-susan between floor tray and puck floor: cheap ($3–4), smooth, ~50 mm open centre.
- XL330 on the floor tray, off-axis, 20T printed pinion (module 1) driving a 60T internal ring gear printed into
  the puck floor; XL330 in extended-position mode (±330° input covers ±110° output). Backlash is tolerable for yaw.
- Only a 5-wire silicone ribbon crosses yaw, as a 1.5-turn "clock spring" in the bearing bore:
  12 V + GND (up to the puck) and the 3-wire Dynamixel bus (down to the yaw servo).
- Inertia: puck ~0.7 kg at r≈65 mm + head → I ≈ 0.004 kg·m². A 90° saccade in 0.3 s needs ~90 rad/s² →
  0.36 N·m at the ring → 0.12 N·m at the servo (3:1). OK for XL330 (0.52 N·m stall), set velocity profile.

### 3.2 Tilt + heave: 3-RPS-style parallel platform
- Three XL330 lying flat in the puck at 120°, horns (r_h = 18 mm) carrying M2 ball links; pushrods (2 mm steel or
  M2 threaded rod, ~45 mm) up to ball studs on the spine plate at r_p = 30 mm (ratio 1.67:1).
- Centre constraint: 8 mm steel post fixed to the puck floor; LM8UU linear bearing in a printed carrier (heave);
  on top a printed cross U-joint on two orthogonal 4 mm steel shafts in 684ZZ bearings → the U-joint carries all
  radial/bending load from the head and blocks yaw of the plate; servos only ever see pushrod axial loads.
- Ranges: heave ±8 mm (horn 26°), tilt 25° at r=30 → 12.7 mm (horn 45°); combined stays inside ±90° horn travel.
- Gravity compensation: compression spring on the post under the carrier, ~2.7 N at mid-stroke (head weight), so
  holding a pose costs ~0.1 A instead of 0.4 A; plus 5–8 mm forward CoM bias to preload one gear flank (less shiver).
- IK (small-angle, exact enough at ≤29°): for pushrod i at azimuth a_i = 90°, 210°, 330°:
  z_i = h + r_p·(θ_pitch·cos a_i + θ_roll·sin a_i); φ_i = asin(z_i / r_h). Two lines of Python.
- Why not the serial gimbal of v1: it hung ~360 g off two plastic XL330 horns in bending, put the roll servo in the
  head (heat, mass, cable), and gave no heave. The parallel platform fixes all four for one extra servo.
- Fallback (simpler, no bob): fixed U-joint + 2 pushrods at ±45°.

### 3.3 Mass & torque (recomputed)
Head: cage 95 + arm servos 36 + skin/batting share 70 + camera/MPR121/LEDs/wires 40 + arms 35 ≈ **280 g**,
CoM ≈ 70 mm above U-joint. Static at 29° combined: 0.28·9.81·0.07·sin29 ≈ 0.093 N·m. Snappy nod 25° in 0.15 s
(α≈100 rad/s², I≈0.0016) adds 0.16 N·m → **~0.25 N·m at the plate**, shared by 2–3 pushrods through 1.67:1 →
≤ 0.1 N·m per servo (20% of XL330 stall). Holding with spring: ~0.02 N·m. Comfortable; XC330-M288 is an upgrade,
not a need.

### 3.4 Tip-over
Total ≈ 1.25 kg (steel disc 360 g + puck ballast 200 g + parts); CoM ≈ 60 mm; feet at r = 70 mm, rubber μ≥0.6.
Push at the crown (190 mm) to tip ≈ 1.25·9.81·0.07/0.19 ≈ 4.5 N; nod reaction torque 0.25 N·m vs righting 0.86 N·m
→ 3.4× margin. Forward pitch limited to 25°.

### 3.5 Arms
- Horn sits flush under the skin (no bone through a slot). A 45×20×3 mm printed paddle is stitched to the inside of
  the arm gore; the fabric is the hinge. Arm: 35–40 mm long, 22–25 mm thick, tapered, foam core on 1.5 mm wire so
  the tip lags. Range 0–45° (15° forward sweep), 90° only for celebrate. Shoulder gaiter of minky around the horn.
- Load ≈ 0.02 N·m → XL330 (bus, compliant) or 9 g MG90S (budget).

### 3.6 Head cage (printed)
- 6 gore T-ribs (2.4 × 8 mm section) printed flat + 3 hoops, M3 screws → no layer-line failures at the hoops.
- Spine plate 4 mm, 3 ball studs, 4× M2.5 to carrier/U-joint; cable slot at rear.
- Face plate 80×60 mm, 3 mm: two 16 mm eye wells (dome + camera pupil), two 20 mm LED diffuser pockets (1.5 mm
  white PETG dome + 1 mm foam), M3 for MPR121 board behind.
- Shoulder pockets at 65% height, 35° from front, 3 mm walls around the XL330 body, TPU 2 mm pads under servos.
- 10 mm quilt batting jacket (spray adhesive) over the ribs. PETG throughout (interior 35–45 °C; PLA creeps).

## 4. Skin: designing the fur to fit the cage
### 4.1 Prototype 0: gut a stuffed animal
Find a 7–8" cream egg/bean plush (dense short pile, e.g. a Squishmallow-like or egg plush). Open the bottom seam,
remove the stuffing, measure the interior at 3 heights. Scale the cage so cage + 10 mm batting ≈ interior.
Insert cage ribs through the slit and screw together inside. Use it to validate proportion, eye position, motion.
Expect the fur type/colour to be wrong; that is fine for P0.

### 4.2 Final: sew a one-piece egg skin
- Fabric: 8–12 mm high-density faux fur, warm ivory (avoid optically-brightened white; it goes blue under LEDs).
  Face: sheared to 3–4 mm inside an 80×60 ellipse, or a blended minky panel. Cheeks: dusty pink, not hot pink.
- Pattern: 6 gores from crown to hem derived from the (cage + batting) ellipsoid: height 190, widest Ø140 at 78 mm.
  Rotate gores so the face sits mid-gore (no seam down the face), or sew a separate oval face panel.
  Pile direction radiates from a crown whorl, not straight down.
- Waist bellows: a 40 mm band at 25–65 mm height gets 1–2 cm of extra fabric length (gathered) and only thin batting,
  so a 25° lean (hem moves ~27 mm) folds instead of gaps. Under it, a Lycra tube sewn from cage lip to puck lid keeps
  every fibre out of the pushrods.
- Eyes: 10–11 mm glossy black high-dome eyes with threaded backs (not one-way safety eyes) or 10 mm magnets through
  the face plate → skin is removable and the face stays aligned. Left eye: camera lens as a 4 mm pupil hole in the
  dome centre; polish the dome so the highlight sells it.
- Smile: 2–3 mm satin stitch, 20 mm wide, radius ≈ 25 mm curve, 25 mm below the eye line.
- Hem: elastic channel + 4 snaps to the puck bottom edge (at ~15 mm height); the dark floor disc shows as a shadow.
- Feet: optional 30×20×15 mm stuffed nubs on the puck front at 60 mm centres, toes slightly inward (they yaw too).

## 5. Electronics
### 5.1 Power (two rails, one cable)
- 12 V 5 A brick → jack on the floor disc → 5-wire clock spring → puck.
- Rail A (servos): Pololu D36V50F5 (5 V, 5.5 A) → OpenRB-150 power terminal; 2200 µF low-ESR at bus head; 20 AWG.
- Rail B (Pi): second 5.1 V buck (D24V22F5 class) → Pi power pads. Common ground, star point at the bucks.
- XL330: Current Limit 600–700 mA, Profile Acceleration set, Temperature Limit 60 °C; worst case 6 servos
  starting together ≈ 4 A for 50–100 ms — rail A handles it, Pi never sees it.
- Pi: overlayfs / read-only root so a brownout can't corrupt the card.

### 5.2 Compute
- Primary: Pi Zero 2 W thin client. Runs Dynamixel driver (via OpenRB-150 over USB), MPR121/LED, audio I/O, MJPEG
  640×480 stream. Your ROS 2 host (laptop) runs DOA fusion, face tracking, the behaviour tree and the LLM bridge.
  Needs a small USB hub (OpenRB + USB camera on the single OTG port).
- Option: Pi 4B 2 GB in a slightly larger egg (160 W × 210 H) for everything on-board. Pi 5 does not belong in fur.

### 5.3 Sensing & outputs
- Camera: 25 mm UVC board camera (1080p, ~$25) on 4× 28 AWG silicone wires, lens flush in the left eye dome;
  pile trimmed ≤3 mm within 12 mm radius.
- Audio: ReSpeaker 2-Mic HAT with in-kernel `dtoverlay=wm8960-soundcard`; mic ports via 2 mm holes + acoustic mesh in
  the puck lid with trimmed pile; HAT on rubber grommets; twisted servo bus; treat 2-mic DOA as a ±20° cue and confirm
  with the camera. Speaker effectively ~1 W (fine for chirps/short TTS). If voice is central: ReSpeaker USB Mic Array v2.
- Touch: MPR121 in the head, electrodes ≥40×60 mm conductive fabric sewn to the inside of the skin (crown, back,
  belly), ≥10 mm from servos, leads <100 mm, 1 kΩ series per electrode (ESD), anti-static spray on fur, GND plane
  (aluminium tape ~150 cm² on puck floor). Mask touch for 300 ms around servo moves. I2C at 100 kHz, 2.2 kΩ pull-ups.
- Cheek LEDs: plain warm-pink LEDs driven from MPR121 ELE4–11 (GPIO mode) → no WS2812/PWM conflict with I2S.
  Diffuser dome, ≤15% duty, ≥400 ms ramps.
- Harness puck→head: 3 (Dynamixel to arm servos) + 4 (I2C+3V3+GND) + 4 (USB cam) = 11 wires, one JST-PH connector at
  the spine plate; single-plane service loop at the rear, ≥25 mm bend radius, sized at both extreme poses.
- Thermal: ≥10 cm² vents top and bottom of the puck, bare (unfurred) underside, torque-off at idle (spring holds the
  head up; add a soft forward pitch stop), poll servo temperature.

## 6. Behaviour (motion vocabulary)
- Idle: Perlin-noise breathing, pitch ±2° + heave ±3 mm at 0.25–0.3 Hz; occasional head-cock (roll 12° + pitch back
  4°, 250 ms ease-in, hold ≥1.5 s); arm micro-lifts.
- Attention: yaw saccade to sound in ~200 ms with slight overshoot, 300 ms settle; then camera face-track (yaw + pitch).
- Speech: heave bob + small pitch on syllables (not pitch alone — "pecking chicken").
- Reactions: pet → lean into the hand, cheek glow, chirp; push → yield (current-based position mode), spring back;
  celebrate → arms 90° + 3 bounces.
- Limits: software joint/velocity/current caps; min-jerk trajectories ≥0.3 s except saccades.
- ROS 2 nodes: dynamixel_driver, audio_doa, face_tracker, touch, behaviour_tree, llm_bridge.

## 7. Build phases
P0 (weekend 1): print cage mock + puck shell, gut a plush, hand-pose for proportion/eye checks.
P1: tilt platform on the bench (3 XL330, post, slider, U-joint, pushrods), IK, spring tuning.
P2: floor disc + lazy-susan + ring gear + yaw; puck electronics, two rails, clock-spring ribbon.
P3: head cage, arms, face plate, camera eye, cheek LEDs, MPR121.
P4: one-piece fur skin, batting, bellows, hem snaps; feet.
P5: behaviours, DOA/face fusion, voice/LLM bridge, idle life.

## 8. BOM (primary path)
| Item | Qty | Est. |
|---|---|---|
| Dynamixel XL330-M288-T (yaw, 3 tilt, 2 arms) | 6 | $144 |
| OpenRB-150 | 1 | $25 |
| Raspberry Pi Zero 2 W + micro USB hub | 1 | $25 |
| ReSpeaker 2-Mic HAT + 28 mm speaker | 1 | $17 |
| UVC board camera 25 mm | 1 | $25 |
| MPR121 + conductive fabric + LEDs | 1 | $20 |
| 12 V 5 A brick + D36V50F5 + 5 V buck | 1 | $40 |
| 76 mm lazy-susan, 4× 684ZZ, LM8UU, 8 mm rod, spring | — | $18 |
| M2 ball links/pushrods, M2/M3 hardware, TPU pads, JST | — | $15 |
| Fur ½ yd + minky + 10 mm dome eyes + batting + Lycra | — | $35 |
| PETG ~350 g | — | $9 |
| 3 mm steel disc Ø150 + washers | — | $15 |
| **Total** | | **≈ $390** |
Budget path (~$230): 4× Feetech STS3215 (7.4 V) + Waveshare bus adapter for yaw/tilt, 2× MG90S arms, Pi Zero 2 W.

## 9. Risks (open)
- Fur in mechanism → Lycra under-tube, gaiters, pile trimmed near horns.
- Noise → bus servos, TPU pads, cage as soundboard (batting helps), min-jerk.
- Heat → vents, spring compensation, torque-off idle, 60 °C limit.
- Tip → 1.25 kg, 70 mm feet, 25° forward cap.
- Skin bunching at waist → bellows band; validate on P0 plush.
- First-timer traps: XL330 default ID 1 @ 57600 (configure one at a time), 0.1 N·m max on horn screws, bearing seats
  print 0.3 mm undersize, size cable loops at both extremes, common ground between rails, screw ballast (don't glue).
