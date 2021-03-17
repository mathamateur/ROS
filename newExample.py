

#perturbator i am the night
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

#====create grid
w = 25
h = 25
m = int(s_w/w)
n = int(s_h/h)
x_grid = []
y_grid = []

for i in range(1,m+1):
    x_grid.append(i*w)
    
for i in range(1,n+1):
    y_grid.append(i*h)
    
#====create grid

    
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

        _, frame = webcam.read()
        gaze.refresh(frame)
        frame = gaze.annotated_frame()
                
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()

        if right_pupil != None and left_pupil != None:
            
            x_f = (right_pupil[0] + left_pupil[0]) / 2
            y_f = (right_pupil[1] + left_pupil[1]) / 2
                      
            pygame.draw.rect(screen,[255,255,255],[x,y,90,90],0)
                
            [x,y] = [(s_w-(x_f-f_c[0])*s_w/f_w) , (y_f-f_c[1])*s_h/f_h]

            for i in range(m):
                if x <= x_grid[i]:
                    x = x_grid[i] - w/2
                    break
                
            for i in range(n):
                if y <= y_grid[i]:
                    y = y_grid[i] - h/2
                    break
                
            pygame.draw.rect(screen,[255,255,255],[x,y,90,90],0) # забеливаем прошлое место
            screen.blit(face,[x,y])
            pygame.display.flip()

cv2.destroyAllWindows() 
webcam.release()            
pygame.quit()


