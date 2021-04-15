
import cv2
import dlib
import numpy as np

def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

def eye_on_mask(mask, side, shape):
    points = [shape[i] for i in side]
    points = np.array(points, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points, 255)
    return mask

left = [36, 37, 38, 39, 40, 41] # keypoint indices for left eye
right = [42, 43, 44, 45, 46, 47] # keypoint indices for right eye

def nothing(x):
    pass

def contouring(thresh, mid, img, right=False):
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[1]
    try:
        #print(cnts)
        cnt = max(cnts, key = cv2.contourArea) # finding contour with
        #maximum area
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        if right:
            cx += mid # Adding value of mid to x coordinate of centre of
            #right eye to adjust for dividing into two parts
        cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
        #eyeball with red
    except:
        pass #print("cant find pupils")


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_Threshold():
    webcam = cv2.VideoCapture(0)
    
    cv2.namedWindow("Demo",cv2.WINDOW_FREERATIO)
    cv2.setWindowProperty('Demo',cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.namedWindow("Threshold")
    cv2.createTrackbar('threshold', "Threshold", 0, 255, nothing)

    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to grayscale
        
        rects = detector(gray, 1) # rects contains all the faces detected

        thresh = 0
        
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            shape = shape_to_np(shape)

            for (x, y) in [shape[39], shape[42]]:
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)
            
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            mask = eye_on_mask(mask, left, shape)
            mask = eye_on_mask(mask, right, shape)

            kernel = np.ones((9, 9), np.uint8)
            mask = cv2.dilate(mask, kernel, 5)
            eyes = cv2.bitwise_and(frame, frame, mask=mask)
            mask = (eyes == [0, 0, 0]).all(axis=2)
            eyes[mask] = [255, 255, 255]
            eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)

            
            threshold = cv2.getTrackbarPos('threshold', "Threshold")
            _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
            thresh = cv2.erode(thresh, None, iterations=2)
            thresh = cv2.dilate(thresh, None, iterations=4)
            thresh = cv2.medianBlur(thresh, 3)

            thresh = cv2.bitwise_not(thresh)

            mid = (shape[39][0] + shape[42][0]) // 2
            contouring(thresh[:, 0:mid], mid, frame)
            contouring(thresh[:, mid:], mid, frame, True)
            

        cv2.imshow("Demo", frame)
        cv2.imshow("Threshold", thresh)

        if cv2.waitKey(1) == 27:
            Threshold = threshold
            break
        
    cv2.destroyAllWindows() 
    webcam.release()

    return Threshold



