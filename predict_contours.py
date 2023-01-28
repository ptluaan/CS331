from mediapipe.python import solutions
from background_replacement import *
import os
import numpy as np

path_img = "Test\\image\\"
path_mask = "Test\\mask\\"

img_list = os.listdir(path_img)

for blur in range(15,45,5) :
    for min_area in range (50, 300, 25) :
        for max_area in range (700, 1000, 25) :
            for canny_low in range (5,100,5) :
                for canny_high in range(100,255,15) :
                    dilate_iter = 10
                    erode_iter = 10
                    # threshold = ii / 100
                    _contours  = background_replacement_contours()
                    _contours.set_parameters(blur,canny_low,canny_high,min_area/1000.0, max_area/1000.0, dilate_iter, erode_iter)
                
                    # _mediapipe.set_parameters(threshold)

                    result = 0

                    for name in img_list:
                        mask_name = name[:-3] + "png"
                        img = cv2.imread(path_img + name)
                        img_test = cv2.imread(path_mask + mask_name, 0)
                        
                        mask, _ = _contours.solution(img, img)

                        count = 0
                        count = np.sum(mask != img_test) #(mask[:] != img_test[:]) 
                        size = mask.shape[0] * mask.shape[1]
                        mae_score = 1.0 * count / (size)
                        result += mae_score
                        # print(count, size, mae_score)

                        # if (i == 10) : break
                        # cv2.imwrite("mask\\" + mask_name, img)
                    result /= len(img_list)
                    print(blur, canny_low, canny_high, min_area, max_area, result)
                    # break