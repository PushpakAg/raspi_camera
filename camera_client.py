import cv2
import socket
import pickle
import os
import numpy as np

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)

server_ip = "192.168.1.5"
server_port1 = 6666
server_port2 = 6668
cap = cv2.VideoCapture(1)
cap1 = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap1.set(3,640)
cap1.set(4,480)

while cap.isOpened():
    ret, img  = cap.read()
    ret1, img1 = cap1.read()
    cv2.putText(img,"HELLO",(0,20),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.imshow("IMG_CLIENT", img)
    cv2.imshow("IMG_CLIENT_1",img1)

    ret, buffer = cv2.imencode(".jpg",img, [int(cv2.IMWRITE_JPEG_QUALITY),30])
    ret1, buffer1 = cv2.imencode(".jpg",img1, [int(cv2.IMWRITE_JPEG_QUALITY),30])
    x_as_bytes = pickle.dumps(buffer)
    x_as_bytes1 = pickle.dumps(buffer1)

    s.sendto((x_as_bytes),(server_ip,server_port1))
    s.sendto((x_as_bytes1),(server_ip,server_port2))

    if cv2.waitKey(5) & 0xFF == 27:
        break
cv2.destroyAllWindows()
cap.release()