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
        if not self.webcam_capture.isOpened():
            print("Error: Could not open video capture.")
            exit()

        self.face_detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.face_trackers = []

    def rectangle_to_tuple(self, rectangle):
        return (rectangle.left(), rectangle.top(), rectangle.width(), rectangle.height())  # (x, y, w, h)

    def run(self):
        while True:
            _, frame = self.webcam_capture.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Handle trackers and cleanup
            for tracker_dict in self.face_trackers[:]:
                tracker = tracker_dict['tracker']
                pos = tracker.get_position()
                tracked_rectangle = dlib.rectangle(int(pos.left()), int(pos.top()), int(pos.right()), int(pos.bottom()))
                tracked_region = gray_frame[tracked_rectangle.top():tracked_rectangle.bottom(), tracked_rectangle.left():tracked_rectangle.right()]

                # Remove tracker if face is no longer detected within the region
                if len(self.face_detector(tracked_region)) == 0:
                    self.face_trackers.remove(tracker_dict)

                # Draw rectangle around tracked facial landmarks
                cv2.rectangle(frame, (int(pos.left()), int(pos.top())), (int(pos.right()), int(pos.bottom())), (0, 255, 0), 3)
                landmarks = self.shape_predictor(gray_frame, tracked_rectangle)
                for n in range(0, 68):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

            # Check for new faces and initialize trackers
            if len(self.face_trackers) == 0:
                faces = self.face_detector(gray_frame)
                for face in faces:
                    face_tracker = dlib.correlation_tracker()
                    face_tracker.start_track(frame, face)
                    tracker_data = {'tracker': face_tracker, 'id': len(self.face_trackers)}
                    self.face_trackers.append(tracker_data)

            # Print the number of faces currently detected
            text = f"Faces Detected in Frame: {len(self.face_trackers)}"
            cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.webcam_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = MotionAndFacialDetection()
    detector.run()

#removed current content and engagement report parts - need to implement at a future date
