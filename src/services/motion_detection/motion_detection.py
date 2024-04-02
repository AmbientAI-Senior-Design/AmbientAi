import cv2
import dlib
import numpy as np
import requests
import math
import threading

engagement_counter = 0

# Used to get currently displayed content information (id, duration, etc..)
def get_current_content():
    req = requests.get("http://localhost:8000/content")
    return req.json()

def post_engagement_report(report):
    req = requests.post("http://localhost:8000/engagement-reports", json=report)
    return req


def calculate_triangle_perimeter(point1, point2, point3):
    # Calculate distance between two points
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    # Calculate perimeter using the distances between the vertices
    side1 = distance(point1, point2)
    side2 = distance(point2, point3)
    side3 = distance(point3, point1)

    perimeter = side1 + side2 + side3
    return perimeter


SCALE_FACTOR = 0.257

def calculate_distance_in_cm(perimeter):
    return perimeter * SCALE_FACTOR


class MotionAndFacialDetection:
    def __init__(self):
        self.engagement_counter = 0
        self.activity = False
        self.webcam_capture = cv2.VideoCapture(0)
        _, self.webcam_frame1 = self.webcam_capture.read()
        _, self.webcam_frame2 = self.webcam_capture.read()

        self.face_detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.hog = cv2.HOGDescriptor()
        self.face_trackers = []
        # Load pre-trained model
        self.net = cv2.dnn.readNet("yolov7-tiny.weights", "yolov7-tiny.cfg")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.event = False 
        self.prev_activity = None

    @staticmethod
    def rectangle_to_tuple(rectangle):
        return rectangle.left(), rectangle.top(), rectangle.width(), rectangle.height()  # (x, y, w, h)

    def detect_people(self, frame):
        height, width, channels = frame.shape

        # Convert image to blob for the model
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        # Post-process the detections
        class_ids = []
        confidences = []
        boxes = []
        counter2 = 0
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:  # Assuming class_id 0 corresponds to a person
                    center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        if len(boxes) > 0:
            self.activity = True
        else:
            self.activity = False
        self.activity_check()

        # Apply non-maximum suppression to remove redundant overlapping boxes
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Draw bounding boxes on the image
        people_boxes = []
        for i in range(len(boxes)):
            if i in indices:
                x, y, w, h = boxes[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                people_boxes.append((x, y, x + w, y + h))

        return people_boxes
    def send_engagement_score(self):
        if self.engagement_counter > 0:
            data = {"score":self.engagement_counter}
            try:
                response = requests.post("http://localhost:8000/engagement", json=data)
                print(f"Engagement score sent: {data['score']} - Server response: {response.status_code}")
                #self.engagement_counter = 0 #potentially adding this
            except Exception as e:
                print(f"Failed to send engagement score: {e}")
    def activity_check(self):
        if self.activity != self.prev_activity:
            self.activity = self.prev_activity
            event_type = "not_engaged" if self.activity else "leave"
            response = requests.post(f"http://localhost:8000/events/{event_type}")
            print(f"Activity state changed to {self.activity}. Response: {response.status_code}")
            
            # Update the previous activity state after sending the POST request
            self.prev_activity = self.activity

    def run(self):
        detection_frequency = 2
        frame_count = 0

        while True:
            time_in = cv2.getTickCount()

            _, frame = self.webcam_capture.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_count += 1
            engaged = False
            text_post = (10, 100)

            # Detect people
            people_boxes = self.detect_people(frame)
            self.face_trackers = []

            # Run face detection only when people are detected
            if people_boxes:
                # get a frame for each people box
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
                cv2.rectangle(frame, (int(pos.left()), int(pos.top())), (int(pos.right()), int(pos.bottom())),
                              (0, 255, 0), 3)
                tracked_rectangle = dlib.rectangle(int(pos.left()), int(pos.top()), int(pos.right()), int(pos.bottom()))
                landmarks = self.shape_predictor(gray_frame, tracked_rectangle)
                #self.engagement_counter += 1
                # Points of interest
                points_of_interest = [19, 33, 24]
                interest_coordinates = []

                for point in points_of_interest:
                    x = landmarks.part(point).x
                    y = landmarks.part(point).y
                    interest_coordinates.append((x, y))
                    cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

                # Draw a triangle connecting the points of interest
                if len(interest_coordinates) == 3:
                    perimeter = calculate_triangle_perimeter(interest_coordinates[0], interest_coordinates[1], interest_coordinates[2])
                    distance = calculate_distance_in_cm(perimeter)
                    cv2.putText(frame, "User Engaged", text_post, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                    event_type = "user_engaged"
                    response = requests.post(f"http://localhost:8000/events/{event_type}")
                    print(f"Activity state changed to {self.activity}. Response: {response.status_code}")
            
                    cv2.polylines(frame, [np.array(interest_coordinates)], isClosed=True, color=(0, 0, 255),
                                  thickness=2)
                    engaged = True
                    if not self.event:
                        self.event = True
                    self.engagement_counter +=1
            if not engaged and self.event:
                self.event = False
                self.send_engagement_score()
                self.engagement_counter = 0
            print(f"Engagement Counter: {self.engagement_counter}")
            time_out = cv2.getTickCount()
            time_diff = time_out - time_in
            ticks_to_seconds = cv2.getTickFrequency()
            print(f"Time taken: {time_diff / ticks_to_seconds} seconds")

            if not engaged:
                cv2.putText(frame, "User not Engaged", text_post, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

            # Print the number of faces currently detected
            text = f"Faces Detected in Frame: {len(self.face_trackers)}"
            
            #print(engagement_counter)
            cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.webcam_capture.release()
        cv2.destroyAllWindows()
#using threading to send score every 5 seconds
#def timed_send_score(detection_run, interval=5):
    #threading.Timer(interval, timed_send_score, [detection_run, interval]).start()
   # detection_run.send_engagement_score()


if __name__ == "__main__":
    motion_and_facial_detection = MotionAndFacialDetection()

    #timed_send_score(motion_and_facial_detection)

    motion_and_facial_detection.run()