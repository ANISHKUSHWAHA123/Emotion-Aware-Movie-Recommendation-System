from flask import Flask, jsonify, render_template, request
import cv2
import json
import threading
import asyncio
import websockets
import requests

from modules.detect_emotion import detect_emotion
from modules.identify_and_update_face import identify_and_update_face
from modules.get_user_by_face_id import get_user_by_face_id
from modules.recommendation import get_recommendations
from modules.start_gaze_control import start_gaze_control

app = Flask(__name__)
connected_clients = set()
poster_regions = []


# ---------------- WebSocket Handler ---------------- #
async def eye_gaze_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        while True:
            gaze_data = {"x": 500, "y": 300}  # Replace with actual gaze tracking logic
            await asyncio.sleep(0.1)  # Simulate ~10Hz updates
            for client in connected_clients.copy():
                try:
                    await client.send(json.dumps(gaze_data))
                except websockets.ConnectionClosed:
                    connected_clients.remove(client)
    except websockets.ConnectionClosed:
        connected_clients.remove(websocket)


# ---------------- Flask Routes ---------------- #
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    video = cv2.VideoCapture(1)
    ret, frame = video.read()
    video.release()

    if not ret:
        return jsonify({"error": "Failed to capture frame from camera"})

    emotion = detect_emotion(frame)
    face_id = identify_and_update_face(frame)
    user = get_user_by_face_id(face_id)

    if not user:
        return jsonify({"error": "User not found"})

    user_id = user['id']
    name = user['name']

    if user_id and emotion:
        recommendations = get_recommendations(user_id, emotion)
        return jsonify({"emotion": emotion, "user": name, "recommendations": recommendations})

    return jsonify({"error": "Unable to process request"})


@app.route('/start-gaze', methods=['POST'])
def start_gaze():
    global poster_regions
    try:
        if not poster_regions:
            return jsonify({"error": "Poster regions are not initialized"}), 400

        start_gaze_control(poster_regions)
        return jsonify({"status": "Gaze control started"})
    except Exception as e:
        print(f"Error starting gaze control: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/poster-regions', methods=['POST'])
def update_poster_regions():
    global poster_regions
    data = request.get_json()  # Correct way instead of requests.json
    poster_regions = data.get('regions', [])
    if poster_regions:
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"}), 400


# ---------------- Run Both Flask & WebSocket ---------------- #
def run_flask():
    app.run(debug=True, use_reloader=False)


async def main():
    # Start Flask in a background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Start WebSocket server
    async with websockets.serve(eye_gaze_handler, "localhost", 8000):
        print("WebSocket server started at ws://localhost:8000")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
