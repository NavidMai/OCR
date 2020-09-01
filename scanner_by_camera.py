# -*- coding: utf-8 -*-
import cv2
import time
import imutils
import threading
import pytesseract
from pytesseract import Output
from pyzbar import pyzbar


class IpcamCapture:
    def __init__(self, url):
        self.Frame = []
        self.status = False
        self.isstop = False

        self.capture = cv2.VideoCapture(url)

    def start(self):
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        self.isstop = True
        print('ipcam stopped!')

    def getframe(self):
        return self.Frame

    def queryframe(self):
        while not self.isstop:
            self.status, self.Frame = self.capture.read()

        self.capture.release()


# Test Camera
rtsp = "rtsp://admin:admin@172.16.12.240:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
# IronYun Right Front Door
# rtsp = "rtsp://172.16.22.100:554/live01/ss-Tunnel/media?stream=5&channel=1"

print("[INFO] starting video stream...")
print("====================================================================")

ipcam = IpcamCapture(rtsp)
ipcam.start()
time.sleep(1)

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream.
    img = ipcam.getframe()
    # resize it to have a maximum width of 10git 00 pixels
    img = imutils.resize(img, width=1000)

    # QCR
    startTime = time.time()
    h, w, c = img.shape
    d = pytesseract.image_to_data(img, lang='eng', output_type=Output.DICT)
    # print(d.keys())
    n_boxes = len(d['text'])

    for i in range(n_boxes):
        if not d['text'][i].isspace():
            if len(d['text'][i]) != 0:
                if int(d['conf'][i]) > 60:
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, d['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    endTime = time.time()

                    print('Confidence: ' + str(d['conf'][i]))
                    print('Text: ' + d['text'][i])
                    print('Pixel(W * H): ' + str(w) + '*' + str(h))
                    print("Time Elapsed: " + str(endTime - startTime) + " seconds")
                    print('----------------------------------------------------------------')

    # Barcode scanner
    startTime1 = time.time()
    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(img)

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw it surrounding the barcode on the image
        (x1, y1, w1, h1) = barcode.rect
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
        # convert the barcode data to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        endTime1 = time.time()

        print("Barcode Detected: " + barcodeData + " (Type: " + barcodeType + ")")
        print("Pixel(W * H): " + str(w1) + " * " + str(h1))
        print("Time Elapsed: " + str(endTime1 - startTime1) + " seconds")
        print('----------------------------------------------------------------')

    cv2.imshow('Scanner', img)
    # if the "ESC" key was pressed, break from the loop
    if cv2.waitKey(1000) == 27:
        print("====================================================================")
        print("[INFO] cleaning up...")
        cv2.destroyAllWindows()
        ipcam.stop()
        break
