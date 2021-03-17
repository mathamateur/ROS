
#perturbator i am the night
from myColibration import getFrameCords

import pygame, sys
import matplotlib.pylab as plt
import numpy as np
import cv2
from gaze_tracking import GazeTracking

def callEvent(i,j):
    if i == 1 and j == 1:
        print("1__1")
    if i == 2 and j == 1:
        print("2__1")
    if i == 3 and j == 1:
        print("3__1")
    if i == 1 and j == 2:
        print("1__2")
    if i == 2 and j == 2:
        print("2__2")
    if i == 3 and j == 2:
        print("3__2")

def colorScreen(i,j):
    pygame.draw.rect(screen,[255,255,255],[x,y,90,90],0)
    pygame.display.flip()  
    

s_w = 1910
s_h = 1015

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

w_grid = []
h_grid = []
n = 3
m = 2
grid_w = round(s_w/n)
grid_h = round(s_h/m)

for i in range(n):
    w_grid.append(i*grid_w)
for i in range(m):
    h_grid.append(i*grid_h)

#pygame
pygame.init()
screen = pygame.display.set_mode([s_w,s_h])
screen.fill([255,255,255])

face = pygame.image.load('Face.png')
x = 200
y = 200

flag = False
        
screen.blit(face,[x,y])

pygame.display.flip()    
running = True
#pygame

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

            if j == 0:
                x_f_k = x_f
                y_f_k = y_f
            else:
                x_f_k = x_f * K + x_f_k * (1 - K)
                y_f_k = y_f * K + y_f_k * (1 - K)            
                          
            pygame.draw.rect(screen,[255,255,255],[x,y,90,90],0)# забеливаем прошлое место

            #[x,y] = [(s_w-(x_f-f_c[0])*s_w/f_w) , (y_f-f_c[1])*s_h/f_h]

            #with kalman
            [x,y] = [(s_w-(x_f_k-f_c[0])*s_w/f_w) , (y_f_k-f_c[1])*s_h/f_h] 

            for i in range(n):
                if x < w_grid[i]:
                    w_grid_ind = i+1
                    break
            for i in range(m):
                if y < h_grid[i]:
                    h_grid_ind = i+1
                    break

            callEvent(w_grid_ind,h_grid_ind)
  
            screen.blit(face,[x,y])
            pygame.display.flip()

            j += 1

cv2.destroyAllWindows() 
webcam.release()            
pygame.quit()
