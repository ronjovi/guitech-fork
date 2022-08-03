import cvzone
import cv2


cap = cv2.VideoCapture(0)
success, img = cap.read()

imgFront = cv2.imread("static/images/Group 3.png", cv2.IMREAD_UNCHANGED)
imgFront = cv2.resize(imgFront, (0, 0), None, 0.809, 1)

hf, wf, cf = imgFront.shape
hb, wb, cb = img.shape

while True:
    success, img = cap.read()
    imgResult = cvzone.overlayPNG(img, imgFront, [0, hb-hf])

    cv2.imshow("Image", imgResult)
    cv2.waitKey(1)