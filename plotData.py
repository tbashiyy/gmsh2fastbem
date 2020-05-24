from typing import *

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import norm


def main(input_path: str, output_path: str) -> None:
    fieldPoints = get_field_cells(input_path)
    pressure_scattered = get_pressure_scattered(output_path)
    if len(fieldPoints) != len(pressure_scattered):
        Exception('size is different')

    field = np.array(fieldPoints)
    pressure = norm(np.array(pressure_scattered), axis=1).reshape(len(pressure_scattered), 1)

    x = field[:, 0]
    z = field[:, 2]

    X = ((x - min(x)) / max((x - min(x))) * 10).round(1).reshape(len(x), 1)
    Z = ((z - min(z)) / max((z - min(z))) * 10).round(1).reshape(len(z), 1)
    XYZ = np.concatenate([X, Z, pressure], 1)

    C = np.empty((11, 11))
    C_p = np.empty((10, 10))

    for point in XYZ:
        C[int(point[0]), int(point[1])] = point[2]

    for i in range(0,10):
        for j in range(0, 10):
            C_p[i, j] = np.sqrt(C[i, j]**2 + C[i+1, j]**2 + C[i, j+1]**2 + C[i+1, j+1]**2)*0.5

    plt.pcolor(C_p)
    plt.colorbar()
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

    print(scatteredPressure)
    return scatteredPressure

