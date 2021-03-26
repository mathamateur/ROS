
from myColibration import getFrameCords

import pygame, sys
import matplotlib.pylab as plt
import numpy as np
import cv2
from gaze_tracking import GazeTracking

#vid.set(cv2.CAP_PROP_FPS, 25)

def countBlink():
    pass

s_w = 1910
s_h = 960

# colibr
points_f = getFrameCords(s_w,s_h) 

X = []
Y = []
for i in range(len(points_f)):
    X.append(points_f[i][0])
    Y.append(points_f[i][1])

plt.scatter(X,Y)
plt.show()


f_w = max(abs(points_f[8][0] - points_f[2][0]),abs(points_f[6][0] - points_f[4][0]))
f_h = max(abs(points_f[8][1] - points_f[6][1]),abs(points_f[3][1] - points_f[4][1]))

f_c = points_f[4]
# colibr

# grid
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

# grid

dim = (s_w,s_h)

def drowLine(cord,orient,size):
    global cv2
    
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

#treck
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
#treck

#kalman
K = 0.1
x_f_k = 0
y_f_k = 0
j = 0
#kalman

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    #frame = imutils.resize(frame, width=1910, height = 1015)

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    
    '''
    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"
    '''

    #cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    #cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    #cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    resized_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    cords = drowLine(vert_lines[0],"vert",s_h)
    cv2.line(resized_frame, cords[0], cords[1], [0,0,255])
    cords = drowLine(vert_lines[1],"vert",s_h)
    cv2.line(resized_frame, cords[0], cords[1], [0,0,255])
    cords = drowLine(hor_lines[0],"hor",s_w)
    cv2.line(resized_frame, cords[0], cords[1], [0,0,255])
    
    if right_pupil != None and left_pupil != None:
            
        x_f = (right_pupil[0] + left_pupil[0]) / 2
        y_f = (right_pupil[1] + left_pupil[1]) / 2

        if j == 0:
            x_f_k = x_f
            y_f_k = y_f
        else:
            x_f_k = x_f * K + x_f_k * (1 - K)
            y_f_k = y_f * K + y_f_k * (1 - K)            
                          
        
        [x,y] = [(s_w-(x_f_k-f_c[0])*s_w/f_w) , (y_f_k-f_c[1])*s_h/f_h]

        if x > s_w:
            x = s_w-10
        if x < 0:
            x = 10
        if y > s_h:
            x = s_h-30
        if y < 0:
            y = 10

        cv2.circle(resized_frame, tuple([round(x),round(y)]), 10, (0,0,255), -1)

        j += 1


    cv2.imshow("Demo", resized_frame)

    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows() 
webcam.release()
