#!/usr/bin/env python3
"""Winterplay logo: a bold geometric W in a pink rounded square (app-icon style).
Archer's brief: the icon must be a W. One geometry source -> logo.svg (site)
+ PNG preview (chat). Brand pink #C2185B.
"""
import os
from PIL import Image, ImageDraw, ImageFont

PINK = (22, 163, 74)
BG = (250, 249, 246)
INK = (12, 12, 12)
WHITE = (255, 255, 255)

OUT_DIR = os.path.expanduser("~/workspace/winterplay")
ASSETS = os.path.join(OUT_DIR, "assets")
os.makedirs(ASSETS, exist_ok=True)

# --- geometry (viewBox 0 0 120 120) ---
# Rounded square: 10..110, radius 24. Custom W: white stroked polyline whose
# middle peak is a right-pointing play triangle (Winter + Play in one mark).
W_PTS = [(30.0, 40.0), (43.0, 80.0), (60.0, 52.0), (77.0, 80.0), (90.0, 40.0)]
TRI = [(50.0, 38.0), (50.0, 70.0), (78.0, 54.0)]

def f(v):
    return f"{v:.2f}"

pts_str = " ".join(f"{f(x)},{f(y)}" for x, y in W_PTS)
tri_str = " ".join(f"{f(x)},{f(y)}" for x, y in TRI)
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">']
svg.append('<rect x="10" y="10" width="100" height="100" rx="24" fill="#16A34A"/>')
svg.append(f'<polyline points="{pts_str}" fill="none" stroke="#FFFFFF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
svg.append(f'<polygon points="{tri_str}" fill="#FFFFFF"/>')
svg.append('</svg>')

svg_path = os.path.join(ASSETS, "logo.svg")
with open(svg_path, "w") as fh:
    fh.write("\n".join(svg) + "\n")

# --- PNG preview: the header lockup as it will look on the site ---
S = 1024 / 120.0

def scale(p):
    return (p[0] * S, p[1] * S)

mark = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
d = ImageDraw.Draw(mark)
# rounded square
d.rounded_rectangle([10 * S, 10 * S, 110 * S, 110 * S], radius=24 * S, fill=PINK + (255,))
d.line([scale(p) for p in W_PTS], fill=WHITE + (255,), width=int(11 * S), joint="curve")
d.polygon([scale(p) for p in TRI], fill=WHITE + (255,))

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
