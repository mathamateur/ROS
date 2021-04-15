
import pygame, sys
from gaze_tracking import GazeTracking
import cv2
import numpy as np

def text_objects(text, font):
    textSurface = font.render(text, True, (0,255,0))
    return textSurface, textSurface.get_rect()


def getFrameCords(s_w,s_h):
    pygame.init()
    screen = pygame.display.set_mode([s_w,s_h])
    screen.fill([255,255,255])
    '''
    x = 200
    y = 200
    pygame.draw.circle(screen,[255,0,0],[x,y],15,0)
    pygame.display.flip()
    '''
    running = True
    k = 0
    points_s = [[s_w/2,s_h/2],[s_w/2,0],[s_w,0],[s_w,s_h/2],[s_w,s_h],[s_w/2,s_h],[0,s_h],[0,s_h/2],[0,0]]
    points_f = []
    S_of_point_f = []

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    flag = False

    while running:
        if cv2.waitKey(1) == 27:
            break
        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                flag = not flag
         
        if flag:
            
            p = points_s[k]
            pygame.draw.circle(screen,[255,0,0],p,15,0)
            

            #==================
            largeText = pygame.font.Font('freesansbold.ttf',40)
            TextSurf, TextRect = text_objects("Посмотрите на точку и нажмите на кнопку.", largeText)
            TextRect.center = ((s_w/2),(s_h/2-60))
            screen.blit(TextSurf, TextRect)
            #==================
            
            pygame.display.flip()
            
            #print("Посмотрите на точку и нажмите на кнопку.")
            i = 0
            x_f = []
            y_f = []
            flag1 = False
            while i < 20:
                pygame.time.delay(20)
                
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        flag1 = True

                _, frame = webcam.read()
                gaze.refresh(frame)
                frame = gaze.annotated_frame()

                left_pupil = gaze.pupil_left_coords()
                right_pupil = gaze.pupil_right_coords()
                                
                if flag1 and right_pupil != None and left_pupil != None:
                    x_f.append((right_pupil[0] + left_pupil[0]) / 2)
                    y_f.append((right_pupil[1] + left_pupil[1]) / 2)
                    
                    i += 1
            
            points_f.append([sum(x_f)/len(x_f),sum(y_f)/len(y_f)])
            S_of_point_f.append(((np.std(np.array(x_f).reshape((len(x_f),1))))**2 + (np.std(np.array(y_f).reshape((len(y_f),1))))**2)**0.5)
            pygame.draw.circle(screen,[255,255,255],p,15,0)
            pygame.display.flip() 
            

            k += 1
        if k >= len(points_s):
            break
            
    
    cv2.destroyAllWindows() 
    webcam.release()
    pygame.quit()

    return points_f
