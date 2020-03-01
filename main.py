import numpy as np

#読み込みファイルを指定
f = open('./gmshSource/newMesh0223_meshsize01')

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
