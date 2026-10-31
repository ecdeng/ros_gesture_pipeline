# Jolly-bot shopping list (U2D2 + Power Hub path)

Researched 30–31 Oct 2026. Prices are from vendor pages on those dates unless marked *est.*; shipping and tax are not included. Grouped by store so each block is one cart.

| Section | Subtotal |
|---|---|
| Servos, controller, computer | $370 |
| Power | $110 |
| Audio, touch, lights, sensors | $54 |
| Mechanical hardware | $189 |
| Fur, foam, eyes | $121 |
| Tools and consumables (skip what you own) | $48 |
| **Total** | **$891** |

## Servos, controller, computer

| Store | Item | Qty | Unit | Line | Link / part | Note |
|---|---|---|---|---|---|---|
| Seeed Studio (ships from China) | Dynamixel XL330-M288-T, Reachy Mini spare **No.1–No.5** (one of each; IDs pre-set 1–5) | 5 | $31.40 | $157.00 | https://www.seeedstudio.com/Servo-Motor-1-5V-103RPM-Brush-mm-p-6783.html (No.2–5 linked from it) | Tilt ×3, arms ×2. Limit 2 per listing. |
| Seeed Studio (ships from China) | Dynamixel XL330-M077-T, Reachy Mini spare **Servo R** | 1 | $31.40 | $31.40 | https://www.seeedstudio.com/Servo-Motor-R-5V-383RPM-Brush-mm-p-6784.html | Yaw. Re-ID to 6. |
| Seeed Studio (ships from China) | ReSpeaker 2-Mics Pi HAT **V2.0** | 1 | $13.99 | $13.99 | https://www.seeedstudio.com/ReSpeaker-2-Mics-Pi-HAT.html | Overlay `respeaker-2mic-v2_0`. |
| RobotShop (US) | Robotis **U2D2** USB-to-Dynamixel adapter | 1 | $46.76 | $46.76 | https://www.robotshop.com/products/robotis-u2d2-usb-to-serial-adapter-for-dynamixel | Includes micro-USB cable. |
| RobotShop (US) | Robotis **Robot Cable-X3P 180 mm**, 10-pack | 1 | $21.85 | $21.85 | https://www.robotshop.com/products/robotis-robot-cable-x3p-180mm-dynamixel-x-series-ttl-only-10x | Servo daisy-chain leads. |
| RobotShop (US) | Arducam 8 MP IMX219 USB camera board (B0196) | 1 | $31.56 | $31.56 | https://www.robotshop.com/products/arducam-8mp-1080p-usb-camera-module | Small fixed lens for the eye pupil. |
| Generation Robots (EU) — or RoboSavvy UK £16.33 / Reichelt €39.95 / eBay | Robotis **U2D2 Power Hub Board** set (€28.20) | 1 | $32.00 *est.* | $32.00 | https://www.generationrobots.com/en/403359-u2d2-power-hub-board.html | ≈ USD at today's rate; 2 left. Feed exactly 5 V. |
| PiShop.us | Raspberry Pi **Zero 2 W** | 1 | $17.25 | $17.25 | https://www.pishop.us/product/raspberry-pi-zero-2-w/ | Limit 1. Take the pre-soldered WH ($20.75) if it is back. |
| PiShop.us | microSD card, 32 GB A1 | 1 | $10.00 *est.* | $10.00 | PiShop or any brand-name card |  |
| PiShop.us | 2×20 male header (only for the bare Zero 2 W) | 1 | $1.00 *est.* | $1.00 | PiShop / Adafruit |  |
| Waveshare | USB HUB HAT (B) for Pi Zero | 1 | $6.99 | $6.99 | https://www.waveshare.com/usb-hub-hat-b.htm | U2D2 + camera into the Zero's one USB port. |

**Subtotal: $369.80**

## Power

| Store | Item | Qty | Unit | Line | Link / part | Note |
|---|---|---|---|---|---|---|
| Digi-Key | Mean Well **GST60A12-P1J** 12 V 5 A desktop supply | 1 | $19.40 | $19.40 | https://www.digikey.com/en/products/detail/mean-well-usa-inc/GST60A12-P1J/7703712 |  |
| Digi-Key | IEC C13 mains cord | 1 | $5.00 *est.* | $5.00 | any |  |
| Digi-Key | Panasonic EEU-FR1A222L 2200 µF 10 V | 1 | $1.46 | $1.46 | https://www.digikey.com/en/products/result?keywords=EEU-FR1A222L | At the Power Hub screw terminal. |
| Pololu | **D36V50F5** 5 V 5.5 A regulator (servo rail → Power Hub terminal) | 1 | $39.95 | $39.95 | https://www.pololu.com/product/4091 | Rationed. |
| Pololu | **D24V22F5** 5 V 2.5 A regulator (Pi rail) | 1 | $26.95 | $26.95 | https://www.pololu.com/product/2858 | Rationed. |
| SparkFun | Panel-mount 2.1 mm DC barrel jack | 1 | $1.75 | $1.75 | https://www.sparkfun.com/dc-barrel-power-jack-connector.html |  |
| Amazon | Silicone wire kit, 20 and 22 AWG | 1 | $15.00 *est.* | $15.00 | any | 5 V runs and the 2-wire yaw clock spring. |

**Subtotal: $109.51**

## Audio, touch, lights, sensors

| Store | Item | Qty | Unit | Line | Link / part | Note |
|---|---|---|---|---|---|---|
| Digi-Key | CUI CMS-251452-28SP 28 mm 8 Ω speaker | 1 | $6.71 | $6.71 | https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/CMS-251452-28SP/21284706 |  |
| Digi-Key | Inolux IN-S63BT5UW 0603 white LED (eye catchlights) | 10 | $0.23 | $2.30 | https://www.digikey.com/en/products/detail/inolux/IN-S63BT5UW/7604936 |  |
| Digi-Key | Kingbright WP7113VRVC1C 5 mm pink LED (cheeks) | 4 | $1.22 | $4.88 | https://www.digikey.com/en/products/detail/kingbright/WP7113VRVC1C/7776808 |  |
| Adafruit | MPR121 capacitive touch breakout (1982) | 1 | $7.95 | $7.95 | https://www.adafruit.com/product/1982 |  |
| Adafruit | Woven conductive fabric (1168) | 1 | $4.95 | $4.95 | https://www.adafruit.com/product/1168 | Four touch pads. |
| Adafruit | US5881LUA hall sensor (158) | 2 | $2.00 | $4.00 | https://www.adafruit.com/product/158 | Yaw homing (one spare). |
| Adafruit | 1 kΩ resistors, 25-pack (4294) | 1 | $0.75 | $0.75 | https://www.adafruit.com/product/4294 |  |
| Adafruit | 28 AWG silicone ribbon, 10-wire, 1 m (3890) | 1 | $3.95 | $3.95 | https://www.adafruit.com/product/3890 | Head harness. |
| Adafruit | JST-PH 2.0 connector kit (4422) | 1 | $8.95 | $8.95 | https://www.adafruit.com/product/4422 | Harness connector at the neck. |
| Amazon | Ø5 × 2 mm N52 magnets, small pack | 1 | $7.00 *est.* | $7.00 | any | Yaw homing magnet. |
| Prym/Dritz | Dritz sew-on snaps size 2/0, 10 sets (80-20-65) | 1 | $2.89 | $2.89 | https://www.prymconsumerusa.com/products/80-20-65 | Touch-pad connectors. |

**Subtotal: $54.33**

## Mechanical hardware

| Store | Item | Qty | Unit | Line | Link / part | Note |
|---|---|---|---|---|---|---|
| Zoro | 61810-2RS bearing 50 × 65 × 7 (Tritan) | 1 | $16.39 | $16.39 | https://www.zoro.com/i/G2727630/ |  |
| Zoro | Ø5 × 20 mm dowel pins, 25-pack | 1 | $3.25 | $3.25 | https://www.zoro.com/i/G3424377/ |  |
| Zoro | M2 stainless all-thread, 1 m | 1 | $8.19 | $8.19 | https://www.zoro.com/i/G0319116/ | Three 45 mm pushrods. |
| Zoro | M4 × 5 cup-point set screws, 100-pack | 1 | $4.05 | $4.05 | https://www.zoro.com/i/G9899246/ |  |
| Ultimate 3D Printing Store | igus Drylin RJ4JP-01-08 bushing, 3-pack | 1 | $8.50 | $8.50 | https://ultimate3dprintingstore.com/products/igus-drylin-rj4jp-01-08-bearing-1-piece |  |
| HeliDirect / eBay | Align 450 linkage balls 4.75 mm (H45Z002XXT) | 1 | $7.99 | $7.99 | https://helidirect.com/search?q=H45Z002XXT |  |
| HeliDirect / eBay | 450-size ball links ×12 (CopterX) | 1 | $4.86 | $4.86 | https://www.ebay.com/itm/127290105452 |  |
| Amazon | 8 mm hardened chrome shaft, 100 mm | 1 | $12.00 *est.* | $12.00 | any (check 8.00 mm) |  |
| Amazon | Steel U-joint coupler 5 × 5 mm bore, 2-pack (HobbySoar B0782WB5Q1) | 1 | $9.00 *est.* | $9.00 | Amazon |  |
| Amazon | GT2 6 mm closed belt 130T / 260 mm | 1 | $5.00 *est.* | $5.00 | any |  |
| Amazon | GT2 20T pulley, 5 mm bore, 6 mm belt | 1 | $9.00 *est.* | $9.00 | any |  |
| Amazon | M3 (M3×4×5) and M4 heat-set inserts | 1 | $21.00 *est.* | $21.00 | CNC Kitchen / ruthex |  |
| Amazon | Rubber feet Ø10 ×4 + PTFE glide pads ×3 | 1 | $8.00 *est.* | $8.00 | any |  |
| Amazon | PETG 1 kg + TPU 95A 1 kg | 1 | $38.00 *est.* | $38.00 | Overture / Sunlu |  |
| Home Depot | M2–M5 stainless socket screw kit with nuts (MYWISH SF-TZ00005) | 1 | $22.72 | $22.72 | https://homedepot.com/p/334334772 |  |
| Wagner | Steel disc 4.5 in × 1/8 in (D240) | 2 | $5.33 | $10.66 | https://shop.wagnercompanies.com/disk-d240 | Ballast. |

**Subtotal: $188.61**

## Fur, foam, eyes

| Store | Item | Qty | Unit | Line | Link / part | Note |
|---|---|---|---|---|---|---|
| Missouri Star Quilt Co | Shannon Luxe Cuddle Seal, Natural, 1 yd | 1 | $24.92 | $24.92 | https://www.missouriquiltco.com/products/cuddle-luxe-seal-natural-60-minky-yardage | Order a swatch first: pile is listed as 10 and 15 mm. |
| Linda's / Fat Quarter Shop | Cuddle 3 minky Ivory, ½ yd (face) | 1 | $7.74 | $7.74 | https://www.lindas.com/products/quilting-cuddle-solid-ivory-fabric-per-yard |  |
| Linda's / Fat Quarter Shop | Cuddle 3 minky Desert Rose, ½ yd (cheeks) | 1 | $7.74 | $7.74 | https://www.fatquartershop.com/cuddle-desert-rose-solid-yardage |  |
| Zoro | Open-cell foam 24 × 24 × ½ in | 1 | $18.95 | $18.95 | https://www.zoro.com/i/G1977297/ |  |
| Zoro | M4 × 10 pan-head screws, 50-pack (eye posts) | 1 | $5.59 | $5.59 | Midwest Fastener 51544 on Zoro |  |
| Potomac Beads | 10 mm Czech glass cabochons, Jet, 5-pack (eyes) | 1 | $2.99 | $2.99 | https://potomacbeads.com/czech-cabochons-jet-10mm-pack-of-5 | Price shown but not confirmed at cart. |
| Nick of Time / Dritz / Sewing Parts Online / Ripstop by the Roll | White power mesh ½ yd + 1 in knit elastic 3 yd | 1 | $12.67 | $12.67 | SKU 7150 + Dritz 9518 |  |
| Nick of Time / Dritz / Sewing Parts Online / Ripstop by the Roll | YKK 9 in invisible zipper, Natural | 1 | $2.99 | $2.99 | https://www.sewingpartsonline.com/products/unique-9in-invisible-zipper-ykk |  |
| Nick of Time / Dritz / Sewing Parts Online / Ripstop by the Roll | Gütermann Mara 70 thread | 1 | $4.75 | $4.75 | https://ripstopbytheroll.com/products/gutermann-mara-70 |  |
| The Cross Living | Jellycat Bashful Cream Bunny, Medium (P0 prototype) | 1 | $33.00 | $33.00 | https://www.thecrossliving.com/en-us/products/bashful-cream-bunny-med |  |

**Subtotal: $121.34**

## Tools and consumables (skip what you own)

| Store | Item | Qty | Unit | Line | Link / part | Note |
|---|---|---|---|---|---|---|
| Chewy / Zoro / Walmart | Wahl Pocket Pro trimmer + slicker brush | 1 | $21.98 | $21.98 | Chewy 151806 + 233468 | Only if shearing instead of a minky face. |
| Chewy / Zoro / Walmart | 3M Super 77 + Static Guard + Fray Check | 1 | $25.58 | $25.58 | Zoro / Walmart |  |

**Subtotal: $47.56**

## Order first
1. **Raspberry Pi Zero 2 W** — one per order at PiShop, out of stock at Adafruit, SparkFun and CanaKit.
2. **U2D2 Power Hub** — two left at Generation Robots; RoboSavvy and Reichelt are the backups. Shipping to the US is unconfirmed.
3. **Pololu regulators** — rationed.
4. **Seeed servos** — ship from China; allow for transit and any import charges.

## How the servo electronics connect
```
laptop / Pi USB ── U2D2 ══(100 mm X3P, included)══ Power Hub ══ yaw ══ tilt 1 ══ tilt 2 ══ tilt 3 ══ neck harness ══ arm L ══ arm R
                                                     ▲
12 V brick ── Pololu D36V50F5 (5.0 V) ── 2200 µF ──┘ screw terminal  (never 12 V: XL330 max is 6 V)
12 V brick ── Pololu D24V22F5 (5.0 V) ── Pi Zero 2 W
```
Servo setup: scan in Dynamixel Wizard at 57,600 and 1,000,000 baud, give the yaw servo ID 6, then set Operating Mode 5,
Current Limit 600 mA (400 mA when idle) and Return Delay 0.

## Not needed on this path
OpenRB-150, 3P JST Expansion Board, crimp tools.
