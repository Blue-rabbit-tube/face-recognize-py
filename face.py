#test
import cv2
import face_recognition
import numpy
import threading
import time

cap=cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,480)

test_image = face_recognition.load_image_file("me.jpg")
   
face_test_locations = face_recognition.face_locations(test_image)
for i in face_test_locations:
    cut_test_face=test_image[(i[0]):(i[2]),(i[3]):(i[1])]

me_encoding = face_recognition.face_encodings(test_image)[0]

def face_test():
    while(1):
        global cut_face
        global me_encoding
        global count
        try:
            # print(cut_face)
            unknown_encoding = face_recognition.face_encodings(cut_face)[0]
            results = face_recognition.compare_faces([me_encoding], unknown_encoding,tolerance=0.5)
            # print(face_recognition.face_encodings(frame))
            print(results)
        except:
            print("No faces")
        cut_face=frame[0:10,0:10]
        
        #查看主线程退出标志位
        if(count==3):
            break
        time.sleep(1)

def start_yes():   
        fs=threading.Thread(target=face_test)
        fs.start()
        
count=0

while(1):
    ret, frame = cap.read()
    #降低图片分辨率   加速找人脸
    frame_resize = cv2.resize(frame, (180, 120), interpolation=cv2.INTER_LINEAR)
    #开始找人脸 返回坐标值
    face_locations = face_recognition.face_locations(frame_resize)
    # print(face_locations)
    #给人脸画上外框  顺便裁剪出来
    for i in face_locations:
        cv2.rectangle(frame,((4*i[1]-50),(4*i[0])),((4*i[3]-50),(4*i[2])),(0,255,0),1)
        # print((4*i[1]-50),(4*i[0]),(4*i[3]-50),(4*i[2]))
        
        #显示字体测试一下
        # cv2.putText(frame, str(4*i[1]-50)+" "+str(4*i[0]), ((4*i[1]-50),(4*i[0])),cv2.FONT_HERSHEY_COMPLEX,1,(0, 255, 0),1)
        # cv2.putText(frame, str(4*i[3]-50)+" "+str(4*i[2]), ((4*i[3]-50),(4*i[2])),cv2.FONT_HERSHEY_COMPLEX,1,(0, 255, 0),1)
        
        #交互提示信息
        cv2.putText(frame, "Finging", ((4*i[1]-50),(4*i[0])),cv2.FONT_HERSHEY_COMPLEX,1,(100, 255, 0),1)
        
        cut_face=frame[(4*i[0]):(4*i[2]),(4*i[3]-50):(4*i[1]-50)]
        # cut_face=frame[0:120,0:100]
        # cv2.imshow("capture1", cut_face) 
        # print(cut_face)
    cv2.imshow("capture", frame)   
    cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    
    if(count==0):
        start_yes()
        count=1
    
    if cv2.waitKey(100) & 0xff == ord('q'):
        count=3
        time.sleep(2)
        break
