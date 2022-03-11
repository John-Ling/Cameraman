import cv2
from cv2 import CascadeClassifier


def main():
    cascade = CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Could not open camera")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1,
                minNeighbors=8,
                minSize=(60,60),
                maxSize=(300,300),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                pt1=(x, y),
                pt2=(x + w, y + h),
                color=(255,0,0),
                thickness=2
            )

            cv2.putText(frame, "Dumbass", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
