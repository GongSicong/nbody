# Taken from:
# The Computer Language Benchmarks Game
# https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# 2to3
# modified by Andriy Misyura
# slightly modified by bmmeijers

# Last Modified by:
# Authors: Gong Sicong
# Studentnumbers: 5711932

import sys
from math import sqrt, pi as PI


def combinations(l):
    result = []
    for x in range(len(l) - 1):
        ls = l[x + 1:]
        for y in ls:
            result.append((l[x][0], l[x][1], l[x][2], y[0], y[1], y[2]))
    return result


SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

BODIES = {
    "sun": ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], SOLAR_MASS),
    "jupiter": (
        [4.84143144246472090e00, -1.16032004402742839e00, -1.03622044471123109e-01],
        [
            1.66007664274403694e-03 * DAYS_PER_YEAR,
            7.69901118419740425e-03 * DAYS_PER_YEAR,
            -6.90460016972063023e-05 * DAYS_PER_YEAR,
        ],
        9.54791938424326609e-04 * SOLAR_MASS,
    ),
    "saturn": (
        [8.34336671824457987e00, 4.12479856412430479e00, -4.03523417114321381e-01],
        [
            -2.76742510726862411e-03 * DAYS_PER_YEAR,
            4.99852801234917238e-03 * DAYS_PER_YEAR,
            2.30417297573763929e-05 * DAYS_PER_YEAR,
        ],
        2.85885980666130812e-04 * SOLAR_MASS,
    ),
    "uranus": (
        [1.28943695621391310e01, -1.51111514016986312e01, -2.23307578892655734e-01],
        [
            2.96460137564761618e-03 * DAYS_PER_YEAR,
            2.37847173959480950e-03 * DAYS_PER_YEAR,
            -2.96589568540237556e-05 * DAYS_PER_YEAR,
        ],
        4.36624404335156298e-05 * SOLAR_MASS,
    ),
    "neptune": (
        [1.53796971148509165e01, -2.59193146099879641e01, 1.79258772950371181e-01],
        [
            2.68067772490389322e-03 * DAYS_PER_YEAR,
            1.62824170038242295e-03 * DAYS_PER_YEAR,
            -9.51592254519715870e-05 * DAYS_PER_YEAR,
        ],
        5.15138902046611451e-05 * SOLAR_MASS,
    ),
}

SYSTEM = tuple(BODIES.values())
PAIRS = tuple(combinations(SYSTEM))


def report_energy(bodies=SYSTEM, pairs=PAIRS, e=0.0):
    for ((x1, y1, z1), v1, m1, (x2, y2, z2), v2, m2) in pairs:
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
    for (r, [vx, vy, vz], m) in bodies:
        e += m * (vx * vx + vy * vy + vz * vz) / 2.0
    print("Energy: %.9f" % e)


def offset_momentum(ref, bodies=SYSTEM, px=0.0, py=0.0, pz=0.0):
    for (r, [vx, vy, vz], m) in bodies:
        px -= vx * m
        py -= vy * m
        pz -= vz * m
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m


import time

list_name = ["sun", "jupiter", "saturn", "uranus", "neptune"]


def advance(dt, bodies=SYSTEM, pairs=PAIRS):
    for ([x1, y1, z1], v1, m1, [x2, y2, z2], v2, m2) in pairs:
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        dist = sqrt(dx * dx + dy * dy + dz * dz)
        mag = dt / (dist * dist * dist)
        b1m = m1 * mag
        b2m = m2 * mag
        v1[0] -= dx * b2m
        v1[1] -= dy * b2m
        v1[2] -= dz * b2m
        v2[2] += dz * b1m
        v2[1] += dy * b1m
        v2[0] += dx * b1m
    for (r, [vx, vy, vz], m) in bodies:
        r[0] += dt * vx
        r[1] += dt * vy
        r[2] += dt * vz


def write(n, output, bodies=SYSTEM):
    if output:
        file = open("result_python.csv", mode='a')
        file.writelines("name of the body;position x;position y;position z;step\n")
        for i in range(n):
            for j, ([x, y, z], volcity, mass) in enumerate(bodies):
                line = list_name[j] + ";" + str(x) + ";" + str(y) + ";" + str(z) + ";" + str(i) + "\n"
                file.write(line)
            advance(0.01)
        file.close()
    else:
        for i in range(n):
            advance(0.01)


def main(ref="sun"):
    n_1 = 5000
    n_2 = 500000 - n_1
    n_3 = 5000000 - n_2 - n_1
    n_4 = 50000000 - n_3 - n_2 - n_1
    file = open("result_python.csv", mode='w')
    offset_momentum(BODIES[ref])
    report_energy()
    start = time.time()

    write(n_1, True, SYSTEM)
    print((time.time() - start) * 1000, "ms")
    report_energy()

    write(n_2, False, SYSTEM)
    print((time.time() - start) * 1000, "ms")
    report_energy()

    write(n_3, False, SYSTEM)
    print((time.time() - start) * 1000, "ms")
    report_energy()

    write(n_4, False, SYSTEM)
    print((time.time() - start) * 1000, "ms")
    report_energy()


if __name__ == "__main__":
    main()
