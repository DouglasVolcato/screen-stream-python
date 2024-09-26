from flask import Flask, render_template, Response
import mss
import cv2
import numpy as np
from flask import request, jsonify

app = Flask(__name__)

SECRET_TOKEN = '45g245g245g'

import time

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            start_time = time.time()
            img = sct.grab(monitor)
            img_np = np.array(img)
            success, frame = cv2.imencode('.jpg', img_np, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not success:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
            
            # Control the frame rate
            elapsed_time = time.time() - start_time
            time.sleep(max(0, (1/60) - elapsed_time))



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    if SECRET_TOKEN not in str(request.query_string):
        return jsonify({"error": "Unauthorized"}), 403
    return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
