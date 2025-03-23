import cv2
import concurrent.futures
from deepface import DeepFace
from simple_facerec import SimpleFacerec
from flask import Flask, Response, request, jsonify
import cv2
import base64
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json['image']
    img_data = base64.b64decode(data.split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    # You can add face recognition processing here

    return jsonify({"message": "Image received and processed"})

if __name__ == "__main__":
    app.run(debug=True)


# Load known faces
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Initialize webcam with reduced resolution
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

def analyze_face(face_frame):
    try:
        return DeepFace.analyze(img_path=face_frame, actions=['emotion'], enforce_detection=False, detector_backend='opencv')
    except Exception as e:
        print(f"DeepFace error: {e}")
        return None

# Store last detected emotion
last_emotion = {}

while True:
    success, frame = cap.read()
    if not success:
        break

    face_locations, face_names = sfr.detect_known_faces(frame)

    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc

        # Draw bounding box & name
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

        # Extract face for analysis
        face_frame = frame[y1:y2, x1:x2]
        if face_frame.size > 0:
            # Start DeepFace analysis asynchronously
            future = executor.submit(analyze_face, face_frame)
            
            # If DeepFace finishes, update the last emotion
            try:
                face_analysis = future.result(timeout=1.5)  # Increased timeout
                if face_analysis:
                    last_emotion[name] = face_analysis[0]['dominant_emotion']
            except concurrent.futures.TimeoutError:
                pass  # Skip this frame and use the last detected emotion

            # Display last detected emotion
            # //dfji=-sdfihs
            emotion = last_emotion.get(name, "Detecting...")
            cv2.putText(frame, emotion, (x1, y2 + 20), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Face Recognition & Emotion Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
executor.shutdown()
