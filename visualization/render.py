#!/usr/bin/env python3
"""Render the two exact cotangent-plane examples as a rotating GIF."""
from math import cos, pi, sin, sqrt
from os import environ
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = (632, 451)
BG = "#0b1525"
PANEL = "#112339"
GRID = "#45627a"
WHITE = "#eff7fc"
MUTED = "#bed0dd"
TEAL = "#69e7c7"
AMBER = "#ffba73"
SHARED = "#eef3ff"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")

CASES = (
    ("Coordinate point", "A = (1, 0; 0, 0)",
     ((0, 1, 0), (0, 0, 1)), ((1, 0, 0), (0, 0, 1)),
     (0, 0, 1), "dy, dz", "dx, dz", "dz"),
    ("Checkerboard point", "A = (1, -1; -1, 1)",
     ((1, 0, 0), (0, 1, 1)), ((0, 1, 0), (1, 0, 1)),
     (1, 1, 1), "dx, dy + dz", "dy, dx + dz", "dx + dy + dz"),
)


def norm(v):
    return sqrt(sum(x*x for x in v))


def scale(v, factor):
    return tuple(x * factor for x in v)


def add(u, v):
    return tuple(x + y for x, y in zip(u, v))


def patch(edge):
    u, v = (scale(w, 0.9 / norm(w)) for w in edge)
    return [add(scale(u, i), scale(v, j)) for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def font(size, bold=False):
    key = "Q220_BOLD_FONT" if bold else "Q220_FONT"
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    return ImageFont.truetype(environ.get(key, str(FONT_DIR / name)), size)


def draw_scene(base, xcenter, camera, row, col, shared):
    tilt = 0.52
    ycenter = 216

    def project(v):
        x, y, z = v
        horiz = x*cos(camera) + y*sin(camera)
        depth = -x*sin(camera) + y*cos(camera)
        vert = z*cos(tilt) - depth*sin(tilt)
        return xcenter + 56*horiz, ycenter - 56*vert

    layer = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(layer)
    axes = ((1.45, 0, 0), (0, 1.45, 0), (0, 0, 1.45))
    for axis in axes:
        d.line([project(scale(axis, -0.87)), project(axis)], fill=GRID, width=2)

    for edge, fill, color in ((row, (47, 203, 177, 73), TEAL), (col, (244, 140, 70, 73), AMBER)):
        points = [project(v) for v in patch(edge)]
        d.polygon(points, fill=fill)
        d.line(points + points[:1], fill=color, width=2)
        for v in edge:
            v = scale(v, 0.9 / norm(v))
            d.line([project(scale(v, -1)), project(v)], fill=color, width=1)
        base.alpha_composite(layer)
        layer = Image.new("RGBA", SIZE)
        d = ImageDraw.Draw(layer)

    line = scale(shared, 1.22 / norm(shared))
    d.line([project(scale(line, -1)), project(line)], fill=SHARED, width=4)
    px, py = project((0, 0, 0))
    d.ellipse((px-3, py-3, px+3, py+3), fill=WHITE)
    for axis, name in zip(axes, ("dx", "dy", "dz")):
        px, py = project(axis)
        d.text((px, py), name, fill=WHITE, font=font(19, True), anchor="mm", stroke_width=2,
               stroke_fill=PANEL)
    base.alpha_composite(layer)


def frame(angle):
    image = Image.new("RGBA", SIZE, BG)
    draw = ImageDraw.Draw(image)
    draw.text((18, 12), "Differential planes at the boundary", font=font(30, True), fill=WHITE)
    draw.text((18, 54), "Two payoff equations are automatically zero here.", font=font(22), fill=MUTED)
    for i, (title, matrix, row, col, common, row_label, col_label, common_label) in enumerate(CASES):
        x = 14 + i*308
        draw.rounded_rectangle((x, 88, x+296, 364), radius=14, fill=PANEL)
        draw.text((x+12, 100), title, font=font(23, True), fill=WHITE)
        draw.text((x+12, 130), matrix, font=font(19), fill=MUTED)
        draw_scene(image, x+148, angle, row, col, common)
        draw.text((x+12, 287), f"Row plane: {row_label}", font=font(19, True), fill=TEAL)
        draw.text((x+12, 311), f"Column plane: {col_label}", font=font(19, True), fill=AMBER)
        draw.text((x+12, 335), f"Shared line: {common_label}", font=font(19, True), fill=SHARED)
    draw.text((18, 374), "Rank loss: one vector is zero, or both lie on the line.",
              font=font(23, True), fill=WHITE)
    draw.text((18, 410), "Each event costs two conditions in payoff space.",
              font=font(22), fill=MUTED)
    return image.convert("RGB")


if __name__ == "__main__":
    frames = [frame(0.8 + 2*pi*i/36) for i in range(36)]
    palette = frames[0].quantize(colors=96)
    frames = [img.quantize(palette=palette, dither=Image.Dither.NONE) for img in frames]
    output = Path(__file__).with_name("boundary-cotangent-planes.gif")
    frames[0].save(output, save_all=True, append_images=frames[1:], duration=125, loop=0, optimize=True)
