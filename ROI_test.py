from re import X
import threading
import cv2
import numpy as np
from collections import deque

#####클래스로 만들어보기(영상 ROI)#####
draw_list = []
class video_thread(threading.Thread):
    def __init__(self,url=None, thread=None):
        threading.Thread.__init__(self)

        global draw_list
        self.V_thread = thread
        self.url = None
        self.frame = None
        self.frame_count = 0
        if url is not None:
            self.cap = cv2.VideoCapture(url)
            self.cap.set(3,640)
            self.cap.set(4,480)

       
    
    def run(self):
         while True:
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, dsize=(640,480), interpolation=cv2.INTER_AREA)
            if ret:

                self.frame = frame
                self.frame_count += 1
                



class ROI_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        global mask
        global draw_list
        global frame2
        
        cv2.imshow('frame2',draw_roi.frame2)
        cv2.setMouseCallback('frame2', draw_roi)
        if cv2.waitKey(10) & 0xff == 27:
            cv2.destroyAllWindows()
            exit()

        
        
def draw_roi(self,event, x, y, flags, params):
    pass


class VIEW_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass
        
            


if __name__ == '__main__':
    cctv='rtsp://admin:4ind331%23@192.168.0.242/profile2/media.smp'
    
    
    thread_list = []
    thread_list.append(video_thread(url=1, name='webcam'))
    thread_list.append(video_thread(url=cctv, name='cctv'))
    for thr in thread_list:
        thr.start()
    C_thread = VIEW_thread()
    C_thread.start()

    B_thread = ROI_thread()
    B_thread.start()
    

    
