"""Configuration settings for the Drowsiness Detection System."""
import os

# Camera Settings
CAMERA_INDEX: int = 0
FRAME_WIDTH: int = 640
FRAME_HEIGHT: int = 480

# Drowsiness Detection Thresholds
EAR_THRESHOLD: float = 0.25      # Below this ratio, eyes are considered closed
CONSEC_FRAMES_WARNING: int = 15  # Frames to trigger WARNING state
CONSEC_FRAMES_DROWSY: int = 30   # Frames to trigger DROWSY state and alarm

# Audio Settings
ALARM_PATH: str = os.path.join("assets", "alarm.wav")
ALARM_VOLUME: float = 0.8

# Logging Settings
DB_DIR: str = "data"
DB_PATH: str = os.path.join(DB_DIR, "logs.db")