import cv2
import socket
import pickle
import numpy as np
from flask import Flask, Response

app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "192.168.131.101"
port = 2222
s.bind((ip, port))


while True:
    x = s.recvfrom(1000000)
    data = x[0]
    data = pickle.loads(data)
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow("IMG_SERVER",frame)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break
cv2.destroyAllWindows()


