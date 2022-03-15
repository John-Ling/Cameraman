from serial.serialutil import SerialException
from imutils.video import VideoStream
import numpy as np
import imutils
import cv2
import serial
import time
import os

class Face_Tracker:
    def __init__(self, baudrate, timeout, port, serialEnabled):
        if (serialEnabled):
            try:
                print("Connecting to serial...")
                self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            except SerialException:
                print("Connection failed: Device not plugged in")
                quit()

        self.serialEnabled = serialEnabled
        self.confidence = 0.5 # constant for DNN certainty
        self.prototxt = "deploy.prototxt"
        self.model = "res10_300x300_ssd_iter_140000.caffemodel" # required for DNN face detection
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        print("Opening camera")
        try:
            self.cameraFeed = VideoStream(src=0).start()
        except IndexError:
            print("Could not open camera")
            quit()


    def track_face(self):
        while True:
            sendData = ""
            largestArea = 0
            centerCoordsX = 0
            centerCoordsY = 0
            frame = self.cameraFeed.read() # read frames from webcam
            frame = imutils.resize(frame, width=550, height=420)
            (h, w) = frame.shape[:2] # convert frame dimensions into blob

            blob = cv2.dnn.blobFromImage( # create blob
                image=cv2.resize(
                    frame, 
                    (300, 300)), 
                scalefactor=1.0, 
		        size=(300, 300), 
                mean=(104.0, 177.0, 123.0)
            )
            
            # pass blob through neural network and get detections
            self.net.setInput(blob)
            detections = self.net.forward()
            
            for i in range(0, detections.shape[2]):
                # get confidence of neural network's prediction
                confidence = detections[0, 0, i, 2]
                
                # remove weak predictions that are uncertain (confidence less than a certain threshold)
                if confidence < self.confidence:
                    continue

                # get coordinates for rectangle / bounding box
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
        
                cv2.rectangle(
                    frame, 
                    pt1=(startX, startY), 
                    pt2=(endX, endY),
                    color=(255, 255, 255), 
                    thickness=2)
                
                cv2.putText(frame, f'{endX - startX} : {endY - startY}', (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                width = endX - startX
                height = endY - startY
                area = width * height
                if area > largestArea:
                    if width >= 150 and height >= 150:
                        pass # ignore
                    else:
                        sendData = ""
                        largestArea = area
                        # get coordinates of rectangle center
                        centerCoordsX = 550 - (startX + width // 2)
                        centerCoordsY = (startY + height // 2)
                        coordsX = str(centerCoordsX)
                        sendData += coordsX
                        sendData += ':'
                        coordsY = str(centerCoordsY)
                        sendData += coordsY

            print(sendData)
            if (sendData.count(':') > 1 or (centerCoordsX < 0 or centerCoordsY < 0)): # check for invalid data format or values
                continue
            
            if (self.serialEnabled):
                self.arduino.write(bytes(sendData, 'utf-8'))
            time.sleep(0.025)
            
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cameraFeed.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # adjust port to port name face tracker is plugged into
    faceTracker = Face_Tracker(baudrate=9600, timeout=0.05, port='/dev/ttyACM0', serialEnabled=False)
    faceTracker.track_face()