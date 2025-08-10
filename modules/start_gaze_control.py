import cv2
import dlib
import time
import pyautogui

# Initialize dlib's face detector (HOG-based) and the facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Ensure the predictor file exists

# Eye landmarks for the left and right eyes
LEFT_EYE = list(range(36, 42))
RIGHT_EYE = list(range(42, 48))

# Function to calculate the eye aspect ratio (EAR)
def calculate_ear(eye):
    # Vertical distances
    A = ((eye[1][1] - eye[5][1]) ** 2 + (eye[1][0] - eye[5][0]) ** 2) ** 0.5
    B = ((eye[2][1] - eye[4][1]) ** 2 + (eye[2][0] - eye[4][0]) ** 2) ** 0.5
    # Horizontal distance
    C = ((eye[0][1] - eye[3][1]) ** 2 + (eye[0][0] - eye[3][0]) ** 2) ** 0.5
    # EAR calculation
    return (A + B) / (2.0 * C)

# Thresholds for blinking
EAR_THRESHOLD = 0.25
CONSECUTIVE_FRAMES = 2

# Variables to track blink count and focus
blink_count = 0
frame_count = 0
focus_movie = None
trailer_links = []

def eye_gaze_control(poster_regions):
    global blink_count, frame_count
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            points = lambda indices: [(landmarks.part(i).x, landmarks.part(i).y) for i in indices]
            left_eye = points(LEFT_EYE)
            right_eye = points(RIGHT_EYE)

            # Calculate EAR for both eyes
            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            ear = (left_ear + right_ear) / 2

            if ear < EAR_THRESHOLD:
                frame_count += 1
            else:
                if frame_count >= CONSECUTIVE_FRAMES:
                    blink_count += 1
                    print(f"Blink detected! Count: {blink_count}")

                    if blink_count == 2:
                        cursor_position = pyautogui.position()
                        for region in poster_regions:
                            top_left = region['top_left']
                            bottom_right = region['bottom_right']
                            if top_left['x'] <= cursor_position.x <= bottom_right['x'] and \
                               top_left['y'] <= cursor_position.y <= bottom_right['y']:
                                print(f"Selecting movie: {region['id']}")
                                pyautogui.click()
                                break
                        blink_count = 0
                frame_count = 0

        cv2.imshow("Eye Gaze Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Function to initialize trailers and start gaze control
def start_gaze_control(poster_regions):
    print("Starting eye-gaze control with movie poster regions.")
    eye_gaze_control(poster_regions)

