from mediapipe.python import solutions
from background_replacement import *
import os
import numpy as np

path_img = "Test\\image\\"
path_mask = "Test\\mask\\"

img_list = os.listdir(path_img)

for ii in range(5,100,5) : 
    threshold = ii / 100
    _mediapipe = background_replacement_mediapipe()
    _mediapipe.set_parameters(threshold)

    result = 0

    for name in img_list:
        mask_name = name[:-3] + "png"
        img = cv2.imread(path_img + name)
        img_test = cv2.imread(path_mask + mask_name, 0)
        
        mask, _ = _mediapipe.solution(img, img)

        count = 0
        count = np.sum(mask != img_test) #(mask[:] != img_test[:]) 
        size = mask.shape[0] * mask.shape[1]
        mae_score = 1.0 * count / (size)
        result += mae_score
        # print(count, size, mae_score)

        # if (i == 10) : break
        # cv2.imwrite("mask\\" + mask_name, img)
    result /= len(img_list)
    print(threshold, result)