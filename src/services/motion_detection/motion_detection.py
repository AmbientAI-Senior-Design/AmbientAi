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
        self.face_trackers = []

    @staticmethod
    def rectangle_to_tuple(rectangle):
        return rectangle.left(), rectangle.top(), rectangle.width(), rectangle.height()  # (x, y, w, h)

    def run(self):
        detection_frequency = 2
        frame_count = 0

        while True:
            _, frame = self.webcam_capture.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_count += 1

            # Run face detection frequently
            if frame_count % detection_frequency == 0:
                self.face_trackers = []
                faces = self.face_detector(gray_frame)
                for face in faces:
                    face_tracker = dlib.correlation_tracker()
                    tracked_face_rect = dlib.rectangle(face.left(), face.top(), face.right(), face.bottom())
                    face_tracker.start_track(frame, tracked_face_rect)
                    tracker_data = {'tracker': face_tracker}
                    self.face_trackers.append(tracker_data)

            # Update trackers and draw facial landmarks
            for tracker_dict in self.face_trackers:
                tracker = tracker_dict['tracker']
                tracker.update(frame)
                pos = tracker.get_position()
                cv2.rectangle(frame, (int(pos.left()), int(pos.top())), (int(pos.right()), int(pos.bottom())), (0, 255, 0), 3)
                tracked_rectangle = dlib.rectangle(int(pos.left()), int(pos.top()), int(pos.right()), int(pos.bottom()))
                landmarks = self.shape_predictor(gray_frame, tracked_rectangle)
                for n in range(0, 68):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

            # Print the number of faces currently detected
            text = f"Faces Detected in Frame: {len(self.face_trackers)}"
            cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.webcam_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    motion_and_facial_detection = MotionAndFacialDetection()
    motion_and_facial_detection.run()
