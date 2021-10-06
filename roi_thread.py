import threading
import time
import cv2
import numpy as np
from darknet.yolo_python import net
from collections import deque
from flask import Flask,render_template, Response
roi={}

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cctv')
def cctv():
    return Response(getFrames('cctv'), mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam')
def webcam():
    # return render_template('index.html')
    return Response(getFrames('webcam'), mimetype = 'multipart/x-mixed-replace; boundary=frame')

def getFrames(name):
    global roi

    while True:
        if roi[name] is not None:
            ret, jpeg = cv2.imencode('.jpg', roi[name], [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            
            bframe = jpeg.tobytes()
            if bframe is not None:
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + bframe + b'\r\n\r\n')
        else :
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n\r\n\r\n')
class threadA(threading.Thread):
    def __init__(self, url = None, name = None):
        threading.Thread.__init__(self)
        self.cap = None
        self.name = name
        self.frame = None
        self.frame_count = 0
        self.results = []
        if url is not None:
            self.cap = cv2.VideoCapture(url)
            self.cap.set(3,640)
            self.cap.set(4,480)

    def run(self):
# global disp_frame
        while True:
            ret,frame = self.cap.read()
            frame = cv2.resize(frame, dsize=(640,480), interpolation=cv2.INTER_AREA)
            if ret:
                self.frame = frame
                self.frame_count += 1

                if (self.frame_count%3==0) & (len(th_detect.deque) < 50):
                    th_detect.deque.append([self, frame])

class threadB(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.deque = deque()
        # self.deque2 = deque()
    def run(self):
        while True:
            if len(self.deque) > 0 :
                th_A, frame = self.deque.popleft()
                results = net.detect(frame, 0.5, 0.5)
                th_A.results = results
            time.sleep(0.0001)
                
            # if cv2.waitKey(10) & 0xFF == 27:
            #     cv2.destroyAllWindows()
            #     exit()



class threadC(threading.Thread):
    global roi_start
    global mask
    global draw_list
    global roi
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        
        while True:
            for th_A in thread_list:
                if th_A.frame is not None:
                    frame = th_A.frame.copy()
                    for detection in th_A.results:
                        label = detection[0]
                        confidence = detection[1]
                        x,y,w,h = detection[2]
                        xmin = int(round(x - (w / 2)))
                        xmax = int(round(x + (w / 2)))
                        ymin = int(round(y - (h / 2)))
                        ymax = int(round(y + (h / 2)))

                        labelText = label + ": " + str(np.rint(100 * confidence)) +"%"

                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,0,255), 2)
                        cv2.putText(frame, labelText, (xmin,ymin-12), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,255), 1)
                    print(th_A.name)
                    print(draw_list)   
                    if not th_A.name in draw_list:
                        draw_list[th_A.name] = [] #딕셔너리의 키값(cctv, webcam)에 value값으로 마우스 x,y 좌표를 받기 위한 새로운 리스트 생성
                        roi_start[th_A.name] = False
                    if len(draw_list[th_A.name]) > 0: 
                        # print(draw_list)   
                        # print(draw_list[th_A.name]) # = 클릭시 좌표 value 값
                        cv2.circle(frame, draw_list[th_A.name][-1], 3, (0, 0, 255), -1)
                        
                    if len(draw_list[th_A.name]) > 1:
                        for i in range(len(draw_list[th_A.name]) - 1):
                            cv2.circle(frame, draw_list[th_A.name][i], 5, (0, 0, 255), -1)
                            cv2.line(frame, draw_list[th_A.name][i], draw_list[th_A.name][i + 1], (255, 0, 0), 2)
                    


                    cv2.imshow(th_A.name, frame)
                    cv2.setMouseCallback(th_A.name, draw_roi, th_A)

                    if roi_start[th_A.name]:
                        roi[th_A.name] = cv2.bitwise_and(src1=frame, src2=mask[th_A.name])
                        # print(roi) #mask array
                        # print(roi_start) # cctv : 'True/False' , webcam : 'True/False'
                    else:
                        roi[th_A.name] = frame
                    if cv2.waitKey(10) & 0xFF == 27:
                        cv2.destroyAllWindows()
                        exit()


def draw_roi(event, x, y, flags, param):
    global mask
    global roi_start
    global draw_list

    if event == cv2.EVENT_LBUTTONDOWN:
        draw_list[param.name].append((x,y))
    if event == cv2.EVENT_RBUTTONDOWN:
        draw_list[param.name].pop()
    if event == cv2.EVENT_MBUTTONDOWN:
        roi_start[param.name] = True
        mask[param.name] = np.zeros(param.frame.shape, np.uint8)
        points = np.array(draw_list[param.name], np.int32)
        mask[param.name] = cv2.fillPoly(mask[param.name], [points], (255,255,255))
            
            

if __name__ == '__main__':
    mask = {}
    roi_start = {}
    draw_list = {}
    
    cctv = 'rtsp://admin:4ind331%23@192.168.0.242/profile2/media.smp'
    th_detect = threadB()
    th_detect.start()

    thread_list = []
    thread_list.append(threadA(url=0, name='webcam'))
    thread_list.append(threadA(url=cctv, name='cctv'))
    for thr in thread_list:
        thr.start()

    th_view = threadC()
    th_view.start()

    app.run(host='127.0.0.1', debug = False, port=5000)