import face_recognition
import pickle
import os
import hashlib

# Path to the encoding file
encoding_file_path = "C:/Users/ANISH KUSHWAHA/OneDrive/Desktop/recommendation/app/models/face_encodings_with_ids_and_names.pkl"

def identify_and_update_face(frame):
    # Load existing encodings
    if os.path.exists(encoding_file_path):
        known_faces = pickle.load(open(encoding_file_path, "rb"))
    else:
        known_faces = {"encodings": [], "face_ids": [], "names": []}
    
    frame_encodings = face_recognition.face_encodings(frame)
    
    for encoding in frame_encodings:
        # Compare face encodings with known faces
        results = face_recognition.compare_faces(known_faces["encodings"], encoding)
        
        if True in results:
            # Recognized user: Return the name
            return known_faces["face_ids"][results.index(True)]
        else:
            # New user detected
            face_id = hashlib.sha256(encoding.tobytes()).hexdigest()  # Generate Face ID
            
            # Prompt for name (can be replaced with a form in a web app)
            name = input("New user detected! Please enter a name: ") or f"user_{len(known_faces['names']) + 1}"
            
            # Update known_faces with the new user
            known_faces["encodings"].append(encoding)
            known_faces["face_ids"].append(face_id)
            known_faces["names"].append(name)
            
            # Save updated data
            with open(encoding_file_path, "wb") as f:
                pickle.dump(known_faces, f)
            
            print(f"New user added: Name: {name}, Face ID: {face_id}")
            return face_id  # Return the newly added name

    return None  # Return None if no faces are detected in the frame
