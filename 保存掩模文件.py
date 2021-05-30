import numpy as np
from PIL import Image


# phasemaplist = ["E:/testimage/phasemap/44abphasemap.bmp",
#                 "E:/testimage/phasemap/47abphasemap.bmp",
#                 "E:/testimage/phasemap/55abphasemap.bmp",
#                 "E:/testimage/phasemap/60abphasemap.bmp",
#                 "E:/testimage/phasemap/80abphasemap.bmp",
#                 "E:/testimage/phasemap/90abphasemap.bmp",
#                 "E:/testimage/phasemap/110abphasemap.bmp"];

maskfilelist = ["E:/testimage/cropped/maskfile/mask1.txt",
                "E:/testimage/cropped/maskfile/mask2.txt",
                "E:/testimage/cropped/maskfile/mask3.txt",
                "E:/testimage/cropped/maskfile/mask4.txt",
                "E:/testimage/cropped/maskfile/mask5.txt",
                "E:/testimage/cropped/maskfile/mask6.txt",
                "E:/testimage/cropped/maskfile/mask7.txt",
                "E:/testimage/cropped/maskfile/mask8.txt"];

tabMatrixFilePath = "E:/testimage/cropped/2tabMatrix.txt"
lightMatrixFilePath = "E:/testimage/cropped/2lightMatrix.txt"

light = [44, 55, 60, 80, 100, 110, 120, 255]

# 读取饱和标记掩模文件
tabmask = np.ones((1024, 1280), dtype=np.int32)
tabfileobj = open(tabMatrixFilePath, "r")
line = tabfileobj.readline() # 读取第一行
tabcount = 0
while line:
    tabmask[tabcount] = [int(i) for i in line.split()] # 将每一行变成列表放入tabmask每一行
    tabcount += 1
    line = tabfileobj.readline() # 读取下一行
tabfileobj.close()

mask1file = open(maskfilelist[0],"w")
mask1 = np.ones((1024, 1280), dtype=np.int32)
for row in range(1024):
    for col in range(1280):
        if tabmask[row][col]==1:
            mask1[row][col] = 0
        mask1file.write(str(mask1[row][col])+' ')
    mask1file.write('\n')
mask1file.close()

# 读取亮度矩阵文件
lightMatrix = np.ones((1024, 1280), dtype=np.int32)
lightfobj = open(lightMatrixFilePath, "r")
line = lightfobj.readline() # 读取第一行
lcount = 0
while line:
    lightMatrix[lcount] = [int(i) for i in line.split()] # 将每一行变成列表放入lightMatrix每一行
    lcount += 1
    line = lightfobj.readline() # 读取下一行
lightfobj.close()

# 创建一个掩模列表
mask = []
for i in range(len(light)-1):
    mask.append(np.zeros((1024, 1280), dtype=np.int32))
    for row in range(1024):
        for col in range(1028):
            if lightMatrix[row][col]>light[i] and lightMatrix[row][col]<light[i+1]:
                mask[i][row][col] = 1

summask = np.zeros((1024, 1280), dtype=np.int32)
for i in range(1, len(mask)):
    summask += mask[i]
mask[0] = tabmask - summask

for i in range(7):
    mask1file = open(maskfilelist[i+1],"w")
    for row in range(1024):
        for col in range(1280):
            mask1file.write(str(mask[i][row][col])+' ')
        mask1file.write('\n')
    mask1file.close()
