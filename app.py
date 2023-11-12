import cv2
import socket
import pickle
import numpy as np
from flask import Flask, Response

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "192.168.1.5"
port1 = 6666
port2 = 6668
s1.bind((ip, port1))
s2.bind((ip, port2))

while True:
    x1 = s1.recvfrom(1000000)
    x2 = s2.recvfrom(1000001)
    data1 = x1[0]
    data2 = x2[0]
    data1 = pickle.loads(data1)
    data2 = pickle.loads(data2)
    frame1 = cv2.imdecode(data1, cv2.IMREAD_COLOR)
    frame2 = cv2.imdecode(data2, cv2.IMREAD_COLOR)

    # Resize frames to have the same height (assuming both frames have the same width)
    min_height = min(frame1.shape[0], frame2.shape[0])
    frame1 = cv2.resize(frame1, (int(frame1.shape[1] * min_height / frame1.shape[0]), min_height))
    frame2 = cv2.resize(frame2, (int(frame2.shape[1] * min_height / frame2.shape[0]), min_height))

    # Concatenate frames horizontally
    concatenated_frame = np.concatenate((frame1, frame2), axis=1)

    cv2.imshow("Concatenated Frames", concatenated_frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cv2.destroyAllWindows()
