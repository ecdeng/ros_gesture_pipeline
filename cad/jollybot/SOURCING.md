# Jolly-bot sourcing sheet (US buyer, researched 2026-10-30)

Prices are what vendor pages showed on the research date; stock changes weekly. 'Alt' rows (qty 0) are fallbacks and are not in the total. Estimates are marked in the notes.

**Primary path total ≈ $818** (with the in-stock Seeed servos) (6 Dynamixel servos, OpenRB-150, Pi Zero 2 W, Pololu rails, bearing/bushing/U-joint, fur, eyes, prototype plush, tools). Without tools and prototype plush ≈ $738.

## What the research changed in the design

- **Belt**: a 136T GT2 belt is eBay-only. CAD now uses a stocked **130T / 260 mm** belt with a **20T** pulley at r 49.8 (6:1). To keep yaw saccades fast through 6:1, the yaw servo becomes the faster **XL330-M077-T**; the tilt and arm servos stay M288.
- **U-joint**: 5×5 mm couplers are sold as Ø11 × 22–23 mm imports, not Ø10 × 24; `params.py` updated.
- **Eyes**: no threaded-shank 10 mm toy eye exists; the design is a 10 mm glass cabochon epoxied to an M4 pan-head screw into the face-plate insert.
- **Audio HAT**: the ReSpeaker 2-Mics HAT is now V2 (TLV320AIC3104) and needs the `respeaker-2mic-v2_0` overlay from Seeed's dtoverlays repo, not `wm8960-soundcard`.
- **Power connector**: no reputable magnetic breakaway barrel adapter was found; use a right-angle plug and anchor the cord to the desk instead.
- **Servos and controller**: Robotis US is sold out of X330 parts and OpenRB-150, and Generation Robots now quotes 8 weeks. Genuine XL330s are in stock at Seeed as Reachy Mini spares (pre-set IDs, $31.40). Pair them with the in-stock U2D2 and let the Pi speak Dynamixel directly.
- **Foam**: 3/8 in open-cell sheet isn't stocked; buy ½ in and shave, or reduce `LAYER_STACK` air gap.

## Stock risks to act on first

1. Pi Zero 2 W: one per order at PiShop, out of stock elsewhere — order today.
2. Servos: buy the Seeed Reachy Mini XL330 spares (No.1–5 + R) and a U2D2 from RobotShop now; OpenRB-150 is sold out everywhere checked.
3. Pololu regulators are rationed.
4. Align ball links (H45045) are out of stock at US hobby shops; the eBay CopterX set is the stand-in.

## Actuation

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| **Buy today:** Dynamixel XL330-M288-T, Seeed "Reachy Mini" spares No.1–No.5 (one of each) | 5 | Seeed Studio | e.g. No.1 https://www.seeedstudio.com/Servo-Motor-1-5V-103RPM-Brush-mm-p-6783.html · No.2 https://www.seeedstudio.com/Servo-Motor-2-5V-103RPM-Brush-mm-p-6786.html (No.3–6 linked from the same page) | $31.40 | $157.00 | IN STOCK (China warehouse), checked 2026-10-31. Limit 2 per SKU per account | Genuine XL330-M288-T. Each number ships pre-set to that ID (1–5), so no ID setup. Servo arm included; cable not listed, so plan on JST EH 3-pin leads. |
| **Buy today:** Dynamixel XL330-M077-T (yaw), Seeed "Reachy Mini" spare R | 1 | Seeed Studio | https://www.seeedstudio.com/Servo-Motor-R-5V-383RPM-Brush-mm-p-6784.html (L variant: …-p-6788.html) | $31.40 | $31.40 | IN STOCK, limit 2 | Fast M077 for the 6:1 yaw belt. Pre-set ID is a letter, not a number: change it to 6 in Dynamixel Wizard. |
| Dynamixel XL330-M288-T / M077-T (Robotis US) | alt | ROBOTIS US | 902-0163-000 · https://www.robotis.us/dynamixel-xl330-m288-t/ | $27.49 | $0.00 | SOLD OUT, ~2-month lead. Generation Robots (EU) now also quotes 8 weeks | Cheaper per unit if you can wait. |
| OpenRB-150 controller | 1 | ROBOTIS US | 902-0183-000 · https://www.robotis.us/openrb-150/ | $28.64 | $28.64 | SOLD OUT in US; RoboSavvy UK £24.25 | 4× TTL 3-pin ports, DXL bus up to 3 A, VIN 3.7–12.6 V (feed exactly 5 V for XL330), USB-C powers the MCU. Bus FET off at boot. |
| Alt: U2D2 USB adapter | alt | RobotShop | RB-Rbi-251 · https://www.robotshop.com/products/robotis-u2d2-usb-to-serial-adapter-for-dynamixel | $46.76 | $0.00 | IN STOCK — fallback if OpenRB stays unavailable | Pi runs the Dynamixel SDK directly; inject 5 V into the chain with a hand-made 3-pin splice (Power Hub is sold out, 18-wk lead). |
| Alt budget: Feetech STS3215 7.4 V ×6 + Waveshare Bus Servo Adapter (A) | alt | Waveshare / Seeed | SKU 33014 $16.99 · https://www.waveshare.com/st3215-servo.htm?sku=33014 ; adapter SKU 25514 $4.99 | $106.93 | $0.00 | In stock, ships from CN | Needs its own 7.4 V buck; no current-based compliance. Don't buy the 12 V variant (SKU 22414). |

## Compute

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| Raspberry Pi Zero 2 W | 1 | PiShop.us | SKU 1799 · https://www.pishop.us/product/raspberry-pi-zero-2-w/ | $17.25 | $17.25 | Adafruit/SparkFun/CanaKit out of stock | Limit 1 per order. Bare board needs a 2×20 header soldered for the HAT; the WH (pre-soldered, SKU 112-1, $20.75) is wish-list only today. |
| Alt: Raspberry Pi 4 Model B 2 GB | alt | PiShop.us | 2GB-9003 · https://www.pishop.us/product/raspberry-pi-4-model-b-2gb/ | $67.50 | $0.00 | IN STOCK | Only if on-board vision is wanted; needs a bigger puck (Ø~150) and a 5 V 3 A rail. |
| Waveshare USB HUB HAT (B) for Zero | 1 | Waveshare | SKU 20317 · https://www.waveshare.com/usb-hub-hat-b.htm | $6.99 | $6.99 | In stock | Pogo-pin hub under the Zero: 4× USB 2.0 for OpenRB + camera. Alt: Adafruit 2991 OTG hub cable $5.95. |

## Audio

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| ReSpeaker 2-Mics Pi HAT V2.0 | 1 | Seeed Studio | 107100001 · https://www.seeedstudio.com/ReSpeaker-2-Mics-Pi-HAT.html | $13.99 | $13.99 | In stock (CN); RobotShop US $14.02 | V2 uses a TLV320AIC3104 codec: overlay is `respeaker-2mic-v2_0` from seeed-linux-dtoverlays, NOT wm8960. Uses I2S GPIO18–21, I2C 2/3, button GPIO17, LEDs on SPI. |
| Speaker 28 mm 8 Ω 2 W (CUI CMS-251452-28SP) | 1 | Digi-Key | 2223-CMS-251452-28SP-ND · https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/CMS-251452-28SP/21284706 | $6.71 | $6.71 | 904 in stock | 28×28 mm frame, 10.8 mm deep. HAT amp delivers ~1 W into it. |

## Vision

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| Arducam 8 MP IMX219 UVC camera board | 1 | RobotShop | B0196 / RB-Adu-100 · https://www.robotshop.com/products/arducam-8mp-1080p-usb-camera-module | $31.56 | $31.56 | In stock | 38×38 mm, fixed ~6–7 mm lens barrel = best pupil candidate, MJPEG native, H 62° FOV. ELP M12 boards have 10–12 mm front elements — too big for the eye. |

## Sensing

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| MPR121 12-key capacitive breakout (STEMMA QT) | 1 | Adafruit | 1982 · https://www.adafruit.com/product/1982 | $7.95 | $7.95 | In stock | I2C 0x5A beside the HAT codec; has its own 10 kΩ pull-ups (fine in parallel). |
| Woven conductive fabric | 1 | Adafruit | 1168 · https://www.adafruit.com/product/1168 | $4.95 | $4.95 | In stock | Enough for four 40×60 mm pads. Knit version 1364 $14.95 stretches with the skin. |
| Sew-on snaps size 2/0 (10 mm), 10 sets | 1 | Dritz | 80-20-65 · https://www.prymconsumerusa.com/products/80-20-65 | $2.89 | $2.89 | In stock | Electrode connectors between skin and harness. |
| Hall sensor US5881LUA | 2 | Adafruit | 158 · https://www.adafruit.com/product/158 | $2.00 | $4.00 | In stock | Yaw homing. Latching type; use a 3-wire pull-up. A3144 6-pk ≈$10 on Amazon is the alternative. |
| Ø5×2 mm N52 magnets | 1 | TotalElement / Amazon | https://totalelement.com/products/5mm-x-2mm-neodymium-rare-earth-permanent-disc-magnets-n52-200-pack | $24.29 | $24.29 | In stock | 200-pack is the only TotalElement size; a 20–50 pack on Amazon is ~$6–8. |
| 0603 white LEDs ×10 (catchlights) + 5 mm pink LEDs ×4 + 1 kΩ ×25 | 1 | Digi-Key / Adafruit | Inolux IN-S63BT5UW 1830-1070-1-ND $0.23 · Kingbright WP7113VRVC1C 754-2184-ND $1.22 · Adafruit 4294 $0.75 | $8.00 | $8.00 | In stock | No stock 'warm pink'; diffuse the pink LED behind dusty-pink minky. Total ≈ $8. |

## Power

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| Mean Well GST60A12-P1J 12 V 5 A desktop supply | 1 | Digi-Key | https://www.digikey.com/en/products/detail/mean-well-usa-inc/GST60A12-P1J/7703712 | $19.40 | $19.40 | 6,901 in stock | 5.5×2.1 mm barrel, cULus. Needs an IEC C13 cord (~$5). |
| Pololu D36V50F5 5 V 5.5 A step-down (servo rail) | 1 | Pololu | #4091 · https://www.pololu.com/product/4091 | $39.95 | $39.95 | 375 in stock today | Rationed; order early. Add the 2200 µF cap at its output. |
| Pololu D24V22F5 5 V 2.5 A step-down (Pi rail) | 1 | Pololu | #2858 · https://www.pololu.com/product/2858 | $26.95 | $26.95 | 111 in stock today | Fixed 5.0 V output. |
| Panasonic EEU-FR1A222L 2200 µF 10 V low-ESR | 1 | Digi-Key | https://www.digikey.com/en/products/result?keywords=EEU-FR1A222L | $1.46 | $1.46 | In stock | At the servo-bus head. |
| Silicone wire: 28 AWG 10-wire ribbon 1 m + 22 AWG 2-wire | 1 | Adafruit / Amazon | Adafruit 3890 $3.95 · BNTECHGO 22 AWG kit ≈$12 | $16.00 | $16.00 | 3890 in stock; 22 AWG Adafruit 6180 OOS | 22 AWG pair = the yaw clock spring; 28 AWG ribbon = head harness. |
| JST-PH 2.0 connector kit (220 pc) | 1 | Adafruit | 4422 · https://www.adafruit.com/product/4422 | $8.95 | $8.95 | In stock | Head harness connector at the neck ring. |
| Panel-mount 2.1 mm DC barrel jack | 1 | SparkFun | PRT-00119 · https://www.sparkfun.com/dc-barrel-power-jack-connector.html | $1.75 | $1.75 | In stock | No reputable magnetic breakaway adapter was found. Use a right-angle plug plus a cable anchor (Velcro tie-down on the desk) as the cord-yank mitigation. |

## Mechanical

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| 61810-2RS thin-section bearing 50×65×7 (Tritan) | 1 | Zoro | G2727630 · https://www.zoro.com/tritan-radial-ball-bearing-ps-50mm-61810-2rs-61810-2rs-prx/i/G2727630/ | $16.39 | $16.39 | In stock | 61810 = 6810, same 50×65×7. eBay import $3.74 if you can wait. |
| igus Drylin RJ4JP-01-08 plain bushing (3-pack) | 1 | Ultimate 3D Printing Store | https://ultimate3dprintingstore.com/products/igus-drylin-rj4jp-01-08-bearing-1-piece | $8.50 | $8.50 | Some packs sold out; single $2.95 | Press fit in a 15 H7 bore; needs an 8.00 h8 shaft — cheap 7.95 rods rattle. |
| 8 mm hardened chromed shaft, 100 mm (cut to 63) | 1 | Amazon / BearingsCanada | Coavoo 2-pk ASIN B0DKSZMPZ2 (price n/f) · 5-pk CAD $28.54 https://bearingscanada.com/products/8mm-100mm-hardened-linear-motion-shafts | $12.00 | $12.00 | Amazon live price not retrievable | Estimate; buy HRC60 chromed, check 8.00 mm with calipers. |
| Steel universal joint coupler 5×5 mm bore (Ø11×22, M4 grubs), 2-pack | 1 | Amazon | HobbySoar ASIN B0782WB5Q1 | $9.00 | $9.00 | Price estimate (page didn't show) | Imports are Ø11×22–23, not Ø10×24 — CAD params updated to 11×23. Pin the bores with the Ø5 dowels and use the grub screws as backup. |
| Ø5×20 mm steel dowel pins, 25-pack | 1 | Zoro | G3424377 · https://www.zoro.com/i/G3424377/ | $3.25 | $3.25 | In stock | Carrier and plate pins for the U-joint; also the yaw pulley stub. m6 oversize: print 4.8 mm holes and ream. |
| Align 450 linkage ball set, 4.75 mm (H45Z002XXT) | 1 | HeliDirect | https://helidirect.com/search?q=H45Z002XXT | $7.99 | $7.99 | In stock | Mixed M2/M2.5 threads in the set — drill the ears for the M2 ones. Rods: Align H45047 is the ROD set ($3.99, OOS Vortex). |
| Align 450 ball links ×12 (H45045) or CopterX equivalent | 1 | Vortex Hobbies / eBay | AGNH45045 $3.29 (OOS) · eBay 127290105452 $4.86 | $4.86 | $4.86 | Buy the eBay set if Vortex still OOS | Socket swing not published; expect ±25–30°. |
| M2×0.4 stainless all-thread, 1 m | 1 | Zoro | G0319116 · https://www.zoro.com/zoro-select-fully-threaded-rod-m2-04mm-1-m-stainless-steel-18-8-plain-finish-m510700201000/i/G0319116/ | $8.19 | $8.19 | In stock | Cut three 45 mm pushrods. |
| GT2 6 mm closed belt 130T / 260 mm | 1 | Amazon / eBay | e.g. eBay 283194907394 (choose 260 mm) | $5.00 | $5.00 | Common size | CAD changed from 136T (eBay-only) to 130T with a 20T pulley at r 49.8: common stock length, no idler. |
| GT2 20T pulley, 6 mm belt, 5 mm bore | 1 | Amazon | any 20T/5 mm-bore aluminium pulley (often 2–5 packs, $8–10) | $9.00 | $9.00 | Common | Mounts on a Ø5 dowel pressed into the printed horn adapter. |
| M3 heat-set inserts (M3×4×5) 100-pk + M4 inserts 50-pk | 1 | 3DJake (CNC Kitchen) / Amazon (ruthex) | CNC Kitchen M3 $9.24–11.54 https://www.3djake.com/cnc-kitchen/threaded-inserts-m3-standard · ruthex M4 50-pk $9.99 | $21.00 | $21.00 | In stock | Six M3 on the shell split, four at the neck, three in the clamp ring; two M4 for the eye screws. |
| M2–M5 stainless socket screw kit with nuts (1290 pc) | 1 | Home Depot | MYWISH SF-TZ00005 · https://homedepot.com/p/334334772 | $22.72 | $22.72 | In stock | Covers M2 horn/paddle/cradle screws, M3 everything else, includes M2 nuts. |
| M4×5 cup-point set screws (grub for the shaft boss), 100-pk | 1 | Zoro | G9899246 · https://www.zoro.com/zoro-select-socket-set-screw-gr-m4-cup-5mm-l-pk100-m078400400005/i/G9899246/ | $4.05 | $4.05 | In stock |  |
| Steel ballast: 4.5 in × 1/8 in discs (Wagner D240) ×2 | 2 | Wagner | D240 · https://shop.wagnercompanies.com/disk-d240 | $5.33 | $10.66 | In stock | ≈256 g each → 512 g; the tray pocket in `params.py` is sized for these (Ø114.3 × 3.2). |
| Rubber feet Ø10 ×4, PTFE/UHMW glide pads ×3 | 1 | Amazon / Walmart | uxcell 10×2 mm 100-pk; UHMW tape WOD SPT5A $19.99 or PTFE furniture glides ~$3 | $8.00 | $8.00 | Common | Furniture glides are the cheap route for the three bearing-rock pads. |
| PETG 1 kg + TPU 95A 1 kg | 1 | Amazon | Overture PETG $15.99–19.99 · Overture/Sunlu TPU $18–23 | $38.00 | $38.00 | Common | ~400 g PETG for the parts; TPU for servo pads and park bumpers. |

## Soft goods

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| Shannon Luxe Cuddle Seal, Natural (off-white), 1 yd | 1 | Missouri Star Quilt Co | lcsealnatural · https://www.missouriquiltco.com/products/cuddle-luxe-seal-natural-60-minky-yardage | $24.92 | $24.92 | In stock | Knit backing, 20–30 % crosswise stretch. Pile listed as 10 mm (MSQC) vs 15 mm (Linda's) — order a swatch first. Cheaper non-stretch alt: Fabricis FAB-1200 10 mm 'Egg Shell' $12.80/yd from Korea. |
| Cuddle 3 minky, Ivory (face panel), ½ yd | 1 | Linda's / Fat Quarter Shop | C3-IVORY · https://www.lindas.com/products/quilting-cuddle-solid-ivory-fabric-per-yard | $7.74 | $7.74 | FQS OOS today; Linda's $10.15/yd sale | 3 mm pile. Stabilise with knit interfacing. |
| Cuddle 3 minky, Desert Rose (cheeks), ½ yd | 1 | Fat Quarter Shop | C3-DESERTROSE · https://www.fatquartershop.com/cuddle-desert-rose-solid-yardage | $7.74 | $7.74 | In stock | Dusty warm pink. |
| Open-cell PU foam 24×24×½ in | 1 | Zoro | 5GCU3 · https://www.zoro.com/i/G1977297/ | $18.95 | $18.95 | In stock | No 3/8 in open-cell sheet found; shave to 10 mm or accept ½ in and reduce the air gap in params. |
| Power mesh white ½ yd + 1 in knit elastic 3 yd | 1 | Nick of Time / Dritz | SKU 7150 $13.75/yd · Dritz 9518 $5.79 | $12.67 | $12.67 | In stock | Under-tube keeping fur off the pushrods; elastic at both ends. |
| YKK 9 in invisible zipper, Natural | 1 | Sewing Parts Online | https://www.sewingpartsonline.com/products/unique-9in-invisible-zipper-ykk | $2.99 | $2.99 | In stock | No ivory shade; Natural is closest. |
| Gütermann Mara 70 heavy poly thread | 1 | Ripstop by the Roll | https://ripstopbytheroll.com/products/gutermann-mara-70 | $4.75 | $4.75 | In stock | Confirm white/natural colour; Extra Strong is a drop-in. |
| Eyes: 10 mm Czech glass cabochons, Jet (5-pk) + M4×10 pan-head screws (50-pk) | 1 | Potomac Beads / Zoro | https://potomacbeads.com/czech-cabochons-jet-10mm-pack-of-5 ≈$2.99 · Midwest Fastener 51544 $5.59 | $8.58 | $8.58 | In stock | No true threaded-shank 10 mm toy eyes exist; 'threaded post' listings are ribbed safety-eye posts. Epoxy a cabochon to the screw head; drill the camera pupil through one. |
| Prototype plush: Jellycat Bashful Cream Bunny, Medium | 1 | The Cross Living / Pacifier Kids | SKU 210000017584 · https://www.thecrossliving.com/en-us/products/bashful-cream-bunny-med | $33.00 | $33.00 | In stock | No current retail 8 in cream Squishmallow; Carmen the Cream Kitty is eBay-only ($10–18). Bashful body is the right bean. |

## Tools

| Item | Qty | Vendor | SKU / URL | Unit | Ext. | Status | Notes |
|---|---|---|---|---|---|---|---|
| Wahl Pocket Pro trimmer (3 / 4.5 mm combs) + Frisco slicker brush | 1 | Chewy | https://www.chewy.com/wahl-pocket-pro/dp/151806 $15.99 · slicker $5.99 | $21.98 | $21.98 | In stock | Only if you shear a face panel instead of using the minky insert. |
| 3M Super 77 + Static Guard + Dritz Fray Check | 1 | Zoro / Walmart | Super 77 $16.89 · Static Guard $5.22 · Fray Check $3.47 | $25.58 | $25.58 | In stock | Super 77 is foam-safe (not EPS). |

## Sources
Vendor product pages linked in the tables (ROBOTIS US and e-Manual, RobotShop, Waveshare, Seeed Studio and wiki, PiShop.us, Adafruit, SparkFun, Digi-Key, Pololu, Zoro, VXB, Ultimate 3D Printing Store, HeliDirect, Vortex Hobbies, Missouri Star, Linda's, Fat Quarter Shop, Nick of Time, Potomac Beads, The Cross Living, Chewy), checked 30 Oct 2026 by four parallel research passes.
