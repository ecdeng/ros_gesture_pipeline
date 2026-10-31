"""Generate SVG mocks for the Jolly-bot deck. All drawings in px; technical drawings at 4 px/mm."""
import math, os
OUT = os.path.dirname(os.path.abspath(__file__))
CREAM="#F3EADA"; CREAM_D="#DCCDB3"; CREAM_L="#FBF6EC"; INK="#2B2622"; PINK="#E9A3AE"; TEAL="#3C7A89"
STEEL="#8A8F98"; DARK="#3A332E"; PETG="#B9D6DE"; SERVO="#2F3A44"; RED="#C8553D"; AMBER="#E0A458"

DEFS = f'''<defs>
<filter id="fuzz" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2"/></filter>
<radialGradient id="furG" cx="42%" cy="35%" r="70%"><stop offset="0" stop-color="{CREAM_L}"/><stop offset="0.7" stop-color="#F1E7D4"/><stop offset="1" stop-color="{CREAM_D}"/></radialGradient>
<radialGradient id="cheekG"><stop offset="0" stop-color="{PINK}" stop-opacity="0.95"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
<radialGradient id="cheekHot"><stop offset="0" stop-color="#F28AA0" stop-opacity="1"/><stop offset="1" stop-color="#F28AA0" stop-opacity="0"/></radialGradient>
<radialGradient id="eyeG" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#4A4A4A"/><stop offset="0.6" stop-color="#151515"/><stop offset="1" stop-color="#000"/></radialGradient>
</defs>'''

EGG = "M100 20 C162 20 180 84 180 134 C180 188 152 210 100 210 C48 210 20 188 20 134 C20 84 38 20 100 20 Z"

def bot(x=0, y=0, s=1.0, pitch=0, roll=0, heave=0, arm_l=18, arm_r=-18, cheek=0.0, back=False, shadow=True, feet=True, pivot=False):
    """A bot in a 200x240 local box. Only the upper body (above the pivot at local y 120 = h 90) rolls; pitch is shown as the
    face sliding down/up with slight foreshortening; heave lifts the upper body only (px). back=True draws the rear view."""
    g=[]
    g.append(f'<g transform="translate({x} {y}) scale({s})">')
    if shadow:
        g.append(f'<ellipse cx="100" cy="213" rx="66" ry="6" fill="{INK}" opacity="0.18" filter="url(#soft)"/>')
        g.append(f'<ellipse cx="100" cy="211" rx="60" ry="5" fill="{DARK}"/>')
    # body (puck sleeve + head drawn as one egg; the head part is clipped above the pivot and transformed)
    g.append(f'<clipPath id="cpL{x}{y}"><rect x="-20" y="112" width="240" height="140"/></clipPath>')
    g.append(f'<clipPath id="cpU{x}{y}"><rect x="-20" y="-20" width="240" height="134"/></clipPath>')
    g.append(f'<path d="{EGG}" fill="url(#furG)" filter="url(#fuzz)" clip-path="url(#cpL{x}{y})"/>')
    if feet and not back:
        g.append(f'<ellipse cx="76" cy="207" rx="14" ry="7" fill="#EFE4D0" filter="url(#fuzz)"/>')
        g.append(f'<ellipse cx="124" cy="207" rx="14" ry="7" fill="#EFE4D0" filter="url(#fuzz)"/>')
    # upper body group: roll about pivot (100,120), heave up
    g.append(f'<g transform="translate(0 {-heave}) rotate({roll} 100 120)">')
    g.append(f'<g transform="translate(44 126) rotate({arm_l})"><ellipse rx="20" ry="12.5" fill="#EFE4D0" stroke="{CREAM_D}" stroke-width="0.6" filter="url(#fuzz)"/></g>')
    g.append(f'<g transform="translate(156 126) rotate({arm_r})"><ellipse rx="20" ry="12.5" fill="#EFE4D0" stroke="{CREAM_D}" stroke-width="0.6" filter="url(#fuzz)"/></g>')
    # skirt overlap band (slightly brighter) and head
    g.append(f'<path d="{EGG}" fill="url(#furG)" filter="url(#fuzz)" clip-path="url(#cpU{x}{y})"/>')
    if not back:
        fy = pitch*0.6; fs = 1 - abs(pitch)*0.003
        g.append(f'<g transform="translate(100 {97+fy}) scale(1 {fs:.3f}) translate(-100 -97)">')
        r = 15 + 4*cheek
        grad = "cheekHot" if cheek>0.5 else "cheekG"
        g.append(f'<circle cx="63" cy="105" r="{r}" fill="url(#{grad})"/><circle cx="137" cy="105" r="{r}" fill="url(#{grad})"/>')
        g.append(f'<circle cx="75" cy="97" r="5.5" fill="url(#eyeG)"/><circle cx="125" cy="97" r="5.5" fill="url(#eyeG)"/>')
        g.append(f'<circle cx="73.2" cy="95" r="1.6" fill="#fff"/><circle cx="123.2" cy="95" r="1.6" fill="#fff"/>')
        g.append(f'<path d="M90 121 Q100.5 127.5 110 120.5" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>')
        g.append('</g>')
    g.append('</g>')
    if pivot:
        g.append(f'<line x1="14" y1="120" x2="186" y2="120" stroke="{RED}" stroke-width="0.8" stroke-dasharray="3 3" opacity="0.7"/>')
    g.append('</g>')
    return "\n".join(g)

def svg(w, h, body, label=None, scale=1.0):
    al = f' aria-label="{label}"' if label else ''
    W,H=int(round(w*scale)),int(round(h*scale))
    inner = body if scale==1.0 else f'<g transform="scale({scale})">{body}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"{al}>\n{DEFS}\n{inner}\n</svg>\n'

def write(name, content):
    p = os.path.join(OUT, name); open(p,'w').write(content); print(name, len(content)//1024, 'KB')

# 1. hero front view (used on cover + spec slide)
write('bot_front.svg', svg(200, 240, bot(), 'Front view of the cream fluffy bean robot with beady eyes, pink cheeks and a tiny smile', scale=3.0))
write('bot_small.svg', svg(200, 240, bot(), 'The robot', scale=1.6))
write('bot_mid.svg', svg(200, 240, bot(), 'Front view of the robot', scale=2.0))

# 2. pose sheet: 5 poses in a row, each 200x240 box scaled 1.4 -> 280x336
poses = [
    dict(pivot=True),
    dict(pitch=15, cheek=0.3, pivot=True),
    dict(roll=-16, pivot=True),
    dict(arm_l=-70, arm_r=70, heave=6, cheek=1.0, pivot=True),
    dict(back=True, pivot=True),
]
parts=[]
for i,p in enumerate(poses):
    parts.append(bot(x=20+i*330, y=0, s=1.4, **p))
write('poses.svg', svg(1664, 340, "\n".join(parts), 'Five poses: idle, lean in, head cock, celebrate, sleep (turned away); dotted line = tilt pivot'))

# ---------------------------------------------------------------- cutaway (front view), 3.8 px/mm, 760x800
S=3.8
def P(x,h): return (380+S*x, 780-S*h)
def pt(x,h): a=P(x,h); return f"{a[0]:.1f} {a[1]:.1f}"
def rect(x0,x1,h0,h1,fill,stroke=INK,sw=1.5,rx=2,extra=""):
    (X0,Y1)=P(x0,h0); (X1,Y0)=P(x1,h1)
    return f'<rect x="{X0:.1f}" y="{Y0:.1f}" width="{X1-X0:.1f}" height="{Y1-Y0:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def line(x0,h0,x1,h1,stroke=INK,sw=1.5,dash=""):
    (X0,Y0)=P(x0,h0); (X1,Y1)=P(x1,h1)
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{X0:.1f}" y1="{Y0:.1f}" x2="{X1:.1f}" y2="{Y1:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}/>'

def egg_path(scale_r=1.0, hmin=12, hmax=198):
    k=scale_r
    return (f"M {pt(0,hmax)} C {pt(60*k,hmax)} {pt(80*k,150)} {pt(80*k,76)} C {pt(80*k,40)} {pt(78*k,hmin)} {pt(60*k,hmin)} "
            f"L {pt(-60*k,hmin)} C {pt(-78*k,hmin)} {pt(-80*k,40)} {pt(-80*k,76)} C {pt(-80*k,150)} {pt(-60*k,hmax)} {pt(0,hmax)} Z")

def cutaway():
    g=[]
    g.append(f'<line x1="0" y1="780" x2="760" y2="780" stroke="{INK}" stroke-width="2"/>')
    g.append(f'<path d="{egg_path(1.0)}" fill="{CREAM}" stroke="#B9A98C" stroke-width="2.5" filter="url(#fuzz)"/>')
    g.append(f'<path d="{egg_path(0.87, 22, 188)}" fill="#F7E7B8" stroke="none" opacity="0.9"/>')   # foam
    g.append(f'<path d="{egg_path(0.74, 32, 178)}" fill="#FBFBF8" stroke="none"/>')                # cavity
    # ---- static floor disc (h 0-14)
    g.append(rect(-65,65,0,14,"#E6E1D8"))
    g.append(rect(-55,55,0,6,STEEL,sw=1))                                   # steel discs
    g.append(rect(-32.5,32.5,7,14,"#C9CDD3",sw=1)); g.append(rect(-25,25,7,14,"#FBFBF8",sw=1))  # 6810 bearing w/ bore
    for sgn in (-1,1): g.append(rect(sgn*38,sgn*40.5,14,21,"#9AA3AE",sw=1,rx=0))               # static GT2 ring
    g.append(rect(56,65,3,12,INK,sw=1))                                     # 12 V breakaway jack
    # ---- puck bowl (h 14-70): Ø112 at bottom -> Ø128 above h 20
    g.append(f'<path d="M {pt(-56,14)} L {pt(56,14)} L {pt(64,22)} L {pt(64,70)} L {pt(-64,70)} L {pt(-64,22)} Z" fill="{PETG}" stroke="{INK}" stroke-width="1.5"/>')
    g.append(f'<path d="M {pt(-53,17)} L {pt(53,17)} L {pt(61,24)} L {pt(61,68)} L {pt(-61,68)} L {pt(-61,24)} Z" fill="#FBFBF8" stroke="none"/>')
    # tilt servos standing (two visible at x=+-43), horn axis at h 37, ball at r 30
    for sgn in (-1,1):
        g.append(rect(sgn*50-10, sgn*50+10, 17, 51, SERVO, sw=1))
        g.append(line(sgn*50, 37, sgn*30, 37, stroke=AMBER, sw=4))
        g.append(f'<circle cx="{P(sgn*30,37)[0]:.1f}" cy="{P(sgn*30,37)[1]:.1f}" r="4" fill="{RED}"/>')
        g.append(line(sgn*30, 37, sgn*30, 97, stroke=STEEL, sw=3))
        g.append(f'<circle cx="{P(sgn*30,97)[0]:.1f}" cy="{P(sgn*30,97)[1]:.1f}" r="4" fill="{RED}"/>')
        g.append(rect(sgn*30-2, sgn*30+2, 90, 99, PETG, sw=1))             # plate ear
    # yaw servo horn-down at r 53 (drawn ghosted, behind) + pulley below the floor, belt to the ring
    g.append(rect(-62,-44,18,52,SERVO,sw=1,extra='opacity="0.35"'))
    g.append(rect(-62,-44,14,18,AMBER,sw=1,extra='opacity="0.7"'))
    g.append(line(-44,15.5,-40.5,15.5,stroke=INK,sw=2)); g.append(line(-44,20,-40.5,20,stroke=INK,sw=2))
    # upper storey: Pi + HAT (ghost) and speaker
    g.append(rect(-32,32,52,68,"#2E7D5B",sw=1,extra='opacity="0.5"'))
    g.append(f'<circle cx="{P(48,58)[0]:.1f}" cy="{P(48,58)[1]:.1f}" r="{10*S:.1f}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>')
    # shaft, carrier, U-joint, spine plate / neck ring
    g.append(rect(-4,4,17,76,STEEL,sw=1,rx=1))
    g.append(rect(-8,8,50,86,PETG,sw=1))                                   # LM8LUU carrier
    g.append(f'<circle cx="{P(0,90)[0]:.1f}" cy="{P(0,90)[1]:.1f}" r="9" fill="{STEEL}" stroke="{INK}" stroke-width="1.5"/>')
    g.append(rect(-38,38,96,100,PETG))                                      # spine plate Ø76
    # head shell: neck Ø76 at h 95 -> Ø108 at 100-130 -> crown
    g.append(f'<path d="M {pt(-38,96)} C {pt(-58,104)} {pt(-56,170)} {pt(0,190)} C {pt(56,170)} {pt(58,104)} {pt(38,96)}" fill="none" stroke="{TEAL}" stroke-width="3"/>')
    # face plate, eyes, cheeks, camera, MPR121
    g.append(rect(-40,40,108,138,PETG,sw=1,extra='opacity="0.7"'))
    for sgn in (-1,1):
        g.append(f'<circle cx="{P(sgn*25,123)[0]:.1f}" cy="{P(sgn*25,123)[1]:.1f}" r="{5.5*S:.1f}" fill="url(#eyeG)"/>')
        g.append(f'<circle cx="{P(sgn*37,115)[0]:.1f}" cy="{P(sgn*37,115)[1]:.1f}" r="{7*S:.1f}" fill="url(#cheekG)"/>')
    g.append(rect(-33,-17,113,127,"#2E7D5B",sw=1))
    g.append(rect(-14,14,140,150,"#2E7D5B",sw=1))
    # arm servos + paddles + arms
    for sgn in (-1,1):
        g.append(rect(sgn*52-10, sgn*52+10, 100, 120, SERVO, sw=1))
        g.append(line(sgn*62,110, sgn*84,106, stroke=AMBER, sw=4))
        g.append(f'<ellipse cx="{P(sgn*94,104)[0]:.1f}" cy="{P(sgn*94,104)[1]:.1f}" rx="{20*S:.1f}" ry="{12.5*S:.1f}" transform="rotate({-sgn*18} {P(sgn*94,104)[0]:.1f} {P(sgn*94,104)[1]:.1f})" fill="#EFE4D0" stroke="{CREAM_D}" stroke-width="1" filter="url(#fuzz)"/>')
    # soft skirt from neck down over the puck sleeve
    for sgn in (-1,1):
        g.append(f'<path d="M {pt(sgn*66,82)} L {pt(sgn*66,70)}" fill="none" stroke="#E8DCC4" stroke-width="10" stroke-linecap="round"/>')   # sleeve collar to h 82
        g.append(f'<path d="M {pt(sgn*42,95)} C {pt(sgn*66,90)} {pt(sgn*74,60)} {pt(sgn*73,33)}" fill="none" stroke="{CREAM_D}" stroke-width="7" stroke-linecap="round" opacity="0.95"/>')
    # power-mesh tube (dashed) from neck to lid
    for sgn in (-1,1):
        g.append(line(sgn*40,94, sgn*58,70, stroke=TEAL, sw=1.5, dash="4 4"))
    # crown touch pad
    g.append(f'<path d="M {pt(-30,186)} C {pt(-15,192)} {pt(15,192)} {pt(30,186)}" fill="none" stroke="{TEAL}" stroke-width="5" stroke-dasharray="6 5"/>')
    # pivot marker
    g.append(line(-80,90,80,90,stroke=RED,sw=1,dash="6 6"))
    callouts=[
        ("Crown touch pad (conductive fabric, snap-connected)", 22,187,  60),
        ("Head shell: two PETG half-shells, 10 mm foam, fur",  58,150, 115),
        ("Face plate: M4 threaded eyes, camera pupil, cheek LEDs", 40,123, 170),
        ("Arm servo + fabric-hinged paddle",                  62,110, 225),
        ("Pivot h 90: pinned 5×5 U-joint on an igus bushing", 9,90,  280),
        ("Spine plate Ø76 with 3 tangential ball studs",      38,98,  335),
        ("Pushrods M2 × 60 mm → horn arms r 20",              30,70,  390),
        ("Skirt (to h 33) over sleeve collar (to h 82)",       73,45,  445),
        ("Upper storey: Pi Zero 2 W + 2-Mic HAT, speaker",    32,60,  500),
        ("Tilt servos ×3 standing, horn axis h 37",           60,30,  555),
        ("Yaw servo + 30T pulley → static 120T GT2 ring",    -39,17,  610),
        ("6810 bearing, hall-sensor home, 450 g steel, breakaway jack", 58,8, 665),
    ]
    rows=[]
    for name,x,h,ly in callouts:
        X,Y=P(x,h)
        g.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="4" fill="{TEAL}"/>')
        g.append(f'<path d="M {X:.1f} {Y:.1f} L 700 {ly} L 756 {ly}" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity="0.8"/>')
        rows.append((name,ly))
    return "\n".join(g), rows

body, rows = cutaway()
write('cutaway.svg', svg(760, 800, body, 'Front cutaway of the robot showing skin, foam, head cage, face plate, arm servos, tilt platform, puck with servos, and the static floor', scale=0.85))
import json; json.dump([(n, ly*0.85) for n,ly in rows], open(os.path.join(OUT,'cutaway_labels.json'),'w'))

# ---------------------------------------------------------------- puck top view, 4 px/mm, 600x600, centre (300,300), front = down
def T(x,y): return (300+4*x, 300+4*y)
def rrect_rot(cx,cy,w,h,ang,fill,stroke=INK,sw=1.2,rx=3,extra=""):
    X,Y=T(cx,cy); return f'<rect x="{X-2*w:.1f}" y="{Y-2*h:.1f}" width="{4*w}" height="{4*h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" transform="rotate({ang} {X:.1f} {Y:.1f})" {extra}/>'
def puck_top():
    g=[]
    cx,cy=T(0,0)
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*76}" fill="{CREAM}" stroke="#B9A98C" stroke-width="2" filter="url(#fuzz)"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*64}" fill="{PETG}" stroke="{INK}" stroke-width="1.5"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*61}" fill="#FBFBF8" stroke="none"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*39}" fill="none" stroke="#9AA3AE" stroke-width="6" stroke-dasharray="3 3"/>')   # static GT2 ring below floor
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*32.5}" fill="none" stroke="#C9CDD3" stroke-width="2" stroke-dasharray="3 5"/>')  # 6810 bearing OD
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*25}" fill="none" stroke="#C9CDD3" stroke-width="2" stroke-dasharray="3 5"/>')    # bore
    for az in (90,210,330):
        a=math.radians(az); r=50
        sx,sy=r*math.cos(a), r*math.sin(a)
        g.append(rrect_rot(sx,sy,20,23,az,SERVO))
        bx,by=30*math.cos(a),30*math.sin(a)
        X0,Y0=T(sx,sy); X1,Y1=T(bx,by)
        g.append(f'<line x1="{X0:.1f}" y1="{Y0:.1f}" x2="{X1:.1f}" y2="{Y1:.1f}" stroke="{AMBER}" stroke-width="5" stroke-linecap="round"/>')
        g.append(f'<circle cx="{X1:.1f}" cy="{Y1:.1f}" r="5" fill="{RED}"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*38}" fill="none" stroke="{TEAL}" stroke-width="2" stroke-dasharray="8 6"/>')  # spine plate Ø76 above
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*7.5}" fill="{PETG}" stroke="{INK}" stroke-width="1.2"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*4}" fill="{STEEL}" stroke="{INK}" stroke-width="1.2"/>')
    # yaw servo horn-down at r 53, azimuth 150; pulley PD 19 touching the ring at r 39 -> pulley centre r = 39+9.5+~4 = 53
    a=math.radians(150); yx,yy=53*math.cos(a),53*math.sin(a)
    g.append(rrect_rot(yx,yy,20,23,150,SERVO))
    X,Y=T(yx,yy); g.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{4*9.5}" fill="none" stroke="{AMBER}" stroke-width="3"/>')
    # belt: wraps the static ring (r 39.5) and the pulley (r 10.5 incl. belt), external tangents
    R1=4*39.5; R2=4*10.5; d=math.hypot(X-cx,Y-cy); ang=math.atan2(Y-cy,X-cx); off=math.acos((R1-R2)/d)
    pts=[]
    for sgn in (1,-1):
        t=ang+sgn*off
        pts.append(((cx+R1*math.cos(t), cy+R1*math.sin(t)),(X+R2*math.cos(t), Y+R2*math.sin(t))))
    (a1,b1),(a2,b2)=pts
    g.append(f'<path d="M {a1[0]:.1f} {a1[1]:.1f} L {b1[0]:.1f} {b1[1]:.1f} A {R2:.1f} {R2:.1f} 0 0 0 {b2[0]:.1f} {b2[1]:.1f} L {a2[0]:.1f} {a2[1]:.1f} A {R1:.1f} {R1:.1f} 0 1 0 {a1[0]:.1f} {a1[1]:.1f} Z" fill="none" stroke="{INK}" stroke-width="2.5" opacity="0.6"/>')
    # Pi + HAT upper storey (ghost), tangential at back (azimuth 270) r 23-62 -> centre r 42
    g.append(rrect_rot(0,-42,65,30,0,"#2E7D5B",stroke=INK,sw=2,extra='opacity="0.55" stroke-dasharray="6 4"'))
    # OpenRB upper storey gap 2 (azimuth 30), speaker gap 3 (azimuth 150 side -> use 60)
    a=math.radians(30); g.append(rrect_rot(50*math.cos(a),50*math.sin(a),50,22,30+90,"#1F5F8B",stroke=INK,sw=2,extra='opacity="0.6" stroke-dasharray="6 4"'))
    a=math.radians(62); X,Y=T(48*math.cos(a),48*math.sin(a)); g.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{4*14}" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="4 3"/>')
    # bucks lower storey in gaps
    a=math.radians(190); g.append(rrect_rot(55*math.cos(a),55*math.sin(a),20,10,190+90,"#6B4FA0"))
    a=math.radians(250); g.append(rrect_rot(56*math.cos(a),56*math.sin(a),14,10,250+90,"#6B4FA0"))
    X,Y=T(0,68); g.append(f'<path d="M {X-10} {Y-4} L {X+10} {Y-4} L {X} {Y+10} Z" fill="{INK}"/>')
    callouts=[("Tilt servo ×3 standing, horn axis tangential at r 50", 50*math.cos(math.radians(330))+10, 50*math.sin(math.radians(330))-10, 60),
              ("Horn arm r 20 → ball stud at r 30 (plate ears above)", 30*math.cos(math.radians(330)), 30*math.sin(math.radians(330)), 130),
              ("8 mm shaft + LM8LUU carrier + U-joint", 7, 0, 200),
              ("OpenRB-150 (upper storey)", 50*math.cos(math.radians(30))+6, 50*math.sin(math.radians(30))+6, 270),
              ("Speaker 28 mm, front wall", 48*math.cos(math.radians(62))+10, 48*math.sin(math.radians(62))+10, 340),
              ("Pi Zero 2 W + 2-Mic HAT (upper storey, back)", 30, -42, 410),
              ("Yaw servo horn-down, 30T pulley, GT2 belt", 53*math.cos(math.radians(150))-6, 53*math.sin(math.radians(150))-8, 480),
              ("Static 120T GT2 ring r 38–40, 6810 bearing, hall magnet at r 35 (below floor)", 39*math.cos(math.radians(235)), 39*math.sin(math.radians(235)), 550)]
    rows=[]
    for name,x,y,ly in callouts:
        X,Y=T(x,y)
        g.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="4" fill="{TEAL}"/>')
        g.append(f'<path d="M {X:.1f} {Y:.1f} L 620 {ly} L 676 {ly}" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity="0.85"/>')
        rows.append((name,ly))
    return "\n".join(g), rows
body, rows = puck_top()
write('puck_top.svg', svg(680, 600, body, 'Top view of the puck: three tilt servos at 120 degrees with horn arms to the spine plate balls, central shaft, yaw servo with belt pulley, Pi, OpenRB, bucks and speaker', scale=0.95))
json.dump([(n, ly*0.95) for n,ly in rows], open(os.path.join(OUT,'puck_labels.json'),'w'))

# ---------------------------------------------------------------- gore pattern (6 gores) from the egg profile, 1:1 in mm scaled 2.6 px/mm
def egg_r(h):
    """outer skin radius (mm) at height h for the v6 bean: r(12)=74, r(60..82)=80, crown 198 with R~62."""
    if h<=60:
        return math.sqrt(max(0.0, 80**2 - ((60-h)*80/152.6)**2))
    if h<=82: return 80.0
    t=(h-82)/(198-82); return 80*math.sqrt(max(0,1-t**2.6))
def gore():
    pts_r=[]; pts_l=[]; arc=0; prev=None
    hs=[198-i for i in range(0,189)]
    for h in hs:
        r=egg_r(h)
        if prev is not None:
            dh=1; dr=r-prev; arc+=math.sqrt(dh*dh+dr*dr)
        prev=r
        half=math.pi*r/6
        pts_r.append((half,arc)); pts_l.append((-half,arc))
    k=1.7; ox=200; oy=24
    d="M "+" L ".join(f"{ox+k*x:.1f} {oy+k*y:.1f}" for x,y in pts_r)+" L "+" L ".join(f"{ox+k*x:.1f} {oy+k*y:.1f}" for x,y in reversed(pts_l))+" Z"
    g=[f'<path d="{d}" fill="{CREAM}" stroke="{INK}" stroke-width="2"/>']
    # seam allowance 8 mm (dashed outline), drawn as a stroked copy offset by stroke width trick
    g.append(f'<path d="{d}" fill="none" stroke="{TEAL}" stroke-width="{2*8*k:.1f}" opacity="0.12"/>')
    # grain / pile arrows (pile runs crown→hem: arrows pointing up = toward crown at top? crown at arc=0 top)
    for yy in (140,240,340,440):
        g.append(f'<path d="M 200 {yy} l 0 -30 m -6 8 l 6 -8 l 6 8" fill="none" stroke="{INK}" stroke-width="1.5" opacity="0.6"/>')
    # eye position marks on the face gore: eye line h=118 -> arc at that h; eyes at ±25 mm around the body = ±25 on this gore (face centered on gore)
    arc_eye=next(a for (x,a),h in zip(pts_r,hs) if h<=123)
    for sx in (-25,25):
        g.append(f'<circle cx="{ox+k*sx:.1f}" cy="{oy+k*arc_eye:.1f}" r="{k*5.5:.1f}" fill="{INK}"/>')
    arc_mouth=next(a for (x,a),h in zip(pts_r,hs) if h<=98)
    g.append(f'<path d="M {ox-k*10:.1f} {oy+k*arc_mouth:.1f} Q {ox:.1f} {oy+k*(arc_mouth+6):.1f} {ox+k*10:.1f} {oy+k*arc_mouth:.1f}" fill="none" stroke="{INK}" stroke-width="2"/>')
    # cheek circles
    for sx in (-37,37):
        g.append(f'<circle cx="{ox+k*sx:.1f}" cy="{oy+k*(arc_eye+8):.1f}" r="{k*15:.1f}" fill="url(#cheekG)"/>')
    # face panel (sheared ellipse 80x60) outline
    g.append(f'<ellipse cx="{ox}" cy="{oy+k*(arc_eye+10):.1f}" rx="{k*40:.1f}" ry="{k*30:.1f}" fill="none" stroke="{PINK}" stroke-width="2" stroke-dasharray="6 5"/>')
    # crown cap circle Ø25 at right
    g.append(f'<circle cx="520" cy="70" r="{k*12.5:.1f}" fill="{CREAM}" stroke="{INK}" stroke-width="2"/>')
    # arm gore (tube 40 long, 70 circumference) rectangle at right
    g.append(f'<rect x="480" y="130" width="{k*40:.0f}" height="{k*72:.0f}" rx="6" fill="{CREAM}" stroke="{INK}" stroke-width="2"/>')
    # dimension lines
    maxhalf=max(x for x,a in pts_r); total=arc
    g.append(f'<line x1="{ox-k*maxhalf:.1f}" y1="{oy+k*total+14:.1f}" x2="{ox+k*maxhalf:.1f}" y2="{oy+k*total+14:.1f}" stroke="{INK}" stroke-width="1"/>')
    g.append(f'<line x1="{ox+k*maxhalf+30:.1f}" y1="{oy}" x2="{ox+k*maxhalf+30:.1f}" y2="{oy+k*total:.1f}" stroke="{INK}" stroke-width="1"/>')
    return "\n".join(g), dict(width_mm=2*maxhalf, length_mm=total, eye_arc=arc_eye, k=k, ox=ox, oy=oy, maxhalf=maxhalf)
body, info = gore()
write('gore.svg', svg(640, 560, body, 'One of six gore pattern pieces for the fur skin, with eye, smile and cheek placement, seam allowance, pile direction, plus the crown cap and an arm tube'))
json.dump(info, open(os.path.join(OUT,'gore_info.json'),'w')); print(info)

# ---------------------------------------------------------------- shell offsets diagram (plan section through the head), 4 px/mm, 520x520
def offsets():
    cx,cy=260,260; g=[]
    layers=[(65,CREAM,"skin + 10 mm pile"),(55,"#F7E7B8","10 mm open-cell foam"),(45,"#FBFBF8","2 mm air gap"),(43,PETG,"1.6 mm PETG shell")]
    for r,fill,_ in layers:
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*r}" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*41.4}" fill="#FBFBF8" stroke="none"/>')
    # fuzzy outer edge
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{4*65}" fill="none" stroke="#B9A98C" stroke-width="3" filter="url(#fuzz)"/>')
    # dimension spokes to the right
    for r0,r1,yoff in ((65,55,-70),(55,45,-20),(45,43,30),(43,0,80)):
        pass
    # radial dimension line at 30deg
    a=math.radians(-30)
    for r,col in ((65,INK),(55,INK),(45,INK),(43,INK)):
        X,Y=cx+4*r*math.cos(a), cy+4*r*math.sin(a)
        g.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="3.5" fill="{TEAL}"/>')
        g.append(f'<path d="M {X:.1f} {Y:.1f} L 470 {Y:.1f} L 512 {Y:.1f}" fill="none" stroke="{TEAL}" stroke-width="1.5"/>')
    # split line of the two half-shells (vertical, dashed) and face plate (flat chord at front = bottom)
    g.append(f'<line x1="{cx}" y1="{cy-4*43}" x2="{cx}" y2="{cy+4*43}" stroke="{RED}" stroke-width="2" stroke-dasharray="8 6"/>')
    g.append(f'<rect x="{cx-4*40}" y="{cy+4*36}" width="{8*40}" height="{4*4}" rx="2" fill="{PETG}" stroke="{INK}" stroke-width="1.5"/>')
    # eye wells
    for sx in (-25,25):
        g.append(f'<circle cx="{cx+4*sx}" cy="{cy+4*38}" r="{4*8}" fill="#FBFBF8" stroke="{INK}" stroke-width="1.2"/>')
    # shoulder pockets at +-35deg from front (front = +y)
    for sgn in (-1,1):
        a=math.radians(90 - sgn*70)
        X,Y=cx+4*40*math.cos(a), cy+4*40*math.sin(a)
        g.append(f'<rect x="{X-40}" y="{Y-26}" width="80" height="52" rx="4" fill="{SERVO}" stroke="none" transform="rotate({-sgn*70} {X:.1f} {Y:.1f})" opacity="0.9"/>')
    g.append(f'<path d="M {cx-12} {cy+4*70} L {cx+12} {cy+4*70} L {cx} {cy+4*70+16} Z" fill="{INK}"/>')
    rows=[]
    a=math.radians(-30)
    for r,name in ((65,"Skin: fur backing + 8–12 mm pile"),(55,"10 mm open-cell foam jacket (squish)"),(45,"2 mm air gap"),(43,"1.6 mm PETG half-shell")):
        rows.append((name, cy+4*r*math.sin(a)))
    return "\n".join(g), rows
body, rows = offsets()
write('offsets.svg', svg(520, 520, body, 'Horizontal section through the head: fur skin, foam jacket, air gap and PETG shell, with the split line, face plate, eye wells and shoulder pockets'))
json.dump(rows, open(os.path.join(OUT,'offsets_labels.json'),'w')); print(rows)

def side_shapes(sc, ox, oy):
    """returns helper to map (x_mm front+, h_mm) to px with scale sc and origin (ox = axis x px, oy = table y px)"""
    def Q(x,h): return (ox+sc*x, oy-sc*h)
    def poly(points): return "M "+" L ".join(f"{Q(x,h)[0]:.1f} {Q(x,h)[1]:.1f}" for x,h in points)+" Z"
    return Q, poly
def side_pose(ox, oy, sc, pitch_down=0, label=None):
    Q,poly=side_shapes(sc,ox,oy); g=[]
    # ghost puck + floor
    g.append(f'<rect x="{Q(-64,70)[0]:.1f}" y="{Q(-64,70)[1]:.1f}" width="{sc*128:.1f}" height="{sc*56:.1f}" fill="none" stroke="{TEAL}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    g.append(f'<rect x="{Q(-65,14)[0]:.1f}" y="{Q(-65,14)[1]:.1f}" width="{sc*130:.1f}" height="{sc*14:.1f}" fill="#D8D2C6" stroke="{INK}" stroke-width="1"/>')
    g.append(f'<line x1="{ox-sc*95:.1f}" y1="{oy:.1f}" x2="{ox+sc*95:.1f}" y2="{oy:.1f}" stroke="{INK}" stroke-width="1.5"/>')
    # puck sleeve h 12..82 (static in tilt)
    hs=[12+i*2 for i in range(0,36)]
    pts=[(egg_r(h),h) for h in hs]+[(-egg_r(h),h) for h in reversed(hs)]
    g.append(f'<path d="{poly(pts)}" fill="{CREAM}" stroke="#B9A98C" stroke-width="1.5" filter="url(#fuzz)"/>')
    # head group rotated about pivot (0,90): head shape h 88..198 + skirt band h 33..95
    px,py=Q(0,90)
    g.append(f'<g transform="rotate({pitch_down} {px:.1f} {py:.1f})">')
    hs=[88+i*2 for i in range(0,56)]
    pts=[(egg_r(h),h) for h in hs]+[(-egg_r(h),h) for h in reversed(hs)]
    g.append(f'<path d="{poly(pts)}" fill="url(#furG)" stroke="#B9A98C" stroke-width="1.5" filter="url(#fuzz)"/>')
    for sgn in (1,-1):
        hs2=[33+i*2 for i in range(0,32)]
        band=[(sgn*(egg_r(h)+3),h) for h in hs2]+[(sgn*(egg_r(h)-8),h) for h in reversed(hs2)]
        g.append(f'<path d="{poly(band)}" fill="#EFE4D0" stroke="#B9A98C" stroke-width="1" opacity="0.95" filter="url(#fuzz)"/>')
    # eye + cheek on the front edge (x positive)
    ex,ey=Q(egg_r(123)-4,123); g.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{sc*5.5:.1f}" fill="url(#eyeG)"/>')
    cx_,cy_=Q(egg_r(115)-9,115); g.append(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{sc*13:.1f}" fill="url(#cheekG)"/>')
    # arm stub (near side) at h 110 angled down 18°
    ax,ay=Q(10,108); g.append(f'<ellipse cx="{ax:.1f}" cy="{ay:.1f}" rx="{sc*20:.1f}" ry="{sc*12.5:.1f}" transform="rotate(18 {ax:.1f} {ay:.1f})" fill="#EFE4D0" stroke="{CREAM_D}" stroke-width="1" filter="url(#fuzz)"/>')
    # neck ring + camera gaze line (camera tilted 18° up)
    g.append(f'<rect x="{Q(-38,96)[0]:.1f}" y="{Q(-38,96)[1]:.1f}" width="{sc*76:.1f}" height="{sc*4:.1f}" fill="{PETG}" stroke="{INK}" stroke-width="1"/>')
    gx,gy=Q(egg_r(123),123); g.append(f'<line x1="{gx:.1f}" y1="{gy:.1f}" x2="{gx+sc*60*math.cos(math.radians(18)):.1f}" y2="{gy-sc*60*math.sin(math.radians(18)):.1f}" stroke="{TEAL}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    g.append('</g>')
    # pivot marker
    g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{RED}"/>')
    g.append(f'<line x1="{ox-sc*85:.1f}" y1="{py:.1f}" x2="{ox+sc*85:.1f}" y2="{py:.1f}" stroke="{RED}" stroke-width="1" stroke-dasharray="5 5" opacity="0.7"/>')
    # front arrow
    g.append(f'<path d="M {ox+sc*70:.1f} {oy+14} L {ox+sc*84:.1f} {oy+14} L {ox+sc*84:.1f} {oy+9} L {ox+sc*92:.1f} {oy+17} L {ox+sc*84:.1f} {oy+25} L {ox+sc*84:.1f} {oy+20} L {ox+sc*70:.1f} {oy+20} Z" fill="{INK}" opacity="0.6"/>')
    return "\n".join(g)
sc=2.1; parts=[]
for i,ang in enumerate([0, 15, -25, -8]):
    parts.append(side_pose(ox=210+i*416, oy=470, sc=sc, pitch_down=ang))
write('sideview.svg', svg(1664, 500, "\n".join(parts), 'Side views at rest, 15 degrees down, 25 degrees up and 8 degrees drowsy, showing the pivot, the puck outline, the skirt draping over the sleeve, and the camera gaze line'))
