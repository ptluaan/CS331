import os
import cv2
path = "C:\\Users\\luant\\Downloads\\DUTS-TE\\DUTS-TE\\DUTS-TE-Mask\\"

img_list = os.listdir("image")

i = 0
for name in img_list:
    i += 1
    print(i)
    mask_name = name[:-3] + "png"
    img = cv2.imread(path + mask_name)

    cv2.imwrite("mask\\" + mask_name, img)
    # path_img = path + name

# print(len(img_list))