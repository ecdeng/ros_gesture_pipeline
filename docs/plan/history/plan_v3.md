# "Jolly-bot" — tabletop fluffy social robot (plan v3, after critic rounds 1–2)

Changelog v2→v3 (from fabrication/maker and HRI critiques):
- Buy the joint: steel RC driveshaft U-joint or 8 mm stepper-coupling U-joint instead of a printed cross on 684ZZ.
- Linear guide: 8 mm hardened shaft + LM8LUU (or igus RJ4JP-01-08, silent); housing bore from a test coupon.
- Yaw drive: GT2 belt (printed 120T pulley ring on puck, 20T on servo), 6:1, forgiving of lazy-susan wobble. Ring gear dropped.
- Pushrods: Align T-Rex 450 linkage balls/rods (M2), 55–60 mm long; printed horn arm r=20 mm; spine plate raised 10 mm.
- Cage: two half-shells (1.6 mm wall, windows) replace 6 ribs + 3 hoops; M3 heat-set inserts everywhere.
- Skin: 20–25 cm invisible zipper centre-back; eyes with M4 threaded shank into heat-set inserts (screw in from outside);
  arm paddles bolt to horns through the fabric after the skin is on; electrode snaps double as connectors.
- Gore pattern from a 10-line script (half-width = π·r(z)/6 vs arc length), 8 mm seam allowance, 2–4 % negative ease, crown cap.
- 10 mm open-cell foam jacket (not batting); power-mesh under-tube with elastic, or TPU boots over the pushrods.
- Pitch range flipped to −25° up / +15° down; camera tilted 15–20° up in its well.
- Animation engine runs on the Pi at 100 Hz; host sends intents (clips/targets) at ≤10 Hz; watchdog keeps idle alive.
- Additive layer blending, touch masking only above 30°/s, pet/tap/stroke discrimination, crown electrode split L/R.
- Blink-equivalents (catchlight LED dim + heave dip), saccade-and-fixate gaze with aversion, onset-based sound response.
- Non-verbal chirp lexicon primary; Animalese-style gibberish if an LLM talks; envelope-driven bob.
- Awake-idle / drowsy / sleep lifecycle; privacy: sleep posture occludes camera, listening cue, wake-word gating, mute gesture.

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
| Tilt | pitch −25° (up) / +15° (down), roll ±18°, heave ±6 mm (IK clamps each pushrod to ±18 mm) |
| Arms | 2 × fabric-hinged paddles, 0–45° normal, 90° "celebrate" |
| Face | 2 glossy black domes 10–11 mm, interocular 50 mm, eye line at 62% of height (~118 mm up), satin-stitch smile 20 mm wide ~25 mm below eye line, dusty-pink cheek glow 30 mm, centres 8 mm below / 12 mm outboard of eyes |
| Fur | 8–12 mm high-density plush (Jellycat-type), warm ivory, face ellipse 80×60 sheared to 3–4 mm or minky panel |
| Sensors | 2-mic array (coarse DOA), USB camera in one eye, MPR121 touch (crown, back, belly), servo load (push/hug) |
| Outputs | 6 servos, cheek LEDs, 1 W speaker |
| Power | tethered 12 V 5 A brick → 5 V servo rail + 5.1 V Pi rail |
| Brain | Pi Zero 2 W runs the 100 Hz animation engine + reflexes; your ROS 2 host (laptop) runs perception, behaviour, LLM; Pi 4B 2 GB if you want vision on-board |

## 2. Architecture (bottom → top)
```
Table
└─ FLOOR DISC (static, Ø150 × 15 mm, dark): 3 mm steel plate (ballast ~360 g) + printed tray, 4 rubber feet at r≥70,
   yaw servo (XL330) with 20T GT2 pulley on a slotted mount, 76 mm steel lazy-susan bearing, 12 V jack at rear
   └─ LOWER BODY "PUCK" (rotates, Ø~135 × 50 mm, printed PETG tray+lid): 120T GT2 pulley ring printed on its floor (6:1),
      Pi Zero 2 W + ReSpeaker 2-Mic HAT, two bucks, OpenRB-150, 28 mm speaker (front), 3 tilt servos at 120°,
      8 mm hardened shaft (centre) with LM8LUU/igus slider + gravity spring, ~200 g extra ballast low at rim
      └─ TILT PLATFORM: slider carrier → bought steel U-joint (RC driveshaft or 8 mm coupling type) → SPINE PLATE
         (4 mm PETG, 3× M2 linkage balls at r=30 mm, 120° apart), driven by three 55–60 mm M2 pushrods
         └─ HEAD CAGE (two half-shells, 1.6 mm wall, windows; ~90 g): face plate + shoulder pockets moulded into the
            front shell, M3 heat-set inserts, 2 arm servos, MPR121 + LEDs, camera board; 10 mm open-cell foam jacket
            └─ ONE-PIECE FUR SKIN crown→hem, centre-back invisible zipper, slack band at waist, hem snapped to puck
```
Waist crease sits at ~45 mm (≈24% of height) and is hidden by pile + bellows; it never twists because yaw moves everything.

## 3. Kinematics & mechanism detail
### 3.1 Yaw (whole bean)
- 76 mm (3") steel lazy-susan between floor tray and puck floor: cheap ($3–4), smooth, ~50 mm open centre.
- Drive: GT2 6 mm closed belt (~400 mm) from a 20T pulley on a printed XL330 horn adapter to a 120T pulley ring printed
  on the puck floor, outside the bearing plate (6:1). XL330 in extended-position mode (±110° output = ±660° input).
  Belt forgives the cheap bearing's 0.3–0.5 mm wobble, is near-silent and never wears like a PETG gear;
  tension via a ±3 mm slotted servo mount. (A ring gear does not fit: the lazy-susan plate occupies r 25–54 mm.)
- Only a 5-wire silicone ribbon crosses yaw, as a 1.5-turn "clock spring" in the ~Ø50 bearing bore:
  12 V + GND (up to the puck) and the 3-wire Dynamixel bus (down to the yaw servo).
- Inertia: puck ~0.7 kg at r≈65 mm + head → I ≈ 0.004 kg·m². A 90° saccade in 0.3 s needs ~90 rad/s² →
  0.36 N·m at the puck → 0.06 N·m at the servo (6:1). Trivial for XL330; limit with a velocity profile.

### 3.2 Tilt + heave: 3-RPS-style parallel platform
- Three XL330 lying flat in the puck at 120°, each with a printed horn arm (4× M2 to the stock horn) carrying an
  Align T-Rex 450 linkage ball (4.75 mm, M2) at r_h = 20 mm; 450-class M2 pushrods with plastic ball links, 55–60 mm
  long, up to matching balls on the spine plate at r_p = 30 mm (ratio 1.5:1). Rod length is adjustable: trim at assembly.
- Centre constraint: 8 mm hardened chromed linear shaft (100 mm, a 3D-printer spare) fixed to the puck floor;
  LM8LUU (45 mm) or igus Drylin RJ4JP-01-08 in a printed carrier whose bore is chosen from a 14.9/15.0/15.1 mm test
  coupon; on top a BOUGHT steel U-joint (1/10 RC driveshaft U-joint, or an 8×8 mm "universal joint coupling") between
  two printed adapters → the U-joint carries all bending load from the head and blocks platform yaw; servos only
  see pushrod axial loads. Never print the joint: two coaxial 4 mm bores will not come out true on FDM.
- Ranges: tilt 32° combined at r=30 → 15.9 mm; heave ±6 mm; IK clamps each pushrod to |z_i| ≤ 18 mm
  (horn ±64°), so full heave is available at small tilt and auto-reduces at extreme tilt.
- Gravity compensation: compression spring on the post under the carrier, ~2.7 N at mid-stroke (head weight), so
  holding a pose costs ~0.1 A instead of 0.4 A; plus 5–8 mm forward CoM bias to preload one gear flank (less shiver).
- IK (small-angle, exact enough at ≤32°): for pushrod i at azimuth a_i = 90°, 210°, 330°:
  z_i = clamp(h + r_p·(θ_pitch·cos a_i + θ_roll·sin a_i), ±18 mm); φ_i = asin(z_i / r_h). Two lines of Python.
- Why not the serial gimbal of v1: it hung ~360 g off two plastic XL330 horns in bending, put the roll servo in the
  head (heat, mass, cable), and gave no heave. The parallel platform fixes all four for one extra servo.
- Fallback (simpler, no bob): fixed U-joint + 2 pushrods at ±45°.

### 3.3 Mass & torque (recomputed)
Head: cage 95 + arm servos 36 + skin/batting share 70 + camera/MPR121/LEDs/wires 40 + arms 35 ≈ **280 g**,
CoM ≈ 70 mm above U-joint. Static at 32° combined: 0.28·9.81·0.07·sin32 ≈ 0.10 N·m. Snappy nod 25° in 0.15 s
(α≈100 rad/s², I≈0.0016) adds 0.16 N·m → **~0.26 N·m at the plate**, shared by 2–3 pushrods through 1.5:1 →
≤ 0.12 N·m per servo (23% of XL330 stall). Holding with spring: ~0.02 N·m. Comfortable; XC330-M288 is an upgrade,
not a need.

### 3.4 Tip-over
Total ≈ 1.25 kg (steel disc 360 g + puck ballast 200 g + parts); CoM ≈ 60 mm; feet at r = 70 mm, rubber μ≥0.6.
Push at the crown (190 mm) to tip ≈ 1.25·9.81·0.07/0.19 ≈ 4.5 N; nod reaction torque 0.25 N·m vs righting 0.86 N·m
→ 3.3× margin. Forward (down) pitch limited to 15°.

### 3.5 Arms
- Horn sits flush under the skin (no bone through a slot). A 45×20×3 mm printed paddle is stitched to the inside of
  the arm gore and bolts to the horn with 2× M2 through the fabric AFTER the skin is on; the fabric is the hinge. Arm: 35–40 mm long, 22–25 mm thick, tapered, foam core on 1.5 mm wire so
  the tip lags. Range 0–45° (15° forward sweep), 90° only for celebrate. Shoulder gaiter of minky around the horn.
- Load ≈ 0.02 N·m → XL330 (bus, compliant) or 9 g MG90S (budget).

### 3.6 Head cage (printed)
- Two half-shells (front/back), 1.6 mm wall, 2 perimeters, large lightening windows; ~90 g total, ~4 h each on a
  220 mm bed, printed open-side down. Joined with 6× M3 into heat-set inserts (M3×4×5) — the skin comes off dozens
  of times, plastic threads won't survive. (Ribs+hoops were 15 parts/18 screws and printed through the foam as bars.)
- Spine plate 4 mm, 3× M2 linkage balls, 4× M3 to the U-joint adapter; cable slot at rear.
- Face plate is a feature of the front shell: 80×60 mm, 3 mm, two 16 mm eye wells with M4 heat-set inserts (eyes with
  M4 threaded shank screw in from outside), camera board registers to the plate behind the left well with a 4 mm
  pupil hole in that dome, camera tilted 15–20° up; two 20 mm LED diffuser pockets (1.5 mm white PETG dome + 1 mm
  foam); M3 bosses for the MPR121 board behind.
- Shoulder pockets at 65% height, 35° from front, 3 mm walls around the XL330 body, TPU 2 mm pads under servos.
- 10 mm open-cell upholstery foam jacket (holds shape; batting mats within weeks) glued to the shell.
  PETG throughout (interior 35–45 °C; PLA creeps).

## 4. Skin: designing the fur to fit the cage
### 4.1 Prototype 0: gut a stuffed animal
Buy an 8" Squishmallow (~Ø160×200 mm, ~$12) or a Jellycat Bashful-type egg in cream. Seam-rip the hand-laddered
closing seam (bottom/back) to 12–15 cm, pull the fill, measure the interior at 3 heights with a cardboard gauge.
Scale the cage so cage + 10 mm foam ≈ interior. Insert the two half-shells, screw together inside, close with
hook-and-loop. Use it for proportion and motion only — the velour surface and dome shape misrepresent the eye read.

### 4.2 Final: sew a one-piece egg skin
- Fabric: 8–12 mm high-density faux fur, warm ivory (avoid optically-brightened white; it goes blue under LEDs).
  Face: sheared to 3–4 mm inside an 80×60 ellipse, or a blended minky panel. Cheeks: dusty pink, not hot pink.
- Pattern: 6 gores from crown to hem derived from the (cage + foam) solid: height 190, widest Ø140 at 78 mm.
  Generate it with a 10-line script: for z in 1 mm steps, gore half-width = π·r(z)/6 plotted against meridian arc
  length → 1:1 PDF. (Blender seams + conformal UV unwrap, or masking-tape wrap on the P0 mock, also work; do not try
  to flatten it in Fusion — the surface isn't developable.) Add 8 mm seam allowance, 2–4 % negative ease for the knit
  backing, cut with the stretch running around the body, and cap the crown with a Ø25 circle so six pile tips don't
  lump. Rotate gores so the face sits mid-gore, or sew a separate oval minky face panel (safer than shearing).
  Pile direction radiates from the crown whorl, not straight down.
- Closure: 20–25 cm invisible zipper (or hook-and-loop placket) centre-back from the hem to ~130 mm; pile hides it.
  Sequence: skin on → zip → screw eyes in from outside → bolt arm paddles to horns through the fabric → snap hem.
- Waist bellows: a 40 mm band at 25–65 mm height gets 1–2 cm of extra fabric length (gathered) and only thin foam,
  so a 25° lean (hem moves ~27 mm) folds instead of gaps. Under it, a power-mesh tube cut 10 % short with elastic at
  both ends (so it never goes slack into a pushrod) — or three printed TPU boots over the pushrod zone.
- Eyes: 10–11 mm glossy black high-dome eyes with an M4 threaded shank screwed into the face-plate inserts through a
  4 mm skin hole → no interior reach, perfect alignment every time, skin fully removable. Left eye: camera lens as a
  4 mm pupil hole in the dome centre; polish the dome so the highlight sells it. A 0603 white "catchlight" LED sits
  behind each dome, off-centre.
- Sewing: cut from the backing with a razor, comb pile inward, 3 mm zigzag or walking foot, brush seams out with a
  slicker brush. If shearing the face: pet clippers with a 3 mm guard, feather over 10 mm, and pick fur whose backing
  matches the pile colour.
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
- Primary: Pi Zero 2 W runs everything latency-critical: the 100 Hz animation engine (layer blender + min-jerk
  interpolator + IK) sync-writing the Dynamixel bus via OpenRB-150, the reflex layer (touch→lean, push→yield),
  GCC-PHAT sound onset/angle, MPR121/LEDs, audio playback, and a 640×480 MJPEG stream. Your ROS 2 host (laptop) runs
  face tracking, behaviour tree, chirp synthesis/LLM bridge and publishes INTENTS only (`/anim/target` 6-DOF pose +
  duration + easing at ≤10 Hz, `/anim/clip` action). Watchdog: no host message for 500 ms → local idle continues;
  5 s → drowsy. Needs a small USB hub (OpenRB + USB camera on the single OTG port).
- Option: Pi 4B 2 GB in a slightly larger egg (160 W × 210 H) for everything on-board. Pi 5 does not belong in fur.

### 5.3 Sensing & outputs
- Camera: 25 mm UVC board camera (1080p, ~$25) on 4× 28 AWG silicone wires, lens flush in the left eye dome;
  pile trimmed ≤3 mm within 12 mm radius.
- Audio: ReSpeaker 2-Mic HAT with in-kernel `dtoverlay=wm8960-soundcard`; mic ports via 2 mm holes + acoustic mesh in
  the puck lid with trimmed pile; HAT on rubber grommets; twisted servo bus; treat 2-mic DOA as a ±20° cue and confirm
  with the camera. Speaker effectively ~1 W (fine for chirps/short TTS). If voice is central: ReSpeaker USB Mic Array v2.
- Touch: MPR121 in the head, electrodes ≥40×60 mm conductive fabric sewn to the inside of the skin (crown L, crown R,
  back, belly) connected via metal sew-on snaps (they are the connector), ≥10 mm from servos, leads <100 mm, 1 kΩ
  series per electrode (ESD), anti-static spray on fur, GND plane (aluminium tape ~150 cm² on puck floor). Mask touch
  only while any joint moves faster than 30°/s (not a blanket 300 ms, or breathing blinds it); MPR121 auto-baseline +
  rate filter. Classify: tap <150 ms, hold >400 ms, stroke = sequential electrodes within 300 ms.
  I2C at 100 kHz, 2.2 kΩ pull-ups.
- Cheek LEDs + eye catchlights: plain LEDs driven from MPR121 ELE4–11 (GPIO mode) → no WS2812/PWM conflict with I2S.
  Diffuser dome, ≤15% duty, ≥400 ms ramps. Catchlights dim for 120 ms every 3–6 s (Poisson) = the blink.
- Harness puck→head: 3 (Dynamixel to arm servos) + 4 (I2C+3V3+GND) + 4 (USB cam) = 11 wires, one JST-PH connector at
  the spine plate; single-plane service loop at the rear, ≥25 mm bend radius, sized at both extreme poses.
- Thermal: ≥10 cm² vents top and bottom of the puck, bare (unfurred) underside, torque-off only in SLEEP (spring
  holds the head up; add a soft forward pitch stop), 300 mA current limit while awake-idle, poll servo temperature.

## 6. Behaviour, animation engine, interaction design
### 6.1 Motion vocabulary
- Idle (awake): Perlin-noise breathing, pitch ±2° + heave ±3 mm at 0.25–0.3 Hz; "notice" micro-events every 20–60 s
  (look at a random point, hold 1 s); occasional head-cock (roll 15–18° + pitch back 4°, 250 ms ease-in, hold ≥1.5 s);
  arm micro-lifts. Never fully still for >2 s while awake.
- Blink-equivalents: catchlight LEDs dim 120 ms every 3–6 s; sometimes paired with a 3 mm heave dip + 2° pitch.
- Attention: sound onset (energy +12 dB over 200 ms, 2 s refractory) → two beats: 120 ms arm micro-lift + cheek flicker
  (acknowledgment), then a 200 ms yaw saccade with slight overshoot, 300 ms settle. Re-estimate angle after turning
  to resolve the 2-mic front/back ambiguity.
- Gaze: saccade-and-fixate, not pursuit — dead-band ±3°, move only if the face is off-centre >150 ms, 200 ms saccade,
  hold. Project the face into body frame with the COMMANDED pose. Gaze aversion every 4–8 s for 300–600 ms
  (60–70 % contact ratio) so it doesn't stare.
- Speech/sound: non-verbal first. A 20–30-item parametric chirp lexicon synthesized live (rising = interest/question,
  falling = sad, trill = joy, double-chirp = acknowledgment), 800 Hz–4 kHz for the 28 mm speaker. If an LLM talks,
  Animalese-style phoneme gibberish from the text; heave bob driven by the audio envelope at 20 ms frames, scheduled
  100 ms ahead (audio/motion skew <40 ms).
- Reactions: pet (stroke) → lean toward that side (roll 10°, pitch back 5°, 400 ms), cheek glow, trill; tap →
  quick heave hop; push → yield (position error >5° for >80 ms → goal current 150 mA, follow), spring back over 600 ms
  with a ±4° roll "shake-off"; celebrate → arms 90° + 3 bounces.
- Lifecycle: awake-idle (torque on, 300 mA limit) → 3 min no stimulus → drowsy (0.12 Hz breath, cheeks dim, pitch −8°)
  → 10 min → sleep (torque off, spring holds, head pitched down so the camera eye looks at the table, stream stopped).
  Wake ramp 1.5 s.
### 6.2 Animation engine (on the Pi, 100 Hz)
final_pose = base_pose + idle_noise·(1 − w_react) + reactive_offset + clip_offset; clips cross-fade in 150–250 ms and
duck idle to 30 %; never hard-switch. IK → clamp → min-jerk interpolation (≥300 ms except saccades) → sync-write.
Host→Pi: `/anim/target` (pose, duration, easing) ≤10 Hz and `/anim/clip` (name, params); timestamps via chrony so the
Pi plays ahead instead of reacting to arrival time. Software caps: joint, velocity (≤300°/s), current.
### 6.3 Latency budget
touch → first motion ≤100 ms (local reflex) · sound onset → yaw start 200–300 ms · face appears → gaze lands ≤500 ms ·
audio/motion skew <40 ms · host dropout 500 ms → idle continues locally.
### 6.4 Privacy
Camera physically occluded in sleep posture and stream stopped; visible "listening" cheek pattern whenever audio leaves
the device; wake-word gating on the Pi before any audio reaches an LLM; LAN-only by default, nothing persisted;
hold the crown 2 s → mute toggle with a distinct chirp.
### 6.5 ROS 2 nodes
Pi: anim_engine, dynamixel_io, touch, audio_io (+GCC-PHAT), camera_stream. Host: face_tracker, sound_fusion,
behaviour_tree, chirp_synth / llm_bridge, teleop/animation authoring tool.

## 7. Build phases
P0 (weekend 1): print half-shell mock + puck shell, gut an 8" Squishmallow, hand-pose for proportion/eye checks.
P1: tilt platform on the bench (3 XL330, shaft, slider, bought U-joint, pushrods), IK, spring tuning, 100 Hz engine.
P2: floor disc + lazy-susan + GT2 belt yaw; puck electronics, two rails, clock-spring ribbon.
P3: head shells, arms, face plate, threaded eyes + camera pupil, cheek/catchlight LEDs, MPR121.
P4: gore script → one-piece fur skin, foam jacket, bellows + mesh tube, zipper, hem snaps; feet.
P5: chirp lexicon, idle life, DOA/face fusion, touch reactions, privacy gating, LLM bridge last.

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
| 76 mm lazy-susan, steel U-joint, LM8LUU/igus, 8 mm hardened shaft, spring | — | $22 |
| GT2 belt + 20T pulley, T-Rex 450 balls/rods, heat-set inserts, M2/M3, TPU pads, JST | — | $25 |
| Fur ½ yd + minky + M4-shank dome eyes + 10 mm foam + power mesh + zipper | — | $40 |
| PETG ~350 g | — | $9 |
| 3 mm steel disc Ø150 + washers | — | $15 |
| **Total** | | **≈ $410** |
Budget path (~$230): 4× Feetech STS3215 (7.4 V) + Waveshare bus adapter for yaw/tilt, 2× MG90S arms, Pi Zero 2 W.

## 9. Risks (open)
- Fur in mechanism → power-mesh under-tube / TPU boots, gaiters, pile trimmed near horns.
- Noise → bus servos, TPU pads, cage as soundboard (batting helps), min-jerk.
- Heat → vents, spring compensation, 300 mA awake-idle limit, torque-off in sleep, 60 °C limit.
- Tip → 1.25 kg, 70 mm feet, 15° forward cap.
- Skin bunching at waist → bellows band; validate on P0 plush.
- Dead-robot over Wi-Fi → animation engine + idle live on the Pi; host sends intents only.
- Privacy → sleep posture occludes camera, listening cue, wake-word gating, mute gesture.
- First-timer traps: XL330 default ID 1 @ 57600 (configure one at a time), 0.1 N·m max on horn screws, bearing seats
  print 0.3 mm undersize, size cable loops at both extremes, common ground between rails, screw ballast (don't glue).
