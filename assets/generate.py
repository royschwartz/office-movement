"""Generate the original instructional artwork. All drawing is code-native SVG."""
from pathlib import Path
from html import escape

OUT = Path(__file__).parent
C = {'paper':'#f6f3ec','shirt':'#204f46','pants':'#c77954','skin':'#d9aa89','hair':'#77776f','ink':'#223e37','pale':'#e5ece4','line':'#a9b7aa','band':'#b06d42'}

def path(d, fill='none', stroke=None, width=1.5, extra=''):
    return f'<path d="{d}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '')+f' {extra}/>'
def circle(x,y,r,fill,stroke=None,w=1.3):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{w}"' if stroke else '')+'/>'
def text(x,y,t,size=13,anchor='middle',weight=600,color=None):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color or C["ink"]}">{escape(t)}</text>'
def limb(points,color,width):
    d='M '+' L '.join(f'{x},{y}' for x,y in points)
    return path(d,stroke=C['ink'],width=width+2)+path(d,stroke=color,width=width)
def arrow(d):
    return path(d,stroke=C['band'],width=2.5,extra='marker-end="url(#arrow)"')
def label(x,y,t): return text(x,y,t,12,weight=700)
def floor(): return path('M 52,318 H 548',stroke=C['line'],width=1.2)
def chair(x,y=210,facing=1):
    # x is the back; the seat extends toward facing direction.
    return (path(f'M {x},{y-75} L {x},{y} H {x+facing*70}',stroke=C['line'],width=8)+
            path(f'M {x},{y} L {x-facing*8},313 M {x+facing*61},{y} L {x+facing*70},313',stroke=C['line'],width=6))
def wall(x):
    return f'<rect x="{x}" y="65" width="14" height="253" rx="4" fill="{C["pale"]}"/>'+path(f'M {x},65 V 318',stroke=C['line'],width=2)
def head(x,y,profile=0):
    # Head is ~40 px high, neck behind it; small facial marks communicate direction.
    s=limb([(x,y+13),(x,y+30)],C['skin'],13)
    s+=f'<ellipse cx="{x}" cy="{y}" rx="16" ry="20" fill="{C["skin"]}" stroke="{C["ink"]}" stroke-width="1.4"/>'
    s+=path(f'M {x-16},{y+1} Q {x-20},{y-19} {x-3},{y-22} Q {x+15},{y-22} {x+16},{y-7} Q {x+7},{y-12} {x-1},{y-13} Q {x-11},{y-7} {x-12},{y+3} Z',fill=C['hair'])
    if profile:
        s+=path(f'M {x+profile*14},{y-3} L {x+profile*21},{y+3} L {x+profile*15},{y+7}',fill=C['skin'],stroke=C['ink'],width=1.2)
        s+=circle(x+profile*10,y-3,1.6,C['ink'])
        s+=path(f'M {x+profile*9},{y+12} l {profile*5},0',stroke=C['ink'],width=1)
        s+=circle(x-profile*9,y+4,3.4,C['skin'])
    else:
        s+=circle(x-5,y-1,1.4,C['ink'])+circle(x+6,y-1,1.4,C['ink'])
        s+=path(f'M {x-4},{y+11} Q {x},{y+13} {x+4},{y+11}',stroke=C['ink'],width=1)
    return s

def arm(shoulder,elbow,hand):
    # Forearm remains visible; a short sleeve covers the upper third.
    sx,sy=shoulder; ex,ey=elbow
    cuff=(sx+(ex-sx)*.53, sy+(ey-sy)*.53)
    return limb([shoulder,elbow,hand],C['skin'],12)+limb([shoulder,cuff],C['shirt'],17)+circle(*hand,7,C['skin'],C['ink'])
def leg(hip,knee,ankle,shoe=1):
    ax,ay=ankle
    return limb([hip,knee,ankle],C['pants'],18)+path(f'M {ax-7},{ay-3} Q {ax+shoe*4},{ay-5} {ax+shoe*9},{ay+1} L {ax+shoe*18},{ay+5} Q {ax+shoe*21},{ay+12} {ax+shoe*12},{ay+12} L {ax-7},{ay+12} Z',fill=C['ink'])
def torso(sl,sr,hl,hr):
    return path(f'M {sl[0]},{sl[1]} Q {(sl[0]+sr[0])/2},{min(sl[1],sr[1])-8} {sr[0]},{sr[1]} L {hr[0]+3},{hr[1]+5} Q {(hl[0]+hr[0])/2},{max(hl[1],hr[1])+12} {hl[0]-3},{hl[1]+5} Z',fill=C['shirt'],stroke=C['ink'],width=1.4)
def front(x=150,hy=83,hips=None,knees=None,ankles=None,arms=None,head_dx=0,shoe_dirs=(-1,1),head_profile=0):
    sl=(x-24,hy+37); sr=(x+24,hy+37)
    hl,hr=hips or ((x-13,hy+109),(x+13,hy+109))
    kl,kr=knees or ((x-17,hy+162),(x+17,hy+162))
    al,ar=ankles or ((x-20,hy+219),(x+20,hy+219))
    arms=arms or (((x-33,hy+77),(x-34,hy+115)),((x+33,hy+77),(x+34,hy+115)))
    return leg(hl,kl,al,shoe_dirs[0])+leg(hr,kr,ar,shoe_dirs[1])+head(x+head_dx,hy,head_profile)+torso(sl,sr,hl,hr)+arm(sl,*arms[0])+arm(sr,*arms[1])
def side(sh=(150,127),hip=(150,194),knee=(153,247),ankle=(150,301),arms=None,profile=1,far=None,head_at=None):
    sx,sy=sh; hx,hy=hip
    # Points along the torso normal, for a comfortably wide profile.
    dx=hx-sx;dy=hy-sy;length=(dx*dx+dy*dy)**.5; nx=dy/length;ny=-dx/length
    sl=(sx-nx*17,sy-ny*17);sr=(sx+nx*17,sy+ny*17)
    hl=(hx-nx*12,hy-ny*12);hr=(hx+nx*12,hy+ny*12)
    elbow,hand=arms or ((sx+profile*12,sy+38),(sx+profile*12,sy+73))
    far=far or ((hip[0]-9,hip[1]),(knee[0]-10,knee[1]-2),(ankle[0]-10,ankle[1]-2))
    s=leg(*far,shoe=profile)
    s+=leg(hip,knee,ankle,profile)
    s+=head(*(head_at or (sx+profile*3,sy-34)),profile=profile)
    s+=torso(sl,sr,hl,hr)
    s+=arm(sh,elbow,hand)
    return s

def note(x,y,lines,anchor='middle'):
    return ''.join(text(x,y+i*17,l,12,anchor,400) for i,l in enumerate(lines))
def save(name,title,desc,body):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M 0,0 L 6,3 L 0,6" fill="{C['band']}"/></marker></defs>
<rect width="600" height="380" fill="{C['paper']}"/>
{body}
</svg>'''
    (OUT/f'{name}.svg').write_text(svg)

# Gentle marching: low knees, contralateral arm swing.
save('march','Gentle standing march','Two front views show alternating low knee lifts and a gentle opposite arm swing. Feet land softly beneath the hips.',
    label(155,36,'LIFT ONE FOOT')+label(445,36,'THEN THE OTHER')+floor()+
    front(155,83,knees=((133,218),(172,245)),ankles=((133,257),(175,302)),arms=(((124,167),(123,193)),((190,150),(193,126))))+
    front(445,83,knees=((428,245),(467,218)),ankles=((425,302),(467,257)),arms=(((410,150),(407,126)),((476,167),(477,193))))+
    arrow('M 110,289 Q 95,268 111,245')+arrow('M 495,288 Q 510,265 494,245')+note(300,353,['Small steps. Stand tall.']))

save('step-touch','Side step and touch','Step one foot sideways into a wider stance, then bring the other foot alongside with a light touch. Reverse direction.',
    label(155,36,'STEP SIDEWAYS')+label(445,36,'TOUCH FEET TOGETHER')+floor()+
    front(155,83,knees=((119,243),(185,243)),ankles=((99,302),(202,302)),arms=(((113,153),(113,185)),((197,153),(197,185))))+
    front(445,83,knees=((434,244),(459,244)),ankles=((439,302),(462,302)),arms=(((405,153),(405,185)),((485,153),(485,185))))+
    arrow('M 129,335 H 81')+arrow('M 395,335 H 432')+note(300,365,['Keep your steps easy and quiet.']))

save('sit-to-stand','Chair sit to stand','Side views show a person seated near the front of a stable chair, then standing with feet planted. The seated body leans slightly forward; knees track with feet.',
    label(155,36,'SIT NEAR THE FRONT')+label(445,36,'STAND UP')+floor()+chair(96,218)+
    side(sh=(156,143),hip=(143,214),knee=(205,221),ankle=(202,301),arms=((183,178),(199,210)),head_at=(162,107))+
    chair(377,218)+side(sh=(445,123),hip=(442,192),knee=(447,245),ankle=(448,301),arms=((471,158),(474,194)))+
    arrow('M 262,247 Q 300,205 324,164')+note(300,353,['Feet planted. Lower slowly.']))

save('wall-push-up','Wall push up','Side views show a straight body leaning toward a wall with bent elbows, then pressing away to straighter arms. Hands stay at shoulder height against the wall.',
    label(154,36,'BEND YOUR ELBOWS')+label(449,36,'PRESS AWAY')+floor()+wall(238)+wall(533)+
    side(sh=(182,137),hip=(144,207),knee=(121,252),ankle=(97,301),arms=((199,163),(230,126)),head_at=(193,101))+
    side(sh=(433,137),hip=(410,209),knee=(396,254),ankle=(382,301),arms=((477,130),(525,125)),head_at=(441,101))+
    arrow('M 408,84 H 377')+note(300,353,['Move as one long line.']))

save('hip-hinge','Standing hip hinge','Side views show standing, then pushing the hips backward while inclining the whole torso forward with a neutral back and a small bend at the knees. Hands rest at the hip crease.',
    label(155,36,'STAND TALL')+label(445,36,'SEND YOUR HIPS BACK')+floor()+
    side(sh=(153,123),hip=(150,194),knee=(153,246),ankle=(150,301),arms=((175,160),(155,190)))+
    side(sh=(477,166),hip=(414,211),knee=(449,251),ankle=(439,301),arms=((462,203),(427,210)),head_at=(501,140))+
    arrow('M 408,194 H 367')+note(300,353,['Soft knees. Keep your back long.']))

# A three-quarter side view makes the hip hinge and both foot anchors visible.
def row_pose(cx,pulled=False):
    near_hand=(cx-6,207) if pulled else (cx+33,230)
    far_hand=(cx+7,207) if pulled else (cx+46,226)
    near_elbow=(cx-31,198) if pulled else (cx+28,190)
    far_elbow=(cx-18,195) if pulled else (cx+41,187)
    band=path(f'M {near_hand[0]},{near_hand[1]} L {cx-6},314 L {cx+25},314 L {far_hand[0]},{far_hand[1]}',stroke=C['band'],width=3)
    far_arm=arm((cx+32,151),far_elbow,far_hand)
    figure=side(sh=(cx+20,149),hip=(cx-20,207),knee=(cx+5,253),ankle=(cx-7,301),arms=(near_elbow,near_hand),head_at=(cx+40,119),far=((cx-9,208),(cx+31,254),(cx+24,301)))
    return far_arm+figure+band+circle(*near_hand,7,C['skin'],C['ink'])+circle(*far_hand,7,C['skin'],C['ink'])
save('band-row','Standing resistance band row','Two three-quarter side views show a hip hinge with a long back, a resistance band securely underneath both shod feet, and pulling both hands toward the hips with elbows moving back. No furniture is used as an anchor.',
    label(150,36,'ARMS LONG')+label(440,36,'PULL TOWARD YOUR HIPS')+floor()+row_pose(150)+row_pose(440,True)+
    arrow('M 473,240 Q 446,241 427,224')+
    note(300,349,['Band under BOTH shod feet.','Hold a comfortable hip hinge.']))

save('calf-raise','Supported calf raise','Side views show holding the back of a stable chair, then rising onto the balls of the feet with both heels lifted. Knees stay softly straight.',
    label(155,36,'HEELS DOWN')+label(445,36,'LIFT YOUR HEELS')+floor()+chair(216,216,-1)+chair(506,216,-1)+
    side(sh=(128,124),hip=(127,193),knee=(130,247),ankle=(128,301),arms=((163,153),(210,141)))+
    side(sh=(418,111),hip=(417,180),knee=(420,234),ankle=(420,286),arms=((458,136),(500,141)))+
    path('M 413,288 L 439,310',stroke=C['ink'],width=13)+arrow('M 388,309 V 278')+
    note(300,353,['Use a stable chair for balance.']))

# Forearm wall plank: forearm vertical, elbow beneath shoulder height.
save('wall-plank','Standing forearm wall plank','A side view shows forearms against a wall with elbows bent about ninety degrees. Feet are stepped back and the body forms a long line from shoulders through hips to ankles. Keep breathing.',
    floor()+wall(417)+side(sh=(345,141),hip=(287,207),knee=(253,253),ankle=(219,301),arms=((411,164),(411,111)),head_at=(367,108))+
    label(300,36,'FOREARMS ON THE WALL')+path('M 232,295 L 288,217 L 342,151',stroke=C['line'],width=1.4,extra='stroke-dasharray="4 6"')+
    note(125,126,['Step back only','as far as comfortable.'])+note(300,353,['A long body line. Keep breathing.']))

# Back against wall; frontal wall plane provides a clear surface cue.
wallplane=f'<rect x="58" y="65" width="484" height="253" rx="12" fill="{C["pale"]}"/>'
save('wall-slide','Wall arm slide','Front views show standing with the back against a wall, arms bent in a W, then sliding upward toward a Y only as high as comfortable. The lower back stays easy rather than arched.',
    wallplane+label(155,36,'START IN A W')+label(445,36,'SLIDE UP COMFORTABLY')+floor()+
    front(155,83,arms=(((108,155),(101,106)),((202,155),(209,106))))+
    front(445,83,arms=(((398,105),(382,68)),((492,105),(508,68))))+
    arrow('M 369,132 L 354,94')+arrow('M 521,132 L 538,94')+note(300,353,['Back to wall. No forced overhead reach.']))

save('seated-rotation','Gentle seated trunk rotation','Two seated front views show turning the upper body gently to the left and right while keeping both feet planted and the hips facing forward. Arms rest comfortably across the chest.',
    label(155,36,'TURN GENTLY LEFT')+label(445,36,'THEN RIGHT')+floor()+chair(110,225)+chair(400,225)+
    front(155,92,hips=((140,217),(170,217)),knees=((122,251),(187,251)),ankles=((124,301),(187,301)),arms=(((119,168),(169,155)),((187,167),(139,151))),head_dx=-7,head_profile=-1)+
    front(445,92,hips=((430,217),(460,217)),knees=((412,251),(477,251)),ankles=((414,301),(477,301)),arms=(((409,167),(459,151)),((477,168),(429,155))),head_dx=7,head_profile=1)+
    arrow('M 198,110 Q 157,81 112,109')+arrow('M 403,110 Q 444,81 489,109')+note(300,353,['Turn through your upper back. Hips stay forward.']))

save('shoulder-roll','Shoulder rolls','Two front views show lifting the shoulders slightly, then letting them travel back and down. The head stays upright; this exercise does not involve neck circles.',
    label(155,36,'LIFT YOUR SHOULDERS')+label(445,36,'ROLL BACK AND DOWN')+floor()+
    front(155,83,arms=(((120,155),(121,192)),((190,155),(189,192))))+
    front(445,83,arms=(((412,163),(411,202)),((478,163),(479,202))))+
    arrow('M 110,139 Q 94,114 118,103')+arrow('M 200,139 Q 216,114 192,103')+
    arrow('M 402,107 Q 379,119 396,145')+arrow('M 488,107 Q 511,119 494,145')+note(300,353,['Keep your head still. Let your shoulders soften.']))

# Close-up forearms and recognizable hands for wrist mobility.
def hand(x,y,direction=1,up=True):
    # forearm horizontal, palm extending up or down from the wrist, fingers together.
    sign=-1 if up else 1
    s=limb([(x-92,y),(x-12,y)],C['skin'],24)
    s+=path(f'M {x-14},{y-11} Q {x-8},{y-20*sign} {x+3},{y-15*sign} L {x+17},{y+sign*36} Q {x+20},{y+sign*49} {x+10},{y+sign*49} L {x-5},{y+sign*47} Q {x-12},{y+sign*44} {x-13},{y+sign*35} Z',fill=C['skin'],stroke=C['ink'],width=1.5)
    s+=path(f'M {x-4},{y+sign*25} L {x+1},{y+sign*43} M {x+4},{y+sign*23} L {x+8},{y+sign*42}',stroke='#b38668',width=1)
    return s
save('wrist-mobility','Gentle wrist motion','Close-up views show a supported forearm held still while the hand tips gently upward and downward at the wrist. The movement is small and unforced.',
    label(155,47,'TIP UP')+label(445,47,'TIP DOWN')+
    f'<rect x="50" y="241" width="210" height="12" rx="6" fill="{C["pale"]}"/><rect x="340" y="241" width="210" height="12" rx="6" fill="{C["pale"]}"/>'+
    hand(191,220,up=True)+hand(481,210,up=False)+arrow('M 236,216 Q 258,185 223,168')+arrow('M 525,199 Q 552,230 518,252')+
    note(300,317,['Keep your forearm still. Move only in an easy range.'])+note(300,344,['Then slowly open and close your hands.']))

save('chest-stretch','Seated chest opening','A person sits tall in a stable chair with feet planted and opens the arms out to the sides below shoulder height, palms forward. The shoulders stay relaxed and the back does not arch.',
    label(300,36,'OPEN YOUR ARMS GENTLY')+floor()+chair(255,228)+
    front(300,91,hips=((285,216),(315,216)),knees=((269,252),(331,252)),ankles=((269,301),(331,301)),arms=(((228,151),(189,169)),((372,151),(411,169))))+
    arrow('M 224,115 Q 197,118 182,142')+arrow('M 376,115 Q 403,118 418,142')+note(300,353,['Sit tall. Keep your shoulders down.']))

save('calf-stretch','Standing calf stretch','Side view of a person facing a wall with hands against it, one knee bent forward and the other leg extended behind. The back heel stays on the floor and both feet face toward the wall.',
    label(300,36,'BACK HEEL STAYS DOWN')+floor()+wall(448)+
    side(sh=(354,133),hip=(305,205),knee=(365,244),ankle=(352,301),arms=((398,141),(440,125)),head_at=(369,98),far=((294,205),(253,250),(209,301)))+
    arrow('M 206,265 V 292')+note(131,215,['Back leg','comfortably straight.'])+note(300,353,['Change sides. Keep both feet facing forward.']))

save('seated-hamstring','Seated hamstring stretch','Side view shows sitting near the front of a stable chair, extending one heel forward with a slight knee bend and toes lifted, and hinging forward a little from the hips with a long back.',
    label(300,36,'HEEL FORWARD, BACK LONG')+floor()+chair(202,217)+
    side(sh=(292,144),hip=(266,213),knee=(345,248),ankle=(410,300),arms=((324,182),(333,223)),head_at=(306,110),far=((257,213),(298,238),(292,301)))+
    path('M 407,302 L 415,280',stroke=C['ink'],width=14)+arrow('M 350,119 Q 370,145 357,173')+note(143,110,['Tip from','your hips.'])+
    note(300,353,['A slight knee bend. Stop at a gentle stretch.']))

def footprints(cx,offset=False):
    def sole(x,y):
        return path(f'M {x-7},{y+16} Q {x-9},{y+4} {x-10},{y-5} Q {x-10},{y-19} {x},{y-19} Q {x+11},{y-19} {x+10},{y-4} L {x+6},{y+16} Q {x},{y+20} {x-7},{y+16} Z',fill=C['ink'])
    bg=f'<rect x="{cx-28}" y="218" width="64" height="92" rx="17" fill="{C["pale"]}"/>'
    return text(cx+4,210,'FEET',9,weight=700)+bg+sole(cx+(9 if offset else 0),241)+sole(cx-(9 if offset else 0),278)

save('tandem-balance','Supported heel to toe balance','Two front views show standing beside a stable chair. The first stance has feet slightly offset for an easier balance. The second places one heel directly in front of the other toes. One hand remains near the chair.',
    label(155,36,'EASIER: FEET OFFSET')+label(445,36,'HEEL TO TOE')+floor()+chair(229,217,-1)+chair(519,217,-1)+
    front(150,83,knees=((133,244),(163,244)),ankles=((125,302),(164,302)),arms=(((116,162),(117,199)),((194,140),(222,143))),shoe_dirs=(1,1))+
    front(440,83,knees=((432,244),(448,244)),ankles=((427,302),(452,302)),arms=(((406,162),(407,199)),((484,140),(512,143))),shoe_dirs=(1,1))+
    footprints(66,True)+footprints(356)+note(300,353,['Keep the chair within reach. Look ahead.']))

# A convenient full-size inspection page, excluded from the production page.
names=[p.stem for p in OUT.glob('*.svg')]
(OUT/'contact-sheet.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><title>Exercise illustration review</title><style>body{background:#e5ece4;font-family:Arial,sans-serif;margin:28px}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}figure{margin:0;background:#f6f3ec;border-radius:12px;overflow:hidden}img{width:100%;display:block}figcaption{padding:12px 18px;color:#204f46}h1{color:#204f46}@media(max-width:700px){main{grid-template-columns:1fr}}</style><h1>Exercise illustrations</h1><main>'''+''.join(f'<figure><img src="{n}.svg" alt="{n}"><figcaption>{n}</figcaption></figure>' for n in names)+'</main></html>')
print(f'Wrote {len(names)} SVGs to {OUT}')
