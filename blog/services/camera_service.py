import cv2
import numpy as np
from typing import Optional, Tuple
import face_recognition
from blog.services.face_recognition_service import FaceRecognitionService
from blog.services.user_service import UserService
from sqlalchemy.orm import Session

class CameraService:
    def __init__(self, db: Session):
        self.db = db
        self.cap = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def start_camera(self):
        if self.cap is not None:
            self.stop_camera()
            
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            raise Exception("Không thể mở camera")
            
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
            
    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            cv2.destroyAllWindows()
            
    def process_frame(self) -> Tuple[np.ndarray, Optional[str]]:
        if self.cap is None:
            return None, None
            
        try:
            ret, frame = self.cap.read()
            if not ret:
                self.stop_camera()
                self.start_camera()
                return None, None
                
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(rgb_frame)
            if not face_locations:
                return frame, None
                
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            if not face_encodings:
                return frame, None
                
            users = UserService.get_all_users(self.db)
            for user in users:
                if user.face_embedding and FaceRecognitionService.compare_faces(user.face_embedding, face_encodings[0]):
                    top, right, bottom, left = face_locations[0]
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, user.full_name, (left, top - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    return frame, user.full_name
                    
            return frame, None
            
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            return None, None 