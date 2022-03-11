import cv2
import serial
import time
from serial.serialutil import SerialException

class Face_Tracker:
    def __init__(self, baudrate, timeout, port, serialEnabled):
        if (serialEnabled):
            try:
                print("Connecting...")
                self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            except SerialException:
                print("Connection failed: Device not plugged in")
                quit()
        # face recognition    
        self.xCoordinates = 0
        self.yCoordinates = 0
        self.serialEnabled = serialEnabled
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
        self.cameraFeed = cv2.VideoCapture(0)

    def track_face(self):
        while True:
            sendData = ""
            largestArea = 0
            centerCoordsX = 0
            centerCoordsY = 0
            ret, frame = self.cameraFeed.read() # read frames from webcam
            if not ret:
                print("Couldn't open camera")
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # turn frame grayscale
            
            # detect faces in frame
            faces = self.faceCascade.detectMultiScale(
                gray, 
                scaleFactor=1.1,
                minNeighbors=6,
                minSize=(60,60),
                maxSize=(300,300),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(
                    frame,
                    pt1=(x, y),
                    pt2=(x + w, y + h),
                    color=(255, 255, 255),
                    thickness=2
                )

                cv2.putText(frame, f'{w} : {h}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                # determine largest rectangle assuming multiple faces are detected
                area = w * h
                if area > largestArea:
                    sendData = ""
                    largestArea = area
                    # get coordinates of rectangle center
                    centerCoordsX = round(550 - (x + w // 2))
                    centerCoordsY =  round(y + h // 2)
                    coordsX = str(centerCoordsX)
                    sendData += coordsX
                    sendData += ':'
                    coordsY = str(centerCoordsY)
                    sendData += coordsY

            print(sendData)
            if (sendData.count(':') > 1 or (centerCoordsX < 0 or centerCoordsY < 0)): # check for invalid data format or values
                pass
            else:
                if (self.serialEnabled):
                    try:
                        self.arduino.write(bytes(sendData, 'utf-8'))
                    except:
                        pass
            time.sleep(0.025)
            
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cameraFeed.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    faceTracker = Face_Tracker(baudrate=9600, timeout=0.05, port='/dev/ttyACM0', serialEnabled=False)
    faceTracker.track_face()