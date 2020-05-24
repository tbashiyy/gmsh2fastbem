import os
import subprocess

from gmsh2fastbem import createMesh
import shutil

ROOT_DIR = os.path.dirname(__file__)


def main() -> None:
    output_dir = "hoge"
    fastBem_dir = "../FastBEM_Acoustics/"
    fastBem_input_path = "../FastBEM_Acoustics/input.dat"
    fastBem_exe_path = "C:/Users/tbashiyy/PycharmProjects/FastBem/FastBEM_Acoustics/FastBEM_Acoustics.bat"
    path = 'BemResults'
    shape = 'quadrangular_prism'
    # x-off,y-off,z-off 回転は考慮しない
    # data作成
    dataFile = createMesh.main(0, 0, 0)
    dataFilePath = ROOT_DIR + "/output/{0}/{1}.dat".format(shape, dataFile)
    resultFilePath = "C:/Users/tbashiyy/PycharmProjects/FastBem/FastBEM_Acoustics/output_result.dat"
    resultMovedPathBase = ROOT_DIR + "/BemResults/{0}".format(shape)
    print(dataFilePath)
    # fastBemディレクトリへ移動
    shutil.move(dataFilePath, fastBem_input_path)
    # run fastBem
    result = subprocess.run(fastBem_exe_path)

    # 結果データを移動
    if result.returncode == 0:
        shutil.move(resultFilePath, resultMovedPathBase + "/output_({0},{1},{2}).dat".format(0, 0, 0))
        shutil.move(fastBem_input_path, resultMovedPathBase + "/input_({0},{1},{2}).dat".format(0, 0, 0))
        exit(0)
    else:
        exit(1)


main()
