#!/usr/bin/python3

# Stand for Logitech Ergo MX trackball.
#
# The trackball is too horizontal to me, built-in adjustment
# is not enough for comfortable hand placement.
# The stand holds the trackball in a vertical position and
# allows for slight adjustments.

# import math
from math import sqrt, pi, atan, sin, cos, atan2, tan, acos
from pprint import pprint
from typing import List

from solid import scad_render_to_file, translate, linear_extrude, rotate_extrude, \
    rotate, difference, intersection, color
from solid.objects import union, polygon, sphere, color, polyhedron, cylinder, \
    circle, cube, square, import_scad

from scipy import interpolate
utils = import_scad('scad-utils/morphology.scad')


D = 0.01
D2 = D * 2

def corner_cutout(r, h):
    p = square([r + D, r + D])
    p -= circle(r=r, segments=100)
    return linear_extrude(h)(p)


def trackball_stand():
    # a = pi / 2 * 0.6
    a = pi / 2 * 0.7
    a2 = a / 2
    l1 = 50
    l2 = 35
    l2_1 = 10
    th = 5

    lead = th / tan(a2)
    profile = [
        (0, 0),
        (l1, 0),
        (l1, th),
        (lead, th),
        (lead + (l2 - lead) * cos(a), th + (l2 - lead) * sin(a)),
        (l2 * cos(a), l2 * sin(a))
    ]
    # plate = cube([100, 50, 4])
    # plate_r = rotate(60, [1, 0, 0])(cube([100, 50, 4]))

    # obj = plate + plate_r
    obj = rotate(90, [1, 0, 0])(linear_extrude(100, convexity=10)(
        utils.fillet(r=7, segments=100)(polygon(profile))
    ))

    obj -= translate([40, -30, 5 + 1.20])(cube([11, 11, 10], center=True))
    obj -= translate([40, -70, 5 + 1.20])(cube([11, 11, 10], center=True))

    r = 10
    obj -= translate([l1 - r, -r, -D])(corner_cutout(r, th + D2))
    obj -= translate([l1 - r, -100 + r, -D])(rotate(-90)(corner_cutout(r, th + D2)))

    obj = rotate(-180 + a * 180 / pi, [0, 1, 0])(obj)

    cd = 80
    obj += translate([-10, -100, 0])(
        cube([l2_1 + 10, 100, 1.2]) *
        translate([-cd/2 + 10 + 7, 100/2, 0])(cylinder(d=cd, segments=200))
    )

    adhesive_w = 26.0
    adhesive_h = 0.75
    adhesive_hole = rotate(-90, [0, 1, 0])(linear_extrude(l2 + D2)(polygon([
        [-D, -1],
        [-D, adhesive_w + 1],
        [adhesive_h, adhesive_w + D],
        [adhesive_h, -D]
    ])))
    for x in -adhesive_w, -100:
        obj -= translate([- D, x - D, 0])(
            adhesive_hole
            # cube([l2 + D2, adhesive_w + D2, 0.75 + D])
        )

    # return obj
    return rotate(-90, [1, 0, 0])(obj)


def pad():
    xw = 45
    yw = 30
    h = 0.6
    obj = cube([xw, yw, h])
    # for i in range(int(xw / 0.8)):
    #     obj += translate([i * 0.8, 0, h - D])(cube([0.4, yw, 0.2 + D]))

    return obj


def main():
    r = trackball_stand()
    scad_render_to_file(trackball_stand(), "scad/trackball_stand.scad", include_orig_code=False)
    scad_render_to_file(pad(), "scad/trackball_pad.scad", include_orig_code=False)

main()
