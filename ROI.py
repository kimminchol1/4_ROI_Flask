import cv2
import imutils
import numpy as np

pts = [] 
mask = None
roi_start = False

def draw_roi(event, x, y, flags, param):
    # frame2 = frame.copy()
    global mask
    global roi_start
    
    if event == cv2.EVENT_LBUTTONDOWN:  
        pts.append((x, y))  

    if event == cv2.EVENT_RBUTTONDOWN:  
        pts.pop()  

    if event == cv2.EVENT_MBUTTONDOWN:
        if len(pts) > 1 :  
            mask = np.zeros(param.shape, np.uint8)
            points = np.array(pts, np.int32)
            mask = cv2.fillPoly(mask, [points], (255, 255, 255))
            
            # cv2.imshow('frame',frame2)
            # cv2.imshow('ROI', ROI)
            roi_start = 1
        
            
cap = cv2.VideoCapture("rtsp://admin:4ind331%23@192.168.0.242/profile2/media.smp")

while True:
    
    ret, frame = cap.read()
    frame = cv2.resize(frame, dsize=(640,480), interpolation=cv2.INTER_AREA)
    if ret:
        
        # cv2.namedWindow('frame')
        
        if len(pts) > 0:
        
            cv2.circle(frame, pts[-1], 3, (0, 0, 255), -1)

        if len(pts) > 1:
            
            for i in range(len(pts) - 1):
                cv2.circle(frame, pts[i], 5, (0, 0, 255), -1)  
                cv2.line(img=frame, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)

        if roi_start:
            ROI = cv2.bitwise_and(mask, frame)
            cv2.imshow('ROI',ROI)
        cv2.imshow('frame', frame)
        cv2.setMouseCallback('frame', draw_roi,frame)
        if cv2.waitKey(10) & 0xFF == 27:
            break



