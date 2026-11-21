#!/usr/bin/env python3
"""Winterplay logo: a snowflake (winter) with a play triangle (play) at its heart.
One geometry source -> logo.svg (site) + PNG preview (chat). Brand pink #C2185B.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

PINK = (194, 24, 91)
BG = (250, 249, 246)
INK = (12, 12, 12)

OUT_DIR = os.path.expanduser("~/workspace/winterplay")
ASSETS = os.path.join(OUT_DIR, "assets")
os.makedirs(ASSETS, exist_ok=True)

CX, CY = 60.0, 60.0

# --- play triangle (pointing right) ---
TRI = [(48.0, 42.0), (48.0, 78.0), (79.0, 60.0)]

# --- snowflake: 6 arms, each with a V-branch chevron near its tip ---
ARM_ANGLES = [-90, -30, 30, 90, 150, -150]  # degrees, screen coords (y down)
ARM_R0, ARM_R1 = 2.0, 52.0
BRANCH_R, BRANCH_LEN, BRANCH_SPREAD = 44.0, 9.0, 35.0

def pt(r, deg):
    a = math.radians(deg)
    return (CX + r * math.cos(a), CY + r * math.sin(a))

arms = [(pt(ARM_R0, a), pt(ARM_R1, a)) for a in ARM_ANGLES]
branches = []
for a in ARM_ANGLES:
    base = pt(BRANCH_R, a)
    for s in (+1, -1):
        bdeg = a + 180 + s * BRANCH_SPREAD
        b = math.radians(bdeg)
        end = (base[0] + BRANCH_LEN * math.cos(b), base[1] + BRANCH_LEN * math.sin(b))
        branches.append((base, end))

# --- SVG ---
def f(v):
    return f"{v:.2f}"

tri_pts = " ".join(f"{f(x)},{f(y)}" for x, y in TRI)
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">']
svg.append('<defs><mask id="tri-cut"><rect width="120" height="120" fill="white"/>')
svg.append(f'<polygon points="{tri_pts}" fill="black" stroke="black" stroke-width="10" stroke-linejoin="round"/>')
svg.append('</mask></defs>')
svg.append('<g mask="url(#tri-cut)" fill="none" stroke="#C2185B" stroke-width="5" stroke-linecap="round">')
for (x0, y0), (x1, y1) in arms:
    svg.append(f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}"/>')
svg.append('</g>')
svg.append('<g mask="url(#tri-cut)" fill="none" stroke="#C2185B" stroke-width="4" stroke-linecap="round">')
for (x0, y0), (x1, y1) in branches:
    svg.append(f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}"/>')
svg.append('</g>')
svg.append(f'<polygon points="{tri_pts}" fill="#C2185B" stroke="#C2185B" stroke-width="4" stroke-linejoin="round"/>')
svg.append('</svg>')

svg_path = os.path.join(ASSETS, "logo.svg")
with open(svg_path, "w") as fh:
    fh.write("\n".join(svg) + "\n")

# --- PNG preview: the header lockup as it will look on the site ---
S = 1024 / 120.0  # scale to 1024px mark

def scale(p):
    return (p[0] * S, p[1] * S)

mark = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
d = ImageDraw.Draw(mark)
for (x0, y0), (x1, y1) in arms:
    d.line([scale((x0, y0)), scale((x1, y1))], fill=PINK + (255,), width=int(5 * S))
for (x0, y0), (x1, y1) in branches:
    d.line([scale((x0, y0)), scale((x1, y1))], fill=PINK + (255,), width=int(4 * S))
# knockout halo around the triangle (same as the SVG mask): erase the arms
# where they would touch the triangle, so the play button stays clean.
tri_scaled = [scale(p) for p in TRI]
d.polygon(tri_scaled, fill=BG + (255,))
d.line(tri_scaled + [tri_scaled[0]], fill=BG + (255,), width=int(10 * S), joint="curve")
d.polygon(tri_scaled, fill=PINK + (255,))

# lockup preview: off-white canvas, mark left + "Winterplay" wordmark
W, H = 1400, 560
preview = Image.new("RGB", (W, H), BG)
pd = ImageDraw.Draw(preview)
mark_small = mark.resize((300, 300), Image.LANCZOS)
preview.paste(mark_small, (90, (H - 300) // 2), mark_small)
font = None
for path in ("/usr/share/fonts/truetype/noto/NotoSansDisplay-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
    if os.path.exists(path):
        font = ImageFont.truetype(path, 110)
        break
pd.text((440, H // 2 - 78), "Winterplay", fill=INK, font=font)
preview.save(os.path.join(OUT_DIR, "logo-preview.png"))
mark.save(os.path.join(OUT_DIR, "logo-mark.png"))
print("svg:", svg_path)
print("preview:", os.path.join(OUT_DIR, "logo-preview.png"))
