"""Handles rendering text, bounding boxes, and UI elements on the frame."""
import cv2
from typing import List, Tuple

class OverlayManager:
    COLORS = {
        "NORMAL": (0, 255, 0),     # Green
        "WARNING": (0, 165, 255),  # Orange
        "DROWSY": (0, 0, 255)      # Red
    }

    @staticmethod
    def draw_landmarks(frame, landmarks: List[Tuple[int, int]], color=(0, 255, 255)):
        """Draws circles on given landmark coordinates."""
        for (x, y) in landmarks:
            cv2.circle(frame, (x, y), 2, color, -1)

    @staticmethod
    def display_metrics(frame, ear: float, fps: float):
        """Displays EAR and FPS values."""
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    @staticmethod
    def display_status(frame, status: str):
        """Displays the driver state with a colored banner if drowsy."""
        color = OverlayManager.COLORS.get(status, (255, 255, 255))
        
        if status == "DROWSY":
            # Draw red border around the whole frame
            h, w = frame.shape[:2]
            cv2.rectangle(frame, (0, 0), (w, h), color, 10)
            cv2.putText(frame, "WAKE UP!", (w//2 - 100, h//2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 4)

        cv2.putText(frame, f"Status: {status}", (10, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)