import face_recognition
import os
import pickle
import hashlib

# Correct image folder path
image_folder = r"C:/Users/ANISH KUSHWAHA/OneDrive/Desktop/recommendation/app/images"

def generate_face_encodings_with_names_and_ids(image_folder):
    """
    Generate face encodings, unique IDs, and names for each face in the provided folder.
    Encodings, IDs, and names are saved to a pickle file for later use.

    Args:
        image_folder (str): Path to the folder containing face images.
    """
    # Initialize lists to hold the encodings, IDs, and names
    encodings = []
    face_ids = []
    names = []
    
    # Verify if the folder exists
    if not os.path.exists(image_folder):
        print(f"Error: The folder {image_folder} does not exist.")
        return
    
    # Loop through all the images in the provided folder
    for filename in os.listdir(image_folder):
        image_path = os.path.join(image_folder, filename)
        
        try:
            # Load the image and detect face locations
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            
            # Check if there are faces in the image
            if face_locations:
                # Generate the first face encoding for the image
                encoding = face_recognition.face_encodings(image, face_locations)[0]
                
                # Generate a unique Face ID using a hash of the encoding
                face_id = hashlib.sha256(encoding.tobytes()).hexdigest()
                
                # Extract the name from the filename (without the extension)
                name = os.path.splitext(filename)[0]
                
                # Append the encoding, Face ID, and name to the respective lists
                encodings.append(encoding)
                face_ids.append(face_id)
                names.append(name)
                print(f"Processed: {filename}, Name: {name}, Face ID: {face_id}")
            else:
                print(f"No face detected in {filename}. Skipping...")
        
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    # Save the encodings, Face IDs, and names to a pickle file
    face_data = {
        "encodings": encodings,
        "face_ids": face_ids,
        "names": names
    }
    
    os.makedirs("models", exist_ok=True)  # Create 'models' folder if it doesn't exist
    with open("models/face_encodings_with_ids_and_names.pkl", "wb") as f:
        pickle.dump(face_data, f)
    
    print(f"Face encodings, IDs, and names saved to models/face_encodings_with_ids_and_names.pkl")

# Call the function with the correct folder path
generate_face_encodings_with_names_and_ids(image_folder)
