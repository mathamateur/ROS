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
cv2.namedWindow("just_a_window", cv2.WINDOW_FULLSCREEN)
#cv2.setWindowProperty("just_a_window",cv2.WND_PROP_ASPECT_RATIO,cv2.WINDOW_KEEPRATIO)
#cv2.setWindowProperty("just_a_window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_AUTOSIZE)


while cv2.getWindowProperty('just_a_window', cv2.WND_PROP_VISIBLE) == 1:
    
    ret, frame = cap.read()

    cv2.imshow("just_a_window",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 'just_a_window', cv2.WND_PROP_VISIBLE cv2.WINDOW_FULLSCREEN cv2.WINDOW_NORMAL
cap.release()
cv2.destroyAllWindows()



