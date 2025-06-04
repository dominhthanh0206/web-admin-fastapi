import face_recognition
import numpy as np
from typing import Optional, Tuple
import pickle
import cv2

class FaceRecognitionService:
    @staticmethod
    def get_face_embedding(image_data: bytes) -> Optional[np.ndarray]:
        try:
            image_array = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            if image_array is None:
                print("Failed to decode image")
                return None
                
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            print(image_array)
            face_locations = face_recognition.face_locations(image_array)
            if not face_locations:
                print("No faces detected in the image")
                return None
                
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            if not face_encodings:
                print("Failed to generate face encodings")
                return None
                
            return face_encodings[0]
        except Exception as e:
            print(f"Error in face recognition: {str(e)}")
            return None

    @staticmethod
    def compare_faces(known_embedding: bytes, unknown_embedding: np.ndarray, tolerance: float = 0.6) -> bool:
        try:
            known_embedding_array = pickle.loads(known_embedding)
            distance = face_recognition.face_distance([known_embedding_array], unknown_embedding)[0]
            return distance <= tolerance
        except Exception as e:
            print(f"Error in face comparison: {str(e)}")
            return False

    @staticmethod
    def encode_embedding(embedding: np.ndarray) -> bytes:
        return pickle.dumps(embedding) 