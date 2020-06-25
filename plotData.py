from typing import *

import matplotlib.pyplot as plt
import numpy as np
import os

ROOT_DIR = os.path.dirname(__file__)


def main(input_path: str, output_path: str, condition: Tuple[float, float, float, str]) -> None:
    fieldPoints = get_field_cells(input_path)
    pressure_scattered = get_pressure_scattered(output_path)
    if len(fieldPoints) != len(pressure_scattered):
        Exception('size is different')

    field = np.array(fieldPoints)
    pressure = np.linalg.norm(np.array(pressure_scattered), axis=1).reshape(len(pressure_scattered), 1)

    x = field[:, 0]
    z = field[:, 2]

    X = ((x - min(x)) / max((x - min(x))) * 10).round(1).reshape(len(x), 1)
    Z = ((z - min(z)) / max((z - min(z))) * 10).round(1).reshape(len(z), 1)
    XYZ = np.concatenate([X, Z, pressure], 1)

    # C_p = get_default_pressure(XYZ)
    C_p = get_thin_out_pressure(XYZ)

    plt.pcolor(C_p, cmap="Blues")
    cbar = plt.colorbar()
    cbar.set_label("[Pa]", rotation=360)
    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title("(x={0}, y={1}, z={2}) {3}".format(condition[0], condition[1], condition[2], condition[3]))
    plt.show()
    exit(0)


# Filed Pointsをinput.datから取得する。(x,y,z)
def get_field_cells(path: str) -> List[List[float]]:
    with open(path) as f:
        lines = f.readlines()

    fieldPoints: List[List[float]] = []
    lineStart: int = 0
    lineEnd: int = 0

    for i, line in enumerate(lines):
        if '$ Field Points' in line:
            lineStart = i + 1
        if '$ Field Cells' in line:
            lineEnd = i

    for line in lines[lineStart:lineEnd]:
        fieldPointData = line.split()
        fieldPoints.append([float(fieldPointData[1]), float(fieldPointData[2]), float(fieldPointData[3])])

    print(fieldPoints)
    return fieldPoints


def get_pressure_scattered(path: str) -> List[List[float]]:
    with open(path) as f:
        lines = f.readlines()

    scatteredPressure: List[List[float]] = []
    lineStart: int = 0
    lineEnd: int = 0

    for i, line in enumerate(lines):
        if 'Solution at the Field Points:' in line:
            lineStart = i + 3
        if 'Sound power (W) radiated by structure' in line:
            lineEnd = i - 1

    for line in lines[lineStart:lineEnd]:
        splitData = line[99:124].split(',')
        scatteredPressure.append([float(splitData[0]), float(splitData[1])])

    return scatteredPressure


def get_default_pressure(xyz):
    C = np.empty((11, 11))
    C_p = np.empty((10, 10))
    for point in xyz:
        C[int(point[0]), int(point[1])] = point[2]

    for i in range(0, 10):
        for j in range(0, 10):
            # C_p[z, x]に変換
            C_p[j, i] = np.sqrt(C[i, j] ** 2 + C[i + 1, j] ** 2 + C[i, j + 1] ** 2 + C[i + 1, j + 1] ** 2) * 0.5

    print(C_p)
    return C_p


def get_thin_out_pressure(xyz):
    C_p = np.empty((10, 10))
    C_p_calculate = np.empty((10, 10))
    C = np.empty((11, 11))

    for point in xyz:
        C[int(point[0]), int(point[1])] = point[2]

    # まず、実際のセンサ部分の音圧を計算する
    for i in range(0, 10):
        for j in range(0, 10):
            if (i + j) % 2 == 0:
                C_p[j, i] = np.sqrt(C[i, j] ** 2 + C[i + 1, j] ** 2 + C[i, j + 1] ** 2 + C[i + 1, j + 1] ** 2) * 0.5
            else:
                C_p[j, i] = 0

    for i in range(0, 10):
        for j in range(0, 10):
            if (i + j) % 2 == 0:
                C_p_calculate[j, i] = C_p[j, i]
            else:
                C_p_calculate[j, i] = np.sqrt(C[j-1, i-1] ** 2 + C[j-1, i+1] ** 2 + C[j+1, i-1] ** 2 + C[j+1, i+1] ** 2) * 0.5

    return C_p_calculate


# Test
def normTest() -> None:
    pressure_scattered = [[1, -5], [2, 3]]
    pressure = np.array(pressure_scattered)
    print(np.linalg.norm(pressure, axis=1))


input_path_sample = ROOT_DIR + "/BemResults/quadrangular_prism/input_(5,20,5).dat"
output_path_sample = ROOT_DIR + "/BemResults/quadrangular_prism/output_(5,20,5).dat"
main(input_path_sample, output_path_sample, (5, 20, 5, "Plane Wave"))
