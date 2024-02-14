import cv2
import dlib
import numpy as np
import requests


# Used to get currently displayed content information (id, duration, etc..)
def get_current_content():
    req = requests.get("http://localhost:8000/content")
    return req.json()


def post_engagement_report(report):
    req = requests.post("http://localhost:8000/engagement-reports", json=report)
    return req


class MotionAndFacialDetection:
    def __init__(self):
        self.webcam_capture = cv2.VideoCapture(0)
        _, self.webcam_frame1 = self.webcam_capture.read()
        _, self.webcam_frame2 = self.webcam_capture.read()

        self.face_detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def motion_detection(self):
        while True:
            frame_difference = cv2.absdiff(self.webcam_frame1, self.webcam_frame2)
            convert_to_grayscale = cv2.cvtColor(frame_difference, cv2.COLOR_BGR2GRAY)
            image_blur = cv2.GaussianBlur(convert_to_grayscale, (5, 5), 0)
            _, threshold = cv2.threshold(image_blur, 20, 255, cv2.THRESH_BINARY)
            image_dilation = cv2.dilate(threshold, None, iterations=3)
            image_contours, _ = cv2.findContours(image_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for image_contour in image_contours:
                if cv2.contourArea(image_contour) < 2000:
                    continue
                x, y, w, h = cv2.boundingRect(image_contour)
                cv2.rectangle(self.webcam_frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

                region_of_interest = self.webcam_frame1[y:y + h, x:x + w]
                possible_faces = self.face_detector(region_of_interest)

                for possible_face in possible_faces:
                    current_content = get_current_content()
                    report = {
                        "id": current_content["id"]
                        # add more fields
                    }

                    post_engagement_report(report)

                    facial_landmarks = self.shape_predictor(region_of_interest, possible_face)
                    for n in range(0, 68):
                        x = facial_landmarks.part(n).x
                        y = facial_landmarks.part(n).y
                        cv2.circle(region_of_interest, (x, y), 2, (255, 0, 0), -1)

            cv2.imshow("webcam_feed", self.webcam_frame1)
            self.webcam_frame1 = self.webcam_frame2
            _, self.webcam_frame2 = self.webcam_capture.read()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.webcam_capture.release()
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    motion_and_facial_detection = MotionAndFacialDetection()
    motion_and_facial_detection.motion_detection()
