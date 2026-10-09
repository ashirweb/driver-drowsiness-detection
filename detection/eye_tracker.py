"""Extracts eye landmarks from MediaPipe output."""
from typing import List, Tuple

# Standard MediaPipe indices for eyes
RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

def extract_eye_landmarks(landmarks, width: int, height: int, eye_indices: List[int]) -> List[Tuple[int, int]]:
    """Extracts (x, y) coordinates for specific eye landmark indices."""
    extracted_points = []
    for idx in eye_indices:
        point = landmarks.landmark[idx]
        x = int(point.x * width)
        y = int(point.y * height)
        extracted_points.append((x, y))
    return extracted_points