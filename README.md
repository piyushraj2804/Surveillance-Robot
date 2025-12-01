# 🚗 Raspberry Pi Robot Car with Live Camera Streaming (Flask + PiCamera2)

This project allows you to **control a Raspberry Pi robot car** remotely through a **web interface**, with **live video streaming** using the Raspberry Pi Camera (Picamera2).  
It uses **Flask** for the web server, **OpenCV** for video encoding, and **RPi.GPIO** for controlling the motors.

---

## 🧩 Features

- 🖥️ Web-based control panel (accessible from any device in the same network)
- 🎥 Live camera feed (MJPEG stream at ~30 FPS)
- ⏩ Movement controls: Forward, Backward, Left, Right, Stop
- 🔌 Automatic GPIO cleanup on exit
- 🌐 Displays local IP address for easy access

---

## 🧠 Project Overview

The Flask web app runs on the Raspberry Pi.  
You can open the Pi’s IP address in a browser (on your phone or computer) and:
- View the live video feed from the PiCamera2.
- Control the motors in real time.

---

## 🛠️ Hardware Requirements

- Raspberry Pi (3B/4B or newer recommended)
- PiCamera2 (with libcamera support)
- Motor Driver (e.g., L298N or L293D)
- 2 DC Motors
- Jumper wires
- **External power supply (9V–12V for motors)**
- Breadboard (optional)

---

## ⚙️ Wiring Diagram

| Component / Connection | Raspberry Pi Pin (BOARD Mode) | Description |
|------------------------:|:-----------------------------:|-------------|
| Motor Driver IN1 | 29 | Motor 1 control A |
| Motor Driver IN2 | 31 | Motor 1 control B |
| Motor Driver IN3 | 33 | Motor 2 control A |
| Motor Driver IN4 | 35 | Motor 2 control B |
| Motor Driver ENA / ENB | Optional PWM pins | Motor speed control (optional) |
| Motor Driver VCC (5V logic) | 2 (5V) | Power for motor driver logic |
| Motor Driver 12V / Vmotor | **External 9V–12V power supply (+)** | Power source for motors |
| Motor Driver GND | Connect to Pi GND **and** external power supply (–) | Common ground connection |
| Motor Output A/B | DC Motors | Connect left & right motors |
| PiCamera2 | CSI Port | Video streaming |

🔋 **Important:**  
Always connect the **ground (GND)** of the Raspberry Pi and the **external motor power supply** together.  
This ensures a **common electrical reference** between logic signals and motor power.

---

## 🧰 Software Requirements

Make sure you have the following installed on your Raspberry Pi:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-opencv python3-flask python3-picamera2
sudo apt install libatlas-base-dev
```
Then install the GPIO library if needed:
```
pip install RPi.GPIO
```
📂 Project Structure
raspi-car/
├── app.py              # Main Flask application (this file)
├── templates/
│   └── temp.html       # Front-end control panel template
└── README.md           # Project documentation

How It Works
1. Flask Web Server
The Flask app serves:
A control page (temp.html) for motor control buttons.
A video stream endpoint at /video_feed.

3. Motor Control
GPIO pins (29, 31, 33, 35) are used to control motor direction:
Forward → IN1 + IN3 HIGH
Backward → IN2 + IN4 HIGH
Left / Right → Selective pin combinations

3. Live Video Streaming
The Picamera2 module captures frames, which are converted to JPEG and streamed via MJPEG over HTTP.
🌐 Running the Application
Clone this repository:
```
git clone https://github.com/<your-username>/raspi-car.git
cd raspi-car
```

Run the Flask app:

python3 app.py


Check your Pi’s IP address printed in the terminal or shown on the web page.
Then open it on another device in the same network:

http://<raspberry-pi-ip>:8080


Use the control buttons to move the robot and watch the live stream!

📸 Web Interface Preview

The web interface includes:

Live video stream

Movement control buttons: Forward, Backward, Left, Right, Stop


🧼 Cleanup and Safety

The app automatically:

Stops all motors when exiting

Cleans up GPIO pins using atexit.register()

You can also manually stop the Flask server with:

Ctrl + C

🧩 Troubleshooting
Problem	Possible Solution
Camera not detected	Ensure Picamera2 is enabled via raspi-config
“Address already in use”	Another Flask app is running on port 8080
No motor movement	Check wiring, motor driver enable pins, and power connections
Motors only move one direction	Verify GPIO pin mapping and wiring order
Slow or lagging stream	Reduce frame size or frame rate in create_video_configuration()
🧑‍💻 Author

Kshitij Prasad
📍 GitHub Profile

💡 B.Tech Student at ITER, Siksha ‘O’ Anusandhan

📜 License

This project is licensed under the MIT License — feel free to use, modify, and share it.
