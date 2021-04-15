
import cv2
from gaze_tracking import GazeTracking
import numpy as np
import matplotlib.pyplot as plt

def count():
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    k = 0
    
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()

        if gaze.is_blinking():
            print("Blinking")
            k += 1

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Blinking counting", (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Blinking counting", frame)    

        
        if cv2.waitKey(1) == 27:
            break
        
    cv2.destroyAllWindows() 
    webcam.release()
    return round(k/3)

print(count())
