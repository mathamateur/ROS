
import cv2
from gaze_tracking import GazeTracking
import numpy as np
import matplotlib.pyplot as plt

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)    

    
    if cv2.waitKey(1) == 27:

        frame_vis_Lpup = gaze.eye_left.pupil.iris_frame
        
        Y = []
        n = frame_vis_Lpup.shape[0]
        for i in range(n):
            Y.append(sum(frame_vis_Lpup[i]))

        X = []
        m = frame_vis_Lpup.shape[1]
        for i in range(m):
            X.append(sum(frame_vis_Lpup.T[i]))
        
        fig, axs = plt.subplots(4,1)
        axs[0].imshow(gaze.eye_left.frame)
        axs[1].imshow(gaze.eye_left.pupil.iris_frame)
        axs[2].plot(Y,range(n))
        axs[3].plot(range(m),X)
        print((np.argmin(Y),np.min(Y)))
        print((np.argmin(X),np.min(X)))
        plt.show()
        
        break
    
cv2.destroyAllWindows() 
webcam.release() 
