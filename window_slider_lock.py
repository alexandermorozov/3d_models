#!/usr/bin/python3

from random import random
from typing import Tuple
from math import sin, cos, pi, sqrt

from solid import (
    scad_render_to_file, translate, linear_extrude, minkowski, hull,
    union, cube, intersection, rotate, square, import_scad, color, polygon,
    square, scale
)
from solid.utils import up, right, left, down
from solid.objects import cylinder, sphere, circle, hole

D = 0.01
D2 = D * 2


bolt_x = 2
bolt_y = 20
shealth_l = 40

box_ext_w = bolt_y + (2 + 1.2) * 2

def hole_strip():
    h0 = 9
    h_max = 20
    L = 90
    off = 1.85
    extra_y = (box_ext_w - bolt_y)- 2 * off
    extra_x = 0.35
    window_r = 880
    window_off = 16

    obj = cube([L, bolt_y + extra_y + off * 2, h_max])
    obj -= translate([window_off, -1, window_r + h0])(
        rotate(-90, [1, 0, 0])(cylinder(r=window_r, h=100, segments=1000))
    )

    # step = bolt_x + 1.8 + extra_x
    # for i in range(0, int(L/step) - 1):
    #     x = 4 + i * step
    #     obj -= translate([x, off, 0.6])(cube([bolt_x + extra_x, bolt_y + extra_y, h_max + 2]))

    xw = bolt_x + extra_x
    yw = bolt_y + extra_y
    hole0 = translate([-xw / 2, off, -window_r])(cube([xw, yw, window_r]))

    step = bolt_x + 1.2 + extra_x
    step_deg = step / window_r * 180 / pi
    a0 = step_deg * 0.7
    for i in range(25):
        a = a0 + i * step_deg
        obj -= up(window_r + 0.6)(rotate(-a, [0, 1, 0])(hole0))

    return obj


def shealth():
    h = shealth_l
    th = 0.6 * 3
    extra_x = 0.7
    extra_y = (box_ext_w - bolt_y) - th * 2
    return (
        cube([bolt_x + th * 2 + extra_x, bolt_y + th * 2 + extra_y, h], center=True)
        - cube([bolt_x + extra_x, bolt_y + extra_y, h + 2], center=True)
    )


def tongue():
    L = shealth_l + 14
    profile = [
        [0, 0],
        [bolt_y, 0.0],
        [bolt_y, L - 3],
        [bolt_y - 1.5, L],
        [1.5, L],
        [0, L - 3],
    ]

    side = (box_ext_w - bolt_y) / 2
    obj = linear_extrude(bolt_x)(polygon(profile))
    obj += translate([-side, 0, 0])(cube([box_ext_w, 5, 3 + 4.5]))
    return obj

def main():
    scad_render_to_file(hole_strip(), "scad/window_slider_lock_strip.scad", include_orig_code=False)
    scad_render_to_file(shealth(), "scad/window_slider_lock_shealth.scad", include_orig_code=False)
    scad_render_to_file(tongue(), "scad/window_slider_lock_tongue.scad", include_orig_code=False)

main()
