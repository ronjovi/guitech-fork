import cv2
import mediapipe as mp
import time
import cvzone
import numpy as np
from flask import Flask, render_template, Response
app = Flask(__name__)

camera = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


def hand_tracking(camera_frame):
    image_rgb = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    fontScale = int (1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # hidelist = [0, 1, 2, 5, 6, 9, 10, 13, 14, 17, 18]
                    # for id in hidelist:
                    #     if id != hidelist:
                            # print(id,lm)
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

                # cv2.imshow("Image", camera_frame)
                # cv2.waitKey(1)


def fret_overlay(frame):
        hf, wf, cf = imgFront.shape
        hb, wb, cb = frame.shape
        result = cvzone.overlayPNG(frame, imgFront, [0, hb - hf])

        cv2.imshow("Image", result)
        cv2.waitKey(1)


def gen_frames():
    while True:
        success, frame = camera.read()
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Show images
        hf, wf, cf = imgFront.shape
        hb, wb, cb = frame.shape
        if not success:
            break
        else:
            hand_tracking(frame)
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
