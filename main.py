import cv2
import mediapipe as mp
import time
import cvzone
import numpy as np
from flask import Flask, render_template, Response
app = Flask(__name__)

camera = cv2.VideoCapture(0)
# hand tracking start
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
# images for overlay & size
logo = cv2.imread("static/images/Group 3.png")
height = 150
width = 1270
logo = cv2.resize(logo, (width, height))
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)


def hand_tracking(camera_frame):
    image_rgb = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    # adds number to fi
    fontScale = int (1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                        h, w, c = camera_frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        print(id, cx, cy)

                        if id == 4:
                            cv2.circle(camera_frame, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
                            cv2.putText(camera_frame, "T", (cx - 8, cy+10), font, fontScale, (255, 255, 255), 2, cv2.LINE_AA )

                        if id == 8:
                            cv2.circle(camera_frame, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
                            cv2.putText(camera_frame, "1", (cx - 8, cy + 10), font, fontScale, (255, 255, 255), 2, cv2.LINE_AA)

                        if id == 12:
                            cv2.circle(camera_frame, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
                            cv2.putText(camera_frame, "2", (cx - 8, cy+10), font, fontScale, (255, 255, 255), 2, cv2.LINE_AA)

                        if id == 16:
                            cv2.circle(camera_frame, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
                            cv2.putText(camera_frame, "3", (cx - 8, cy+10), font, fontScale, (255, 255, 255), 2, cv2.LINE_AA)

                        if id == 20:
                            cv2.circle(camera_frame, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
                            cv2.putText(camera_frame, "4", (cx - 8, cy+10), font, fontScale, (255, 255, 255), 2, cv2.LINE_AA)

                mpDraw.draw_landmarks(camera_frame, handLms, mpHands.HAND_CONNECTIONS)


def fret_overlay(frame):
    # Region of Image (ROI), where we want to insert logo
    roi = frame[-height - 10:-10, -width - 10:-10]
    roi[np.where(mask)] = 0
    roi += logo
    cv2.imshow("WebCam", frame)
    # dot
    radius = 150
    paint_h = int(height / 2)  # will be painted in the middle

    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./circle_noise.avi', fourcc, float(FPS), (width, height))

    for paint_x in range(-radius, width+radius, 6):
        frame = np.random.randint(0, 256,
                                  (height, width, 3),
                                  dtype=np.uint8)
        cv2.circle(frame, (paint_x, paint_h), radius, (0, 0, 0), -1)
        video.write(frame)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            hand_tracking(frame)
            fret_overlay(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play_page')
def play_page():
    return render_template('play_page.html')


@app.route('/camera_feed')
def camera_feed():
    return render_template('camera_feed.html')


@app.route('/video_camera')
def video_camera():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/thebeatlesplaypage.html')
def thebeatlesplaypage():
    return render_template('thebeatlesplaypage.html')


if __name__ == '__main__':
    app.run()
