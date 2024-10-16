from flask import Flask, Response, jsonify, render_template
from ultralytics import YOLO
import cv2

app = Flask(__name__)

# Load YOLO model that detects both fire and smoke
model = YOLO('best1.pt')  # Update to the model trained for fire and smoke

# Initialize variables
fire_detected = False
smoke_detected = False
camera = cv2.VideoCapture(0)  # Assuming source=0 is your camera

def generate_camera_feed():
    global fire_detected, smoke_detected
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Run YOLO model for fire and smoke detection
        results = model.predict(frame, conf=0.25)

        # Reset detection flags
        fire_detected = False
        smoke_detected = False

        # Check if 'fire' or 'smoke' is detected in the results
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_name = model.names[int(box.cls)]
                    if 'fire' in class_name:  # Check if the detected class is 'fire'
                        fire_detected = True
                    if 'smoke' in class_name:  # Check if the detected class is 'smoke'
                        smoke_detected = True

                    # Draw bounding boxes on the frame
                    coords = box.xyxy[0].numpy()  # Get the bounding box coordinates
                    cv2.rectangle(frame, (int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3])), (0, 0, 255), 2)  # Red box for fire
                    cv2.putText(frame, class_name, (int(coords[0]), int(coords[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Serves the HTML file for the homepage

# Route for the video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_camera_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to check fire and smoke detection
@app.route('/check-fire-smoke', methods=['GET'])
def check_fire_smoke():
    return jsonify({"fireDetected": fire_detected, "smokeDetected": smoke_detected})

if __name__ == '__main__':
    app.run(debug=True)
