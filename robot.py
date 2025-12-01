from flask import Flask, render_template, Response, request
from picamera2 import Picamera2
import cv2
import RPi.GPIO as GPIO
import time
import threading
import atexit
import socket

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Motor_In1, Motor_In2, Motor_In3, Motor_In4 = 29, 31, 33, 35
for pin in [Motor_In1, Motor_In2, Motor_In3, Motor_In4]:
    GPIO.setup(pin, GPIO.OUT)

def move_forward():
    GPIO.output(Motor_In1, True)
    GPIO.output(Motor_In2, False)
    GPIO.output(Motor_In3, True)
    GPIO.output(Motor_In4, False)

def move_backward():
    GPIO.output(Motor_In1, False)
    GPIO.output(Motor_In2, True)
    GPIO.output(Motor_In3, False)
    GPIO.output(Motor_In4, True)

def turn_left():
    GPIO.output(Motor_In1, False)
    GPIO.output(Motor_In2, True)
    GPIO.output(Motor_In3, True)
    GPIO.output(Motor_In4, False)

def turn_right():
    GPIO.output(Motor_In1, True)
    GPIO.output(Motor_In2, False)
    GPIO.output(Motor_In3, False)
    GPIO.output(Motor_In4, True)

def stop_motors():
    GPIO.output(Motor_In1, False)
    GPIO.output(Motor_In2, False)
    GPIO.output(Motor_In3, False)
    GPIO.output(Motor_In4, False)

@atexit.register
def cleanup():
    stop_motors()
    GPIO.cleanup()

# Get local IP address for display
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# Camera & threading
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (320, 240)},
    buffer_count=3,
    controls={"FrameDurationLimits": (33333, 33333)}  # ~30 FPS
))
picam2.start()

frame_lock = threading.Lock()
latest_frame = None

def update_frames():
    global latest_frame
    while True:
        try:
            frame = picam2.capture_array()
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            ret, buffer = cv2.imencode('.jpg', frame_bgr)
            with frame_lock:
                latest_frame = buffer.tobytes()
        except Exception as e:
            print("Frame capture error:", e)
        time.sleep(0.03)  # ~30 FPS

# Start the thread
frame_thread = threading.Thread(target=update_frames, daemon=True)
frame_thread.start()

# Flask app
Url_Address = get_ip()
app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            with frame_lock:
                if latest_frame:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
            time.sleep(0.03)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template("temp.html", HTML_address=Url_Address)

@app.route('/Forward', methods=['POST'])
def forward():
    move_forward()
    return render_template("temp.html", HTML_address=Url_Address)

@app.route('/Backward', methods=['POST'])
def backward():
    move_backward()
    return render_template("temp.html", HTML_address=Url_Address)

@app.route('/left', methods=['POST'])
def left():
    turn_left()
    return render_template("temp.html", HTML_address=Url_Address)

@app.route('/right', methods=['POST'])
def right():
    turn_right()
    return render_template("temp.html", HTML_address=Url_Address)

@app.route('/stop', methods=['POST'])
def stop():
    stop_motors()
    return render_template("temp.html", HTML_address=Url_Address)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, threaded=True)
