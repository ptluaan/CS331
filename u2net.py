import cv2
from rembg import remove
import numpy as np
input_path = 'images/md.jpg'
output_path = 'output.jpg'
bg_path = 'images/Untitled.jpg'

img = cv2.imread(input_path)
img_bg = cv2.imread(bg_path)

img = remove(img)

height , width, channel = img.shape
bg_image = cv2.resize(img_bg, (width, height))
out = np.array(img[:,:,:3], np.uint8)
id = img[:,:,3] == 0
print(id.shape)
out[id, :] = bg_image[id, :]

cv2.imwrite(output_path, out)
# camera = cv2.VideoCapture(0)

# while True :
#     key = cv2.waitKey(100) & 0xFF
#     _, frame = camera.read()
#     # width = 120
#     # height = 120
#     # dim = (width, height)
#     # frame = cv2.resize(frame, dim,  interpolation = cv2.INTER_AREA)
#     img = remove(frame)
#     cv2.imshow("out", img)
#     if key == ord('q') or key == 27:
#         break

# camera.release()
# cv2.destroyAllWindows()
# camera.release()
