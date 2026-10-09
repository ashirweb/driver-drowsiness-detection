"""Calculates Eye Aspect Ratio (EAR)."""
import numpy as np
from typing import List, Tuple

def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculates Euclidean distance between two points."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_ear(eye_landmarks: List[Tuple[float, float]]) -> float:
    """
    Calculates the Eye Aspect Ratio (EAR).
    eye_landmarks must contain 6 (x,y) coordinates in standard order.
    """
    if len(eye_landmarks) != 6:
        return 0.0
        
    # Vertical distances
    v1 = euclidean_distance(eye_landmarks[1], eye_landmarks[5])
    v2 = euclidean_distance(eye_landmarks[2], eye_landmarks[4])
    
    # Horizontal distance
    h = euclidean_distance(eye_landmarks[0], eye_landmarks[3])
    
    # Calculate EAR
    ear = (v1 + v2) / (2.0 * h)
    return float(ear)