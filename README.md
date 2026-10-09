# AI Driver Drowsiness & Distraction Detection System 🚘⚠️

A real-time computer vision university project built with Python, OpenCV, and MediaPipe. 

## Core Capabilities
* **Micro-Sleep Detection:** Calculates Eye Aspect Ratio (EAR) to trigger instant alerts if eyes close.
* **3D Distraction Tracking:** Monitors head pitch/yaw and iris movement to detect if the driver is looking away from the road, utilizing a smart "forgiveness window" for checking mirrors.
* **Yawn Detection:** Tracks the vertical and horizontal distance of the mouth to catch early signs of fatigue.

## How to Run
1. Install requirements: `pip install opencv-python mediapipe numpy pygame`
2. Run the system: `python main.py`
3. Press `q` to quit.