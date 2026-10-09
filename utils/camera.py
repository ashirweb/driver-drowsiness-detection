"""Handles webcam initialization and frame acquisition."""
import cv2
import logging
from typing import Tuple, Optional
import numpy as np

class Camera:
    def __init__(self, camera_index: int, width: int, height: int):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            logging.error(f"Failed to open camera index {self.camera_index}")
            raise RuntimeError("Camera connection failed.")
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def get_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Reads a frame from the webcam."""
        ret, frame = self.cap.read()
        if not ret:
            logging.warning("Failed to grab frame.")
            return False, None
        return True, frame

    def release(self):
        """Releases the camera resource."""
        self.cap.release()