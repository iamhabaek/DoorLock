import cv2
import face_recognition
from face_rec import FaceRecognition
#Encode faces from a folder


class Recognizer:
    
    def recognizer(self):
        face_rec  = FaceRecognition()
        face_rec.load_encoding_images()

        cap = cv2.VideoCapture(0)



        while True:
            ret, frame = cap.read()


            #Detect Known Faces
            face_locations,face_names = face_rec.detect_known_faces(frame)
            for face_loc, name in zip(face_locations,face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3] 
                cv2.rectangle(frame,(x1-20,y1-20),(x2+20,y2+20),(255,0,0),4)
                #cv2.rectangle(frame,(x1-20,y1-15),(x2+20,y2+20),(255,0,0),cv2.FILLED)
                cv2.putText(frame,name,(x1-20, y2 + 15),cv2.FONT_HERSHEY_DUPLEX,.5,(255,255,255),2)



            cv2.imshow("R E C O G N I Z E R",frame)

            key = cv2.waitKey(1)
            if key ==27:
                break
        cap.release()
        cv2.destroyAllWindows()