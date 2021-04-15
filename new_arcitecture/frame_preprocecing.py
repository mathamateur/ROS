

def drowLine(cord,orient,size):
    
    if orient == "vert":
        x1 = cord
        x2 = cord
        y1 = 0
        y2 = size
    elif orient == "hor":
        x1 = 0
        x2 = size
        y1 = cord
        y2 = cord
    else:
        print("not hor not vert")
        return 0
    
    return [(x1,y1),(x2,y2)]

# grid
def getGrid(s_w,s_h):
    vert_lines = []#[200,400]
    hor_lines = []#[250]

    n = 3
    m = 2
    grid_w = round(s_w/n)
    grid_h = round(s_h/m)

    for i in range(1,n):
        vert_lines.append(i*grid_w)
    for i in range(1,m):
        hor_lines.append(i*grid_h)

    return (vert_lines, hor_lines)

# grid

#from diferent_from_medium_trecker import get_Threshold

#threshold = get_Threshold()

import cv2
import dlib
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

left = [36, 37, 38, 39, 40, 41] # keypoint indices for left eye
right = [42, 43, 44, 45, 46, 47] # keypoint indices for right eye

kernel = np.ones((9, 9), np.uint8)

def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

def eye_on_mask(mask, side, shape):
    points = [shape[i] for i in side]
    points = np.array(points, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points, 255)
    return mask

def contouring(thresh, mid, prev_val, right=False):
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[1]
    try:
        cnt = max(cnts, key = cv2.contourArea) # finding contour with
        #maximum area
        M = cv2.moments(cnt)
        pupil_x = int(M['m10']/M['m00'])
        pupil_y = int(M['m01']/M['m00'])
        if right:
            pupil_x += mid # Adding value of mid to x coordinate of centre of
            #right eye to adjust for dividing into two parts
        return (pupil_x, pupil_y)
    
    except:
        return prev_val

def get_eye_AND_pupil_cords(frame, threshold, prev_val_pupil):
    (left_eye_x, left_eye_y, right_eye_x, right_eye_y, left_pupil_x, left_pupil_y, right_pupil_x, right_pupil_y) = (0,0,0,0,0,0,0,0)
    global left, right, kernel
    # We get a new frame from the webcam

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to grayscale
    
    rects = detector(gray, 1) # rects contains all the faces detected

    for (i, rect) in enumerate(rects):
    
        shape = predictor(gray, rect)
        shape = shape_to_np(shape)

        (left_eye_x, left_eye_y) = shape[39]
        (right_eye_x, right_eye_y) = shape[42]

        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        mask = eye_on_mask(mask, left, shape)
        mask = eye_on_mask(mask, right, shape)

        mask = cv2.dilate(mask, kernel, 5)
        eyes = cv2.bitwise_and(frame, frame, mask=mask)
        mask = (eyes == [0, 0, 0]).all(axis=2)
        eyes[mask] = [255, 255, 255]
        eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)
        thresh = cv2.medianBlur(thresh, 3)

        thresh = cv2.bitwise_not(thresh)

        cv2.imshow("foo",thresh)

        mid = (shape[39][0] + shape[42][0]) // 2

        (left_pupil_x, left_pupil_y) = contouring(thresh[:, 0:mid], mid, prev_val_pupil[0])
        (right_pupil_x, right_pupil_y) = contouring(thresh[:, mid:], mid, prev_val_pupil[1], right = True)

            
    return (left_eye_x, left_eye_y, right_eye_x, right_eye_y, left_pupil_x, left_pupil_y, right_pupil_x, right_pupil_y)


def getGaze(x_f_k_p, y_f_k_p, s_w, s_h, j,left_eye_x, left_eye_y, right_eye_x, right_eye_y, left_pupil_x, left_pupil_y, right_pupil_x, right_pupil_y):

    K = 0.2
    f_w = 12
    f_h = 8
    
    left_pupil_on_eye_x = left_pupil_x - left_eye_x
    left_pupil_on_eye_y = left_pupil_y - left_eye_y

    f_c = [(left_eye_x + right_eye_x)/2, (left_eye_y + right_eye_y)/2]
    
    x_f = (left_pupil_x + right_pupil_x) / 2
    y_f = (left_pupil_y + right_pupil_y) / 2

    #x_f_k = x_f * K + x_f_k_p * (1 - K)
    #y_f_k = y_f * K + y_f_k_p * (1 - K)            
                          
        
    #[x,y] = [(s_w-(x_f_k-f_c[0])*s_w/f_w) , (y_f_k-f_c[1])*s_h/f_h]
    [x,y] = [(s_w-(x_f-f_c[0])*s_w/f_w) , (y_f-f_c[1])*s_h/f_h]

    if x > s_w:
        x = s_w-10
    if x < 0:
        x = 10
    if y > s_h:
        y = s_h-10
    if y < 0:
        y = 10
    
    return (int(x),int(y))

def get_Centr(): # returns 
    pass
















