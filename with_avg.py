

from myColibration import getFrameCords

import pygame, sys
import matplotlib.pylab as plt
import numpy as np
import cv2
from gaze_tracking import GazeTracking


s_w = 1910
s_h = 1015

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
#f_dispers = max(S_of_points_f)

print(f_w)
print(f_h)
print(f_c)

pygame.init()
screen = pygame.display.set_mode([s_w,s_h])
screen.fill([255,255,255])

face = pygame.image.load('Face.png')
x = 200
y = 200

flag = False
        
screen.blit(face,[x,y])
#pygame.draw.circle(screen,[255,0,0],[320,240],30,0)
pygame.display.flip()    
running = True

#treck
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
#treck

while running:
    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            flag = not flag

    if flag:
        
        x_f_ar = []
        y_f_ar = []
        g = 0
        
        while g <= 10:
            #pygame.time.delay(20)
            _, frame = webcam.read()
            gaze.refresh(frame)
            frame = gaze.annotated_frame()
            
            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
        
            if right_pupil != None and left_pupil != None:
                
                x_f_ar.append((right_pupil[0] + left_pupil[0]) / 2)
                y_f_ar.append((right_pupil[1] + left_pupil[1]) / 2)
                g += 1
                
        x_f = sum(x_f_ar)/len(x_f_ar)
        y_f = sum(y_f_ar)/len(y_f_ar)
                    
        pygame.draw.rect(screen,[255,255,255],[x,y,90,90],0)
            
        [x,y] = [(s_w-(x_f-f_c[0])*s_w/f_w) , (y_f-f_c[1])*s_h/f_h]
            
        pygame.draw.rect(screen,[255,255,255],[x,y,90,90],0) # забеливаем прошлое место
        screen.blit(face,[x,y])
        pygame.display.flip()
        
pygame.quit()






    
        
