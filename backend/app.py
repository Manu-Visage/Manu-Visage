from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import face_recognition
import numpy as np

app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

@app.route('/recognize', methods=['POST'])
def recognize_face():
    file = request.files['image']
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    if len(face_encodings) > 0:
        return jsonify({"message": "Face detected", "face_count": len(face_encodings)})
    else:
        return jsonify({"message": "No face detected"}), 400

if __name__ == '__main__':
    app.run(debug=True)
