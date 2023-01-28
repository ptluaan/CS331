from mediapipe.python import solutions
from background_replacement import *
import os

solution = 0

mediapipe_visible = False
contours_visible  = False
subtract_visible  = False
mask_visible      = False

flag_flip = False

background_path = 'images'
backgrounds = os.listdir(background_path)

background_index = 0
background = cv2.imread(background_path+'/'+backgrounds[background_index])

# camera
camera = cv2.VideoCapture(0)
_,frame_model = camera.read()

def nothing(x):
    pass

# create solutions
_mediapipe = background_replacement_mediapipe()
_contours  = background_replacement_contours()

# setting panel
cv2.namedWindow('Panel')

# Pannel for background_replacement_mediapipe
def panel_mediapipe():
    cv2.destroyWindow('Panel')
    cv2.namedWindow('Panel')

    cv2.createTrackbar('Threshold','Panel',60,100,nothing)
    cv2.createTrackbar('Portrait' ,'Panel',0,50 ,nothing)

# Pannel for background_replacement_contours
def panel_contours():
    cv2.destroyWindow('Panel')
    cv2.namedWindow('Panel',cv2.WINDOW_NORMAL)

    cv2.createTrackbar('Portrait'   ,'Panel',0,50  ,nothing)
    cv2.createTrackbar('Blur'       ,'Panel',10,25  ,nothing)
    cv2.createTrackbar('Min area'   ,'Panel',50,700 ,nothing)
    cv2.createTrackbar('Max area'   ,'Panel',950,1000,nothing)
    cv2.createTrackbar('Canny low'  ,'Panel',15,250 ,nothing)
    cv2.createTrackbar('Canny high' ,'Panel',150,250 ,nothing)
    cv2.createTrackbar('Dilate iter','Panel',10,15  ,nothing)
    cv2.createTrackbar('Erode iter' ,'Panel',10,15  ,nothing)

# Pannel for background_replacement_subtract
def panel_subtract():
    cv2.destroyWindow('Panel')
    cv2.namedWindow('Panel')

    cv2.createTrackbar('Threshold chanel','Panel',0,255,nothing)
    cv2.createTrackbar('Threshold gray'  ,'Panel',0,255,nothing)
    cv2.createTrackbar('Blur'            ,'Panel',0,50 ,nothing)
    cv2.createTrackbar('Portrait'        ,'Panel',0,50 ,nothing)

def mediapipe_handle(frame, background) :
    global mediapipe_visible, contours_visible, subtract_visible, flag_flip

    if not mediapipe_visible : panel_mediapipe()

    mediapipe_visible = True
    contours_visible  = False
    subtract_visible  = False

    threshold = cv2.getTrackbarPos('Threshold','Panel') / 100.0
    portrait  = cv2.getTrackbarPos('Portrait' ,'Panel') * 2 + 1

    _mediapipe.set_parameters(threshold)

    if portrait > 1:
        background = cv2.GaussianBlur(frame, (portrait,portrait),0)

    return _mediapipe.solution(frame, background)

def contours_handle(frame, background) :
    global mediapipe_visible, contours_visible, subtract_visible, flag_flip

    if not contours_visible : panel_contours()

    contours_visible  = True
    mediapipe_visible = False
    subtract_visible  = False

    blur        = cv2.getTrackbarPos('Blur'       ,'Panel') * 2 + 1
    canny_low   = cv2.getTrackbarPos('Canny low'  ,'Panel')
    canny_high  = cv2.getTrackbarPos('Canny high' ,'Panel')
    min_area    = cv2.getTrackbarPos('Min area'   ,'Panel') / 1000.0
    max_area    = cv2.getTrackbarPos('Max area'   ,'Panel') / 1000.0
    dilate_iter = cv2.getTrackbarPos('Dilate iter','Panel')
    erode_iter  = cv2.getTrackbarPos('Erode iter' ,'Panel')
    portrait    = cv2.getTrackbarPos('Portrait'   ,'Panel') * 2 + 1

    _contours.set_parameters(blur,canny_low,canny_high,min_area, max_area, dilate_iter, erode_iter)
   
    if portrait > 1:
        background = cv2.GaussianBlur(frame, (portrait,portrait),0)

    return _contours.solution(frame, background)

def save_output():
    out_path = 'Output'
    out = os.listdir(out_path)
    name_out = str(len(out)) 
    cv2.imwrite(out_path +"/" + name_out + ".jpg",output)

while True:
    key = cv2.waitKey(1) & 0xFF
    
    _, frame = camera.read()

    if  key == ord('f') :
        flag_flip ^= True
    
    if (flag_flip) :
        frame = cv2.flip(frame,1)

    if   key == ord('q') or key == 27:
        break
    
    elif key == ord('d'):
        background_index = (background_index + 1) % len(backgrounds)
        background = cv2.imread(background_path+'/'+backgrounds[background_index])
    
    elif ord('p') == key:
        frame_model = frame

    elif key == ord('1'):
        solution = 0
    elif key == ord('2'):
        solution = 1

    if   0 == solution :
        mask, output = mediapipe_handle(frame, background)
    elif 1 == solution :
        mask, output = contours_handle(frame, background)
    
    if key == ord('m'):
        if mask_visible :
            cv2.destroyWindow('mask')
        mask_visible ^= True

    if mask_visible :
        cv2.imshow('mask',mask)
   
    cv2.imshow("Output", output)

    if ord('s') == key:
        save_output()

cv2.destroyAllWindows()
camera.release()