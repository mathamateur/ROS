
from gi import require_version
require_version("Gdk", "3.0")
from gi.repository import Gdk

def get_screen_size(display):
    mon_geoms = [
        display.get_monitor(i).get_geometry()
        for i in range(display.get_n_monitors())
    ]

    x0 = min(r.x            for r in mon_geoms)
    y0 = min(r.y            for r in mon_geoms)
    x1 = max(r.x + r.width  for r in mon_geoms)
    y1 = max(r.y + r.height for r in mon_geoms)

    return x1 - x0, y1 - y0

(s_w, s_h) = get_screen_size(Gdk.Display.get_default())

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cv2.namedWindow("just_a_window")
#cv2.resizeWindow("just_a_window", s_w, s_h)
#cv2.setWindowProperty("just_a_window",cv2.WND_PROP_ASPECT_RATIO,cv2.WINDOW_KEEPRATIO)
#cv2.setWindowProperty("just_a_window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_AUTOSIZE)

def foo(matrix):
    for i in range(60):
        for j in range(30):
            print(matrix[i][j])
region = 0
while cv2.getWindowProperty('just_a_window', cv2.WND_PROP_VISIBLE) == 1:
    
    ret, frame = cap.read()
    '''
    cv2.circle(frame, (100,300), 10, (0,0,267), -1)
    cv2.circle(frame, (100,270), 10, (255,0,0), -1)
    
    x = 85
    w = 30
    y = 255
    h = 60
    region = frame[y:y+h, x:x+w]
    #cv2.GaussianBlur(src = region, ksize = (51, 51), sigmaX = 10, dst = region, sigmaY = 10)
    '''
    xg = 100
    yg = 100
    r = 30
    alfa = 1000
    betha = 600
    for i in range(xg-r,xg+r+1,1):
        for j in range(yg-r,yg+r+1,1):
            er = ((i-xg)**2 + (j-yg)**2)**0.5
            if er == 0:
                er = 0.0001
            if er <= r:
                [b,g,red] = frame[i][j].copy()
                frame[i][j][0] = b
                frame[i][j][1] = alfa*er + g
                frame[i][j][2] = (betha/er)+ red

    cv2.imshow("just_a_window",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#foo(region)
# 'just_a_window', cv2.WND_PROP_VISIBLE cv2.WINDOW_FULLSCREEN cv2.WINDOW_NORMAL
cap.release()
cv2.destroyAllWindows()



