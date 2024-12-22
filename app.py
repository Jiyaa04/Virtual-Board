from flask import Flask, Response, render_template_string
import cv2
from flask_cors import CORS

# Define the app first
app = Flask(__name__)

# Enable CORS
CORS(app)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Generate frames from webcam
def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Air Canvas</title>
    </head>
    <body>
        <h1>Air Canvas Streaming</h1>
        <img src="{{ url_for('video_feed') }}" alt="Air Canvas">
    </body>
    </html>
    """)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
