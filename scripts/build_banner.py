#!/usr/bin/env python3
"""Compose self-contained SVG profile banners from the existing city artwork."""
import base64
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ARTWORK = ASSETS / 'neon-city-background.png'


def text(x, y, value, size, color='#f2f5fa', weight=400, mono=False, tracking=0):
    family = 'ui-monospace, SFMono-Regular, Consolas, monospace' if mono else 'Arial, Helvetica, sans-serif'
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" letter-spacing="{tracking}">'
            f'{escape(value)}</text>')


def compose(mobile=False):
    width, height = (600, 720) if mobile else (1280, 660)
    x = 40 if mobile else 64
    image = base64.b64encode(ARTWORK.read_bytes()).decode('ascii')
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Finn // Hallaka — Enter Neon City</title>',
           '<desc id="desc">Media Informatics student at HSMW building mobile apps with Flutter and SwiftUI. '
           'Open the portfolio for projects, about me, and my toolbox.</desc>',
           '<defs>',
           '<linearGradient id="shade"><stop stop-color="#060a14" stop-opacity=".94"/>'
           '<stop offset=".55" stop-color="#060a14" stop-opacity=".73"/>'
           '<stop offset="1" stop-color="#060a14" stop-opacity=".16"/></linearGradient>',
           '<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">'
           '<stop stop-color="#060a14" stop-opacity="0"/>'
           '<stop offset="1" stop-color="#060a14" stop-opacity=".88"/></linearGradient>',
           '<linearGradient id="edge"><stop stop-color="#60e6fa"/>'
           '<stop offset="1" stop-color="#ff65bc"/></linearGradient>',
           '</defs>',
           f'<image width="{width}" height="{height}" preserveAspectRatio="xMaxYMid slice" '
           f'href="data:image/png;base64,{image}"/>',
           f'<path fill="url(#shade)" d="M0 0h{width}v{height}H0z"/>',
           f'<path fill="url(#floor)" d="M0 0h{width}v{height}H0z"/>']
    svg.append(text(x, 77 if mobile else 91, 'FINN // HALLAKA', 30 if mobile else 38,
                    weight=600, mono=True, tracking=1))
    svg.append(text(x, 206 if mobile else 228, 'Everyday ideas.', 64 if mobile else 72, weight=700))
    svg.append(text(x, 285 if mobile else 313, 'Real apps.', 64 if mobile else 72,
                    color='#60e6fa', weight=700))
    if mobile:
        svg.append(text(x, 349, 'Media Informatics student at HSMW.', 24, '#d0d8e7'))
        svg.append(text(x, 388, 'Building with Flutter & SwiftUI.', 24, '#d0d8e7'))
    else:
        svg.append(text(x, 374, 'Media Informatics student at HSMW.', 26, '#d0d8e7'))
        svg.append(text(x, 414, 'Building mobile apps with Flutter & SwiftUI.', 26, '#d0d8e7'))
    button_y = 451 if mobile else 462
    button_width, button_height = (520, 82) if mobile else (380, 72)
    svg.append(f'<rect x="{x}" y="{button_y}" width="{button_width}" '
               f'height="{button_height}" rx="4" fill="#60e6fa"/>')
    svg.append(text(x + 25, button_y + (51 if mobile else 46), 'ENTER NEON CITY',
                    24 if mobile else 23, '#07101c', weight=700, mono=True))
    arrow_x, arrow_y = x + button_width - 49, button_y + button_height // 2
    svg.append(f'<path d="M{arrow_x-11} {arrow_y+11}l22-22m-17 0h17v17" '
               'fill="none" stroke="#07101c" stroke-width="3"/>')
    footer_y = 624 if mobile else 607
    svg.append(f'<path d="M{x} {footer_y-36}H{width-x}" stroke="url(#edge)" opacity=".6"/>')
    svg.append(text(x, footer_y, 'PROJECTS / ABOUT ME / TOOLBOX', 18 if mobile else 20,
                    '#c6d5e8', mono=True, tracking=.5))
    if mobile:
        svg.append(text(x, 673, 'hallaka01.github.io', 20, '#60e6fa', mono=True))
    else:
        svg.append(text(932, footer_y, 'hallaka01.github.io', 20, '#60e6fa', mono=True))
    svg.append(f'<path d="M1 29V1h42M{width-43} {height-1}h42v-28" '
               'fill="none" stroke="url(#edge)" stroke-width="2"/>')
    svg.append('</svg>')
    return '\n'.join(svg) + '\n'


if __name__ == '__main__':
    for filename, mobile in [('portfolio-banner.svg', False), ('portfolio-banner-mobile.svg', True)]:
        (ASSETS / filename).write_text(compose(mobile), encoding='utf-8')
        print('Built ' + filename)
