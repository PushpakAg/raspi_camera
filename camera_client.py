import cv2
import socket
import pickle
import os
import numpy as np

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)

server_ip = "127.0.0.1"
server_port = 5000

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while cap.isOpened():
    ret, img  = cap.read()
    cv2.putText(img,"HELLO",(0,20),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.imshow("IMG_CLIENT", img)

    ret, buffer = cv2.imencode(".jpg",img, [int(cv2.IMWRITE_JPEG_QUALITY),30])
    x_as_bytes = pickle.dumps(buffer)

    s.sendto((x_as_bytes),(server_ip,server_port))

    if cv2.waitKey(5) & 0xFF == 27:
        break
cv2.destroyAllWindows()
cap.release()