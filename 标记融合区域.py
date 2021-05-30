from PIL import Image
import numpy as np

# phasemaplist = ["E:/testimage/phasemap/44abphasemap.bmp",
#                 "E:/testimage/phasemap/47abphasemap.bmp",
#                 "E:/testimage/phasemap/55abphasemap.bmp",
#                 "E:/testimage/phasemap/60abphasemap.bmp",
#                 "E:/testimage/phasemap/80abphasemap.bmp",
#                 "E:/testimage/phasemap/90abphasemap.bmp",
#                 "E:/testimage/phasemap/110abphasemap.bmp"];

phasemaplist = ["E:/testimage/phasemap/44p2zhuphasemap.bmp",
                "E:/testimage/phasemap/47p2zhuphasemap.bmp",
                "E:/testimage/phasemap/55p2zhuphasemap.bmp",
                "E:/testimage/phasemap/60p2zhuphasemap.bmp",
                "E:/testimage/phasemap/80p2zhuphasemap.bmp",
                "E:/testimage/phasemap/90p2zhuphasemap.bmp",
                "E:/testimage/phasemap/110p2zhuphasemap.bmp"];

tabMatrixFilePath = "E:/testimage/tabMatrix.txt"
lightMatrixFilePath = "E:/testimage/lightMatrix.txt"
# firstPhaseMapFilePath = "E:/testimage/phasemap/120abphasemap.bmp"
firstPhaseMapFilePath = "E:/testimage/phasemap/120p2zhuphasemap.bmp"
light = [43, 47, 55, 60, 80, 90, 111,255]

phaseMatrix = []
for i in range(len(phasemaplist)):
    imgmat = np.array(Image.open(phasemaplist[i]).convert("RGB"))
    phaseMatrix.append(imgmat)


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

mask1 = np.ones((1024, 1280), dtype=np.int32)
for row in range(1024):
    for col in range(1280):
        if tabmask[row][col]==1:
            mask1[row][col] = 0

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

# 将包含未饱和区域的相位图读取到矩阵
firstPhaseMatrix = np.array(Image.open(firstPhaseMapFilePath).convert("RGB"))

for i in range(1024):
    for j in range(1280):
        if mask1[i][j]==1:
            firstPhaseMatrix[i][j]=[255,0,0]
        if mask[0][i][j]==1:
            phaseMatrix[0][i][j]=[255,165,0]
        if mask[1][i][j]==1:
            phaseMatrix[1][i][j]=[255,255,0]
        if mask[2][i][j]==1:
            phaseMatrix[2][i][j]=[0,255,0]
        if mask[3][i][j]==1:
            phaseMatrix[3][i][j]=[0,127,255]
        if mask[4][i][j]==1:
            phaseMatrix[4][i][j]=[0,0,255]
        if mask[5][i][j]==1:
            phaseMatrix[5][i][j]=[139,0,255]
        if mask[6][i][j]==1:
            phaseMatrix[6][i][j]=[255,192,203]



img = Image.fromarray(firstPhaseMatrix)
img.show()
img.save("E:/毕业论文/配图/融合标记示意图/firstzhuphasemaptab.bmp")

img0 = Image.fromarray(phaseMatrix[0])
img0.save("E:/毕业论文/配图/融合标记示意图/zhuphasemaptab0.bmp")
img1 = Image.fromarray(phaseMatrix[1])
img1.save("E:/毕业论文/配图/融合标记示意图/zhuphasemaptab1.bmp")
img2 = Image.fromarray(phaseMatrix[2])
img2.save("E:/毕业论文/配图/融合标记示意图/zhuphasemaptab2.bmp")
img3 = Image.fromarray(phaseMatrix[3])
img3.save("E:/毕业论文/配图/融合标记示意图/zhuphasemaptab3.bmp")
img4 = Image.fromarray(phaseMatrix[4])
img4.save("E:/毕业论文/配图/融合标记示意图/zhuphasemaptab4.bmp")
img5 = Image.fromarray(phaseMatrix[5])
img5.save("E:/毕业论文/配图/融合标记示意图/zhuphasemaptab5.bmp")
img6 = Image.fromarray(phaseMatrix[6])
img6.save("E:/毕业论文/配图/融合标记示意图/zhuphasemaptab6.bmp")