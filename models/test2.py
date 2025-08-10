import pickle

# Load the .pkl file
with open('face_encodings_with_ids_and_names.pkl', 'rb') as f:
    known_faces = pickle.load(f)

# Function to retrieve all face IDs and corresponding names
def get_all_face_ids_and_names():
    face_id_name_pairs = {}
    for face_id, name in zip(known_faces["face_ids"], known_faces["names"]):
        face_id_name_pairs[face_id] = name
    return face_id_name_pairs

# Example usage
all_face_ids_and_names = get_all_face_ids_and_names()

# Print all face IDs and corresponding names
for face_id, name in all_face_ids_and_names.items():
    print(f"Face ID: {face_id}, Name: {name}")
