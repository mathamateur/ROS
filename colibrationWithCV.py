
from gaze_tracking import GazeTracking
import cv2
import numpy as np
import time

import matplotlib.pylab as plt

watchsOnPoint = False

def click(event, x, y, flags, param):
    global watchsOnPoint
    if event == cv2.EVENT_LBUTTONDOWN:
        watchsOnPoint = True

def getInhabitationOfPupilsWhenLookingOnScreen(s_w,s_h):
    # получаю границы области на фотографии
    # в которой могут находиться зрачки объекта, 
    # когда он смотрит куда-то на экран
    # аргументы это размеры экрана
    # предполагаю что эта область прямоугольная
    # возвращает центр этой облости (координаты зрачков на фото во время того
    # как они смотрят в центр экрана) и, аналогично края.

    global watchsOnPoint
    
    webcam = cv2.VideoCapture(0)
    cv2.namedWindow("Colibration") # cv2.WINDOW_KEEPRATIO
    #cv2.resizeWindow("Colibration", s_w, s_h)
    cv2.setMouseCallback("Colibration", click)

    gaze = GazeTracking() # object that is used for gaze traking

    '''
    # points on screen where the object should look
    points_s = [[s_w/2, s_h/2],  # center
                [s_w/2, 15],     # top
                [s_w-15, s_h/2], # right boundary
                [s_w/2, s_h-15], # bottom
                [15, s_h/2]]     # left boundary
    '''
    
    points_f = [] # cords of domain that we are looking for

    text = "Посмотрите на точку и нажмите на экран для начала определения взгляда."
    
    k = 0 # counter of points
    i = 0 # counter of values to enumerait the coordinat of pupils when looking on concret point

    x_Pup = [] # x of pupils when looking on points_s[k]
    y_Pup = []

    x_face = [] # coordinats of point between eyes # not using now. use x_face_look_center
    y_face = []

    x_face_look_center = []
    y_face_look_center = []
    
    while cv2.getWindowProperty("Colibration", cv2.WND_PROP_VISIBLE) == 1 and k < 5:
        #print(cv2.getWindowProperty("Colibration", cv2.WND_PROP_VISIBLE))
        if cv2.waitKey(1) == 27:
            break

        _, frame = webcam.read()
        
        w = frame.shape[1]
        h = frame.shape[0]

        gaze.refresh(frame)
        frame = gaze.annotated_frame()
        
        # points on screen where the object should look
        points_s = [[w/2, h/2],  # center
                    [w/2, 10],     # top
                    [w-10, h/2], # right boundary
                    [w/2, h-10], # bottom
                    [10, h/2]]     # left boundary
                
        p = points_s[k] # corent point

        cv2.putText(frame, text, (20, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
        cv2.circle(frame, (round(p[0]),round(p[1])), 10, (0,0,255), -1)

        resized_frame = cv2.resize(frame, (s_w,s_h), interpolation = cv2.INTER_AREA)
        cv2.imshow("Colibration", resized_frame)
                
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        left_eye = gaze.eye_left
        right_eye = gaze.eye_right
            
        if watchsOnPoint:
            
            text = ""
            
            if i < 20:

                if right_pupil != None and left_pupil != None and left_eye != None and right_eye != None:

                    x_Pup.append((right_pupil[0] + left_pupil[0]) / 2)
                    y_Pup.append((right_pupil[1] + left_pupil[1]) / 2)                    
                    
                    x_face.append((left_eye.cods[0] + right_eye.cods[0])/2)
                    y_face.append((left_eye.cods[1] + right_eye.cods[1])/2)
                    
                    if k == 0:
                        x_face_look_center.append((left_eye.cods[0] + right_eye.cods[0])/2)
                        y_face_look_center.append((left_eye.cods[1] + right_eye.cods[1])/2)
                    
                    i += 1
                    time.sleep(0.02)

            if i == 20:
                points_f.append([sum(x_Pup)/len(x_Pup),sum(y_Pup)/len(y_Pup)])
                x_Pup = []
                y_Pup = []
                
                text = "Посмотрите на точку, нажмите на экран для начала определения взгляда."
                
                k += 1
                i = 0
                watchsOnPoint = False

    if len(x_face) == 0 or len(y_face) == 0:
        #eye_cords_when_looking_on_screen = [0,0]
        eye_cords_when_looking_on_center = [0,0]
    else:
        # avg coordinats of point between eyes
        #eye_cords_when_looking_on_screen = [sum(x_face)/len(x_face),sum(y_face)/len(y_face)]

        eye_cords_when_looking_on_center = [sum(x_face_look_center)/len(x_face_look_center),sum(y_face_look_center)/len(y_face_look_center)]

            
    cv2.destroyAllWindows() 
    webcam.release()

    #points_f.append(eye_cords_when_looking_on_screen)
    points_f.append(eye_cords_when_looking_on_center)

    return points_f
'''
s_w = 1910
s_h = 960

points_f = getInhabitationOfPupilsWhenLookingOnScreen(s_w,s_h)

cx = points_f[len(points_f)-2][0]
cy = points_f[len(points_f)-2][1]

#c1x = points_f[len(points_f)-1][0]
#c1y = points_f[len(points_f)-1][1]

X = []
Y = []
for i in range(len(points_f)-1):
    X.append(points_f[i][0])
    Y.append(points_f[i][1])

plt.scatter(X,Y,c="g")
plt.scatter(cx,cy,c="r")
#plt.scatter(c1x,c1y,c="b")
plt.show()
'''
