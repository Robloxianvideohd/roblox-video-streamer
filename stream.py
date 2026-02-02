import cv2
import json
from flask import Flask, jsonify

app = Flask(__name__)

VIDEO_PATH = "video.mp4"  # Replace with your MP4 path
PIXELS = 64               # Resolution for Roblox
FPS = 30                  # Target FPS for Roblox

# Load video
cap = cv2.VideoCapture(VIDEO_PATH)
video_fps = cap.get(cv2.CAP_PROP_FPS)
frame_skip = max(int(video_fps / FPS), 1)

frames = []
frame_count = 0

# Preload all frames into memory
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_skip == 0:
        # Resize to 32x32
        small_frame = cv2.resize(frame, (PIXELS, PIXELS))
        # Convert BGR to RGB
        pixels = [[ [int(r), int(g), int(b)] for b,g,r in row] for row in small_frame]
        frames.append(pixels)

    frame_count += 1

cap.release()
frame_index = 0

@app.route("/frame")
def frame_endpoint():
    global frame_index
    frame = frames[frame_index]
    frame_index = (frame_index + 1) % len(frames)  # Loop video
    return jsonify(frame)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
