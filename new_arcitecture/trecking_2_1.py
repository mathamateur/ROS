
# cv2.getWindowProperty('Trecking Window', cv2.WND_PROP_VISIBLE) когда нажат крстик возвращает ноль, иначе один

import cv2
import dlib

from Threshold_colibration import get_Threshold

threshold = get_Threshold()

# colibr
'''
from myColibration import getFrameCords
import matplotlib.pylab as plt

# for geting s_w s_h
webcam = cv2.VideoCapture(0)
cv2.namedWindow('Trecking Window',cv2.WINDOW_FREERATIO)
cv2.setWindowProperty('Trecking Window',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

_, frame = webcam.read()

(s_h, s_w, _) = frame.shape # !!!

cv2.destroyAllWindows() 
webcam.release()
frame = 0
webcam = 0
# for geting s_w s_h

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
'''
# colibr

from frame_preprocecing import drowLine, getGrid, get_eye_AND_pupil_cords, getGaze

webcam = cv2.VideoCapture(0)
cv2.namedWindow('Trecking Window',cv2.WINDOW_FREERATIO)
cv2.setWindowProperty('Trecking Window',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

_, frame = webcam.read()
(s_h, s_w, _) = frame.shape
(vert_lines, hor_lines) = getGrid(s_w, s_h)
                                  
line_cords1 = drowLine(vert_lines[0],"vert",s_h)
line_cords2 = drowLine(vert_lines[1],"vert",s_h)
line_cords3 = drowLine(hor_lines[0],"hor",s_w)

prev_val_pupil = ((0,0),(0,0))
x_f_k_p = 0
y_f_k_p = 0

j = 0

while True:
    
    _, frame = webcam.read() 

    (left_eye_x, left_eye_y, right_eye_x, right_eye_y, left_pupil_x, left_pupil_y, right_pupil_x, right_pupil_y) = get_eye_AND_pupil_cords(frame, threshold, prev_val_pupil)
    (gaze_x, gaze_y) = getGaze(x_f_k_p, y_f_k_p, s_w, s_h, j, left_eye_x, left_eye_y, right_eye_x, right_eye_y, left_pupil_x, left_pupil_y, right_pupil_x, right_pupil_y)

    cv2.line(frame, line_cords1[0], line_cords1[1], [0,0,0])
    cv2.line(frame, line_cords2[0], line_cords2[1], [0,0,0])
    cv2.line(frame, line_cords3[0], line_cords3[1], [0,0,0])
    
    cv2.circle(frame, (left_eye_x, left_eye_y), 2, (255, 0, 0), -1)
    cv2.circle(frame, (right_eye_x, right_eye_y), 2, (255, 0, 0), -1)
    
    cv2.circle(frame, (left_pupil_x, left_pupil_y), 4, (0, 0, 255), 2)
    cv2.circle(frame, (right_pupil_x, right_pupil_y), 4, (0, 0, 255), 2)
    
    cv2.circle(frame, (gaze_x, gaze_y), 10, (0,0,255), -1)

    cv2.imshow('Trecking Window', frame)

    prev_val_pupil = ((left_pupil_x, left_pupil_y), (right_pupil_x, right_pupil_y))
    (x_f_k_p, y_f_k_p) = (gaze_x, gaze_y)
    
    j += 1
    
    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows() 
webcam.release()
