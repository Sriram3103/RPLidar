import math
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

EXTEND_AREA = 1.0


def file_read(f):
    with open(f) as data:
        measures = [line.split(",") for line in data]
    angles = []
    distances = []
    for measure in measures:
        angles.append(float(measure[0]))
        distances.append(float(measure[1]))
    angles = np.array(angles)
    distances = np.array(distances)
    return angles, distances


def wu_line(start, end):
    x1, y1 = start
    x2, y2 = end
    points = []

    dx = x2 - x1
    dy = y2 - y1
    is_steep = abs(dy) > abs(dx)

    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1
    gradient = dy / dx if dx != 0 else 1

    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = 1 - fractional_part(x1 + 0.5)
    xpxl1 = xend
    ypxl1 = int(yend)

    if is_steep:
        points.append((ypxl1, xpxl1))
        points.append((ypxl1 + 1, xpxl1))
    else:
        points.append((xpxl1, ypxl1))
        points.append((xpxl1, ypxl1 + 1))

    intery = yend + gradient

    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fractional_part(x2 + 0.5)
    xpxl2 = xend
    ypxl2 = int(yend)

    if is_steep:
        points.append((ypxl2, xpxl2))
        points.append((ypxl2 + 1, xpxl2))
    else:
        points.append((xpxl2, ypxl2))
        points.append((xpxl2, ypxl2 + 1))

    for x in range(int(xpxl1 + 1), int(xpxl2)):
        if is_steep:
            points.append((int(intery), x))
            points.append((int(intery) + 1, x))
        else:
            points.append((x, int(intery)))
            points.append((x, int(intery) + 1))
        intery += gradient

    return np.array(points)


def fractional_part(value):
    return value - int(value)


def calc_grid_map_config(ox, oy, xy_resolution):
    min_x = round(min(ox) - EXTEND_AREA / 2.0)
    min_y = round(min(oy) - EXTEND_AREA / 2.0)
    max_x = round(max(ox) + EXTEND_AREA / 2.0)
    max_y = round(max(oy) + EXTEND_AREA / 2.0)
    xw = int(round((max_x - min_x) / xy_resolution))
    yw = int(round((max_y - min_y) / xy_resolution))
    print("The grid map is ", xw, "x", yw, ".")
    return min_x, min_y, max_x, max_y, xw, yw


def atan_zero_to_twopi(y, x):
    angle = math.atan2(y, x)
    if angle < 0.0:
        angle += math.pi * 2.0
    return angle

def init_flood_fill(center_point, obstacle_points, xy_points, min_coord, xy_resolution):
    center_x, center_y = center_point
    prev_ix, prev_iy = center_x - 1, center_y
    ox, oy = obstacle_points
    xw, yw = xy_points
    min_x, min_y = min_coord  # Fix here
    occupancy_map = (np.ones((xw, yw))) * 0.5
    for (x, y) in zip(ox, oy):
        ix = int(round((x - min_x) / xy_resolution))
        iy = int(round((y - min_y) / xy_resolution))
        free_area = wu_line((prev_ix, prev_iy), (ix, iy))
        for fa in free_area:
            occupancy_map[fa[0]][fa[1]] = 0  # free area 0.0
        prev_ix = ix
        prev_iy = iy
    return occupancy_map

def flood_fill(center_point, occupancy_map):
    sx, sy = occupancy_map.shape
    fringe = deque()
    fringe.appendleft(center_point)
    while fringe:
        n = fringe.pop()
        nx, ny = n
        if nx > 0:
            if occupancy_map[nx - 1, ny] == 0.5:
                occupancy_map[nx - 1, ny] = 0.0
                fringe.appendleft((nx - 1, ny))
        if nx < sx - 1:
            if occupancy_map[nx + 1, ny] == 0.5:
                occupancy_map[nx + 1, ny] = 0.0
                fringe.appendleft((nx + 1, ny))
        if ny > 0:
            if occupancy_map[nx, ny - 1] == 0.5:
                occupancy_map[nx, ny - 1] = 0.0
                fringe.appendleft((nx, ny - 1))
        if ny < sy - 1:
            if occupancy_map[nx, ny + 1] == 0.5:
                occupancy_map[nx, ny + 1] = 0.0
                fringe.appendleft((nx, ny + 1))


def generate_ray_casting_grid_map(ox, oy, xy_resolution, use_wu_line=True):
    min_x, min_y, max_x, max_y, x_w, y_w = calc_grid_map_config(
        ox, oy, xy_resolution)
    occupancy_map = np.ones((x_w, y_w)) / 2
    center_x = int(round(-min_x / xy_resolution))
    center_y = int(round(-min_y / xy_resolution))

    if use_wu_line:
        for (x, y) in zip(ox, oy):
            ix = int(round((x - min_x) / xy_resolution))
            iy = int(round((y - min_y) / xy_resolution))
            laser_beams = wu_line((center_x, center_y), (ix, iy))
            for laser_beam in laser_beams:
                occupancy_map[laser_beam[0]][laser_beam[1]] = 0.0
            occupancy_map[ix][iy] = 1.0
            occupancy_map[ix + 1][iy] = 1.0
            occupancy_map[ix][iy + 1] = 1.0
            occupancy_map[ix + 1][iy + 1] = 1.0
    else:
        occupancy_map = init_flood_fill((center_x, center_y), (ox, oy),
                                        (x_w, y_w),
                                        (min_x, min_y), xy_resolution)
        flood_fill((center_x, center_y), occupancy_map)
        occupancy_map = np.array(occupancy_map, dtype=float)
        for (x, y) in zip(ox, oy):
            ix = int(round((x - min_x) / xy_resolution))
            iy = int(round((y - min_y) / xy_resolution))
            occupancy_map[ix][iy] = 1.0
            occupancy_map[ix + 1][iy] = 1.0
            occupancy_map[ix][iy + 1] = 1.0
            occupancy_map[ix + 1][iy + 1] = 1.0
    return occupancy_map, min_x, max_x, min_y, max_y, xy_resolution



def main():
    print(_file_, "start")
    xy_resolution = 0.02
    ang, dist = file_read("lidar01.csv")
    ox = np.sin(ang) * dist
    oy = np.cos(ang) * dist
    occupancy_map, min_x, max_x, min_y, max_y, xy_resolution = \
        generate_ray_casting_grid_map(ox, oy, xy_resolution, True)
    xy_res = np.array(occupancy_map).shape
    plt.figure(1, figsize=(10, 4))
    plt.subplot(122)
    plt.imshow(occupancy_map, cmap="PiYG_r")
    plt.clim(-0.4, 1.4)
    plt.gca().set_xticks(np.arange(-.5, xy_res[1], 1), minor=True)
    plt.gca().set_yticks(np.arange(-.5, xy_res[0], 1), minor=True)
    plt.grid(True, which="minor", color="w", linewidth=0.6, alpha=0.5)
    plt.colorbar()
    plt.subplot(121)
    plt.plot([oy, np.zeros(np.size(oy))], [ox, np.zeros(np.size(oy))], "ro-")
    plt.axis("equal")
    plt.plot(0.0, 0.0, "ob")
    plt.gca().set_aspect("equal", "box")
    bottom, top = plt.ylim()
    plt.ylim((top, bottom))
    plt.grid(True)
    plt.show()


if __name__ == '_main_':
    main()