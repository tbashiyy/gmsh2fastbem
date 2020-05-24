from typing import Tuple, List


def main(x: float, y: float, z: float) -> str:
    dir_name = 'quadrangular_prism'
    file_name = 'quadrangular_prism_({0},{1},{2})'.format(x, y, z)
    nodes, elements = readFile('./gmshSource/' + dir_name + '/' + dir_name)
    print(len(nodes))
    print(len(elements))
    writeFile('./output/' + dir_name + '/' + file_name + '.dat', nodes, elements, (x, y, z))
    return file_name


# 読み込み
def readFile(filename: str) -> Tuple[List[str], List[str]]:
    print('start file reading...')
    f = open(filename, mode='r')

    nodes = []
    elements = []
    nodesLength = 0

    line = f.readline()

    # Nodesまで行を飛ばす
    while line:
        if line == '$Nodes\n':
            line = f.readline()
            nodesLength = int(line)
            break
        else:
            line = f.readline()

    # カウント部分を飛ばすS
    line = f.readline()

    # Nodes読み込み
    while line:
        if line == '$EndNodes\n':
            line = f.readline()
            break
        else:
            nodes.append(line)
            line = f.readline()

    # カウント部分を飛ばす
    line = f.readline()
    elementsLength = int(line)
    line = f.readline()

    # Elements読み込み
    while line:
        if line == '$EndElements\n':
            break
        else:
            elements.append(line)
            line = f.readline()

    # データ長チェック
    if len(nodes) != nodesLength:
        raise Exception('Illegal data length')

    if len(elements) != elementsLength:
        raise Exception('Illegal data length')

    f.close()

    transferredNodes = []
    transferredElements = []

    for node in nodes:
        ret = node.split(' ')
        x = '{0:.15f}'.format(float(ret[1])).rjust(18)
        y = '{0:.15f}'.format(float(ret[2])).rjust(18)
        z = '{0:.15f}'.format(float(ret[3])).rjust(18)
        transferredNodes.append("      {0}  {1}D+00  {2}D+00  {3}D+00\n".format(ret[0].rjust(5), x, y, z))

    elemCount = 1
    for element in elements:
        ret = element.split(' ')
        if len(ret) == 8:
            n1 = ret[5].rjust(5)
            n2 = ret[6].rjust(5)
            n3 = ret[7].strip('\n').rjust(5)
            transferredElements.append(
                "      {0}  {1}    {2}    {3}       2  (   0.000000000000000D+00   0.000000000000000D+00)\n".format(
                    str(elemCount).rjust(5), n1, n2, n3))
            elemCount += 1

    print('end reading.')
    return transferredNodes, transferredElements


# writing
def writeFile(fileName: str, nodes: List[str], elements: List[str], offsets: Tuple[float, float, float]) -> None:
    print('start file writing...')
    f = open(fileName, mode='w')
    f.write('A Sphere Model for Acoustic Scattering Analysis\n')
    f.write(
        '  Complete    1      1                ! Job Type (Complete/Field Only/ATM/Use ATM); Solver (1=FMBEM/2=ACA/3=CBEM/4=HFBEM); No. threads\n')
    f.write(
        '   Full       0      0.d0              ! Problem Space, Symmetry Plane, Symmetry Plane Property (1=Rigid; -1=Soft)\n')
    f.write(
        '  {0}       {1}     121     100       ! Nos. of Boundary Elements/Nodes, and Nos. of Field Points/Cells, No. of panels\n'.format(
            str(len(elements)).rjust(5), str(len(nodes)).rjust(5)))
    f.write('      1       0                       ! No. of plane incident waves, User defined sources (1=Yes/0=No)\n')
    f.write(' (1., 0.)    0.     -1.      0.       ! Complex amplitude and direction vector of the plane wave(s)\n')
    f.write('      0       0                       ! No. of monopoles, and No. of dipoles\n')
    f.write(
        '    343.   1.29  2.d-5  1.d-12    0.  ! cspeed, density, Ref. pressure, Ref. intensity, complex wavenumber k ratio\n')
    f.write(
        '  40000   40000      1       0    0   ! Freq1, Freq2, No. freqs, NOctave, Update BCs for each frequency (1=Yes/0=No)\n')
    f.write(
        '      0       3      1       0  One   ! Dual BIE (1=Yes/0=No), nruleb (1-6), nrulef (1-6), animation (1=Yes/0=No), Tecplot data (All/One)\n')
    f.write(' $ Nodes:\n')
    f.writelines(nodes)
    f.write(' $ Elements and Boundary Conditions:\n')
    f.writelines(elements)
    f.write(' $ Field Points\n')
    f.writelines(get_field_points(offsets[0], offsets[1], offsets[2]))
    f.write(' $ Field Cells\n')
    f.writelines(get_field_cells())
    f.write(' $ End of the File\n')
    f.close()
    print('end writing.')


# createField
def get_field_points(offset_x: float, offset_y: float, offset_z: float) -> List[str]:
    base_distance = 0.06

    count = 1
    points = []
    # オフセットは -5 ~ 0 , 0.1刻み
    for z in range(0, 11):
        for x in range(0, 11):
            points.append("   {0}          {1:.8f}          {2:.8f}          {3:.8f}\n".format(count, float((x+offset_x) * 0.01), base_distance + offset_y, float((z+offset_z) * 0.01)))
            count += 1

    return points


def get_field_cells() -> List[str]:
    count = 0
    cells = []
    for i in range(1, 110):
        if i % 11 == 0:
            continue

        cells.append("   {0}          {1}          {2}          {3}          {4}\n".format(count, i, i + 1, i + 12, i + 11))
        count += 1

    return cells
