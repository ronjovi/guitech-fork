import cv2
import mediapipe as mp
import time
from flask import Flask, render_template, Response
app = Flask(__name__)

camera = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


def gen_frames():
    while True:
        success, img = camera.read()
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgrgb)
        # print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    print(id, cx, cy)
                    if id == 0:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3
        # (255,0,255),3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

        # success, frame = camera.read()
        # if not success:
        #     break
        # else:
        #     ret, buffer = cv2.imencode('.jpg', frame)
        #     frame = buffer.tobytes()
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/camera_feed')
def camera_feed():
    return render_template('camera_feed.html')


@app.route('/video_camera')
def video_camera():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
