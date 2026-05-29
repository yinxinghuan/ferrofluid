#!/usr/bin/env python3
"""Compose ferrofluid poster: shader screenshot + 'ferrofluid' title at top.

Per CLAUDE.md game-publish skill:
  - 1:1, 1024×1024 PNG
  - title text must be near the top (list UI buttons cover the bottom)
"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, '_dev_poster_v2.png')
OUT  = os.path.join(ROOT, 'poster.png')
TARGET = 1024

# Cormorant Garamond italic — try Cormorant first, fall back to system serif italic
FONT_CANDIDATES = [
    '/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf',
    '/System/Library/Fonts/Supplemental/Georgia Italic.ttf',
    '/System/Library/Fonts/Supplemental/Hoefler Text Italic.ttf',
    '/Library/Fonts/Times New Roman Italic.ttf',
    '/System/Library/Fonts/NewYorkItalic.ttf',
]
SANS = '/System/Library/Fonts/Supplemental/Futura.ttc'

def find_font(paths, fallback=None):
    for p in paths:
        if os.path.exists(p):
            return p
    return fallback

font_serif = find_font(FONT_CANDIDATES)
if not font_serif:
    # Last resort: PIL default bitmap font (won't be pretty)
    print('WARN: no italic serif found, falling back')
    font_serif = None

# 1. Load shader screenshot, scale/crop to TARGET
img = Image.open(SRC).convert('RGB')
w, h = img.size
print(f'src size: {w}x{h}')

# Center-crop to square then resize
side = min(w, h)
left = (w - side) // 2
top  = (h - side) // 2
img = img.crop((left, top, left + side, top + side)).resize((TARGET, TARGET), Image.LANCZOS)

# 2. Title overlay
draw = ImageDraw.Draw(img, 'RGBA')

# Pink AlterU color, slightly translucent for elegance
PINK = (245, 177, 199, 240)
SUB_PINK = (245, 177, 199, 150)

title = 'ferrofluid'
TITLE_SIZE = 120
font_title = ImageFont.truetype(font_serif, TITLE_SIZE) if font_serif else ImageFont.load_default()

# Measure title
bbox = draw.textbbox((0, 0), title, font=font_title)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
tx = (TARGET - tw) // 2
ty = 120
draw.text((tx, ty), title, fill=PINK, font=font_title)

# Subtitle / pseudo-tagline
sub = 'a magnet in your finger'
SUB_SIZE = 28
font_sub = ImageFont.truetype(font_serif, SUB_SIZE) if font_serif else ImageFont.load_default()
sbbox = draw.textbbox((0, 0), sub, font=font_sub)
sw = sbbox[2] - sbbox[0]
sx = (TARGET - sw) // 2
sy = ty + th + 32
draw.text((sx, sy), sub, fill=SUB_PINK, font=font_sub)

img.save(OUT, 'PNG', optimize=True)
print(f'wrote {OUT}  {TARGET}x{TARGET}')
