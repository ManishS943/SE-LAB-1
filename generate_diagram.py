"""Generate the editable UML use-case diagram from fixed layout definitions."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'diagrams'
OUT.mkdir(exist_ok=True)
parts = []


def add(item):
    parts.append(item)


def text(x, y, label, size=22, bold=False):
    add(f'<text x="{x}" y="{y}" text-anchor="middle" '
        f'dominant-baseline="middle" font-size="{size}" '
        f'font-weight="{700 if bold else 400}" fill="#183649">'
        f'{escape(label)}</text>')


def line(points, dashed=False, arrow=False):
    coords = ' '.join(f'{x},{y}' for x, y in points)
    dash = 'stroke-dasharray="9 6"' if dashed else ''
    mark = 'marker-end="url(#openArrow)"' if arrow else ''
    add(f'<polyline points="{coords}" fill="none" stroke="#475f70" '
        f'stroke-width="2.3" {dash} {mark}/>')


def actor(x, y, labels):
    add(f'<circle cx="{x}" cy="{y-45}" r="20" fill="white" '
        'stroke="#183649" stroke-width="3"/>')
    line([(x, y-25), (x, y+35)])
    line([(x-33, y), (x+33, y)])
    line([(x, y+35), (x-28, y+75)])
    line([(x, y+35), (x+28, y+75)])
    for i, label in enumerate(labels):
        text(x, y+110+i*29, label, 23, True)


def use_case(x, y, radius, case_id, labels):
    add(f'<ellipse cx="{x}" cy="{y}" rx="{radius}" ry="52" '
        'fill="#eef4f7" stroke="#21495e" stroke-width="2.5"/>')
    text(x, y-27, case_id, 17, True)
    for i, label in enumerate(labels):
        text(x, y+2+i*24, label, 22)


add('<svg xmlns="http://www.w3.org/2000/svg" width="1850" height="1350" '
    'viewBox="0 0 1850 1350" role="img" aria-labelledby="title desc">')
add('<title id="title">Hostel Maintenance and Issue Ticketing UML Use-Case Diagram</title>')
add('<desc id="desc">Resident and Maintenance Warden goals inside a system '
    'boundary, mandatory ticket validation, conditional SLA escalation, '
    'and a supporting SMS/email gateway.</desc>')
add('<defs><marker id="openArrow" markerWidth="14" markerHeight="14" '
    'refX="12" refY="7" orient="auto" markerUnits="userSpaceOnUse">'
    '<path d="M 1 1 L 12 7 L 1 13" fill="none" stroke="#475f70" '
    'stroke-width="2"/></marker></defs>')
add('<rect width="1850" height="1350" fill="white"/>')
add('<g font-family="Arial,Helvetica,sans-serif">')
text(925, 52, 'Hostel Maintenance and Issue Ticketing', 36, True)
text(925, 98, 'SE Lab 1 | UML use-case model based on the repository requirements', 23)
add('<rect x="230" y="150" width="1350" height="1060" rx="3" '
    'fill="white" stroke="#183649" stroke-width="3"/>')
text(905, 190, 'Hostel Maintenance and Issue Ticketing System', 25, True)

for end in [(340,300),(340,550),(320,800)]:
    line([(133,600),end])
for end in [(1470,300),(1470,550),(1470,800),(1475,1030)]:
    line([(1667,600),end])
line([(950,1112),(950,1170),(1610,1170),(1610,1050),(1667,1050)])

actor(100,600,['Hostel','Resident'])
actor(1700,600,['Maintenance','Warden'])
actor(1700,1050,['SMS/email','Gateway'])

cases=[
    (500,300,160,'UC-01',['Log Maintenance','Ticket']),
    (900,300,170,'UC-02',['Validate Ticket','Details']),
    (1300,300,170,'UC-04',['Manage Ticket','Queue']),
    (500,550,160,'UC-03',['Track Own Ticket','Status']),
    (1300,550,170,'UC-05',['Prioritize and','Assign Work']),
    (500,800,180,'UC-07',['Confirm and Close','Own Ticket']),
    (1300,800,170,'UC-06',['Update Ticket','Status']),
    (1300,1030,175,'UC-08',['Close with','Warden Override']),
    (550,1060,150,'UC-09',['Monitor SLA']),
    (950,1060,165,'UC-10',['Queue Escalation','Alert']),
]
for args in cases:
    use_case(*args)

line([(660,300),(730,300)],dashed=True,arrow=True)
text(700,240,'<<include>>',20,True)
line([(785,1060),(700,1060)],dashed=True,arrow=True)
text(745,989,'<<extend>>',20,True)
text(745,1140,'[eligible high-priority ticket stale >= 24h]',18)

add('<path d="M 770 555 L 1020 555 L 1040 575 L 1040 770 '
    'L 770 770 Z M 1020 555 L 1020 575 L 1040 575" '
    'fill="#fff7e6" stroke="#a78a52" stroke-width="1.5"/>')
for i,label in enumerate([
    'Authentication is a', 'precondition; ownership', 'and role checks apply',
    'to protected requests.', '', 'SLA monitoring is an',
    'internal timed behavior.',
]):
    if label:
        text(905,588+i*25,label,19)

text(925,1260,'Solid line: actor association | dashed open arrow: include / extend',21)
text(925,1302,'Closure requires resident confirmation or a documented Warden override; no automatic closure.',21)
add('</g></svg>')
(OUT/'Hostel_Maintenance_Use_Case.svg').write_text('\n'.join(parts),encoding='utf-8')
print(OUT/'Hostel_Maintenance_Use_Case.svg')
