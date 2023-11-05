from flask import Flask, render_template, Response
import cv2
import socket
import pickle
import numpy as np

app = Flask(__name__)

# Create a TCP socket to receive the video stream.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 5000))
s.listen(1)

# Define a function to generate the video stream.
def generate_video_stream():
    conn, addr = s.accept()

    while True:
        # Receive a frame from the client.
        data = conn.recv(1000000)

        if not data:
            break

        # Decode the frame.
        frame = pickle.loads(data)

        # Convert the frame to a NumPy array.
        frame = np.asarray(frame)

        # Encode the frame as a JPEG image.
        ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

        # Yield the JPEG image to the client.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'
               + buffer + b'\r\n')

# Define a route to show the video stream.
@app.route("/video")
def video():
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Start the Flask server.
if __name__ == "__main__":
    app.run(debug=True)
