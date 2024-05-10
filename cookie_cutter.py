#!/usr/bin/python3
from typing import Tuple

from solid import scad_render_to_file, translate, linear_extrude, minkowski, hull, polygon, union, intersection, scale
from solid.utils import up, down
from solid.objects import cylinder, sphere, circle, square


D = 0.01
D2 = D * 2
LW = 0.42
H_SIDE = 10
H_SIDE_W0 = H_SIDE - 7
H_SIDE_W1 = H_SIDE - 3

W_SIDE0 = LW * 4
W_SIDE1 = LW * 2

# H_MID = H_SIDE - 1.9
H_MID = H_SIDE - 3.5
W_MID = LW * 7
W_MID0 = LW * 4

K = 0.22

def rescale(k, arr):
    return [(x*k, y*k) for x, y in arr]

def rescale2(k, arr2):
    return [rescale(k, xs) for xs in arr2]

OUTLINE_COORDS = rescale(K, [
    (95.91, 24.30),
    (221.18, 149.32),
    (274.67, 24.57),
    (326.65, 153.66),
    (376.30, 103.66),
    (432.94, 129.26),
    (455.31, 199.83),
    (375.98, 184.14),
    (375.86, 304.35),
    (255.88, 424.22),
    (87.69, 481.09),
    (185.36, 350.30),
    (96.06, 256.56),
])

INTERNAL_LINES = rescale2(K, [
    ((276.18, 204.33), (221.18, 149.32)),
    ((276.18, 204.33), (326.65, 153.66)),
    ((276.18, 204.33), (375.86, 304.35)),
    ((276.18, 204.33), (255.88, 424.22)),
    ((276.18, 204.33), (96.06, 256.56)),
    ((376.30, 103.66), (375.98, 184.14)),
    ((185.36, 350.30), (255.88, 424.22)),
])

POLYS = rescale2(K, [
    [(95.91, 24.30), (276.18, 204.33), (96.06, 256.56)],
    [(221.18, 149.32), (274.67, 24.57), (326.65, 153.66), (276.18, 204.33)],
    [(276.18, 204.33), (376.30, 103.66), (375.86, 304.35)],
    [(376.30, 103.66), (432.94, 129.26), (455.31, 199.83), (375.98, 184.14)],
    [(276.18, 204.33), (375.86, 304.35), (255.88, 424.22)],
    [(255.88, 424.22), (87.69, 481.09), (185.36, 350.30)],
    [(255.88, 424.22), (96.06, 256.56), (276.18, 204.33)],
])

def outline(shape, w, segments=16):
    return minkowski()(shape, circle(r=w, segments=50)) - shape


def base_shape():
    return polygon(OUTLINE_COORDS)

def mesh2d(w):
    lines = list(INTERNAL_LINES)


def mid_spike():
    return (
        cylinder(d=W_MID0, h=H_MID-W_MID/2 + D, segments=30) +
        up(H_MID - W_MID/2)(sphere(d=W_MID, segments=30))
    )


def mid_wall(p1: Tuple[float, float], p2: Tuple[float, float]):
    s = mid_spike()
    return hull()(
        translate(p1)(s),
        translate(p2)(s),
    )

def mid_walls():
    walls = union()
    for p1, p2 in INTERNAL_LINES:
        walls += mid_wall(p1, p2)
    return intersection()(
        walls,
        linear_extrude(H_SIDE, convexity=10)(
            minkowski()(base_shape(), circle(d=W_SIDE1/2, segments=50))
        )
    )


def make_cutter(shape):
    def wall(h, w):
      return linear_extrude(h, convexity=10)(outline(shape, w))

    side = wall(H_SIDE, W_SIDE1) + wall(H_SIDE_W0, W_SIDE0)

    n = 60
    for i in range(n):
        h = H_SIDE_W0 + (H_SIDE_W1 - H_SIDE_W0) * i / n
        w = W_SIDE0 + (W_SIDE1 - W_SIDE0) * i / n
        side += wall(h, w)

    return side


def inverse2d(shape):
    return square([1e5, 1e5], center=True) - shape

def outset(shape, r, segments=50):
    return minkowski()(shape, circle(r=r, segments=segments))

def inset(shape, r):
    return inverse2d(outset(inverse2d(shape), r))


def press():
    a = union()
    gap = 4.
    r = 4.0
    h = 4.0
    base_th = 2
    for poly in POLYS:
        p = down(r)(linear_extrude(r)(inset(polygon(poly), r=gap/2 + r)))
        p = minkowski()(p, sphere(r=r, segments=50))
        p = intersection()(p, down(D)(linear_extrude(r + D2)(polygon(poly))))
        p = scale([1.0, 1.0, h/r])(p)
        a += p

    return a + down(base_th)(linear_extrude(base_th)(outset(base_shape(), 4)))


def final_cutter():
    return make_cutter(base_shape()) + mid_walls()


def outline_cutter():
    return make_cutter(minkowski()(base_shape(), circle(r=10, segments=50)))


def main():
    f_cutter = final_cutter()
    o_cutter = outline_cutter()
    p = press()
    scad_render_to_file(o_cutter, "scad/cookie_cutter_outline_cutter.scad", include_orig_code=False)
    scad_render_to_file(p, "scad/cookie_cutter_press.scad", include_orig_code=False)
    scad_render_to_file(f_cutter, "scad/cookie_cutter_final.scad", include_orig_code=False)


main()
