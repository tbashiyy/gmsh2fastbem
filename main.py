import numpy as np
from typing import Tuple, List


def main() -> None:
    nodes, elements = readFile('./gmshSource/newMesh0223_meshsize01')
    print(len(nodes))
    print(len(elements))
    writeFile('./output/resultfile.dat', nodes, elements)

#読み込み
def readFile(filename: str) -> Tuple[List[str], List[str]]:
    print('start file reading...')
    f = open(filename, mode='r')

    nodes = []
    elements =  []
    nodesLength = 0
    elementsLength = 0

    line = f.readline()

    #Nodesまで行を飛ばす
    while line:
        if(line == '$Nodes\n'):
            line = f.readline()
            nodesLength = int(line)
            break
        else:
            line = f.readline()


    #カウント部分を飛ばすS
    line = f.readline()

    #Nodes読み込み
    while line:
        if(line == '$EndNodes\n'):
            line = f.readline()
            break
        else:
            nodes.append(line)
            line = f.readline()

    #カウント部分を飛ばす
    line = f.readline()
    elementsLength = int(line)
    line = f.readline()

    #Elements読み込み
    while line:
        if(line == '$EndElements\n'):
            break
        else:
            elements.append(line)
            line = f.readline()

    #データ長チェック
    if(len(nodes) != nodesLength):
        raise Exception('Illegal data length')

    if(len(elements) != elementsLength):
        raise Exception('Illegal data length')
    
    f.close()

    transferedNodes = []
    transferedElements = []

    for node in nodes:
        ret = node.split(' ')
        x = float(ret[1])
        y = float(ret[2])
        z = float(ret[3])
        transferedNodes.append("{0} {1} {2} {3}\n".format(ret[0],x,y,z))
    
    for element in elements:
        ret = element.split(' ')
        n1 = int(ret[5])
        n2 = int(ret[6])
        n3 = int(ret[7])
        transferedElements.append("{0} {1} {2} {3} 2 (0.0000000000D+00, 0.0000000000D+00) {4}\n".format(ret[0],n1,n2,n3,ret[4]))

    print('end reading.')
    return transferedNodes, transferedElements

#writing
def writeFile(fileName: str, nodes: List[str], elements: List[str]) -> None:
    print('start file writing...')
    f = open(fileName, mode='w')
    f.write('$Nodes:\n')
    f.writelines(nodes)
    f.write('$Elements and Boundary Conditions:\n')
    f.writelines(elements)
    f.close()
    print('end writing.')


#実行
main()
