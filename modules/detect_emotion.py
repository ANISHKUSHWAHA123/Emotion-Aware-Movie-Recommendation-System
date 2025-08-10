import cv2
import numpy as np
from tensorflow.keras.models import load_model

def detect_emotion(frame):
    model = load_model("C:/Users/ANISH KUSHWAHA/OneDrive/Desktop/recommendation/app/models/emotion_model.h5")
    emotions = ['Happy', 'Sad', 'Anger', 'Surprise', 'Neutral', 'Disgust', 'Fear']
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y + h, x:x + w]
        roi_resized = cv2.resize(roi_gray, (48, 48)).reshape(1, 48, 48, 1) / 255.0
        emotion_index = np.argmax(model.predict(roi_resized))
        return emotions[emotion_index]
    return None
