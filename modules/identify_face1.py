import face_recognition
import pickle

def identify_face(frame):
    known_faces = pickle.load(open("C:/Users/ANISH KUSHWAHA/OneDrive/Desktop/recommendation/app/models/face_encoding.pkl", "rb"))
    frame_encodings = face_recognition.face_encodings(frame)

    for encoding in frame_encodings:
        results = face_recognition.compare_faces(known_faces["encodings"], encoding)
        if True in results:
            return known_faces["names"][results.index(True)]
    return None