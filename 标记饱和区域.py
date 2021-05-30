from PIL import Image
import numpy as np

img = Image.open("E:/testimage/cropped_left/ScanIm_13_120_camera1.bmp")
i_array = np.array(img)

img_rgb = img.convert("RGB")
img_array = np.array(img_rgb)
print(img_array.shape)
w = img.size[0]
h = img.size[1]
print(w)
print(h)
count = 0

#阈值判断
for i in range(h):
    print(i)
    for j in range(w):
        if i_array[i,j]>248:
            img_array[i, j] = [255, 0, 0]
            count=count+1
            #[255, 0, 0]为红色，[255, 255, 255]为白色，[0, 0, 0]为黑色等

img3 = Image.fromarray(img_array)
img3.save("E:\\毕业论文\\simulation\\cropped\\ScanIm_13_120_camera1_saturation.bmp")
print(count)
