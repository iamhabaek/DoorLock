import face_recognition
import cv2
import os
import glob
import numpy as np
import mysql.connector
class FaceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self):
        conn = mysql.connector.connect(
                        host ="localhost",
                        user = "root",
                        password = "B)omerang1",
                        database = "doorsecurity"
                            )
        cursor = conn.cursor()
        cursor.execute('select * from room_users')
        a = cursor.fetchall()
        result = np.asarray(a)
        for row in result:
            img = np.frombuffer(row[4],np.uint8)
            img_np = cv2.imdecode(img, cv2.IMREAD_COLOR) #  in OpenCV 3.1
            rgb_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            img_encoding = face_recognition.face_encodings(rgb_img)[0]
            names = row[1] + " " + row[2]
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(names)
            print(self.known_face_names)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding,tolerance=0.4)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
