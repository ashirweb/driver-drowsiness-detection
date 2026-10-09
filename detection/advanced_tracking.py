import math

def distance(p1, p2):
    """Calculates standard 2D distance."""
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def distance_3d(p1, p2):
    """Calculates 3D distance using Z-depth for higher AI accuracy."""
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def check_yawn(landmarks):
    """Advanced 3D Yawn Detection."""
    top_lip = landmarks.landmark[13]
    bottom_lip = landmarks.landmark[14]
    left_mouth = landmarks.landmark[78]
    right_mouth = landmarks.landmark[308]

    vert_dist = distance_3d(top_lip, bottom_lip)
    horz_dist = distance_3d(left_mouth, right_mouth)

    mar = vert_dist / (horz_dist + 1e-6)
    return mar > 0.55  # Tuned to prevent false alarms when talking

def get_head_pose(landmarks):
    """
    Advanced Head Pose AI. 
    Calculates Pitch (Up/Down) and Yaw (Left/Right) using 3D facial anchor ratios.
    """
    nose = landmarks.landmark[1]
    left_side = landmarks.landmark[234]
    right_side = landmarks.landmark[454]
    chin = landmarks.landmark[152]
    forehead = landmarks.landmark[10]

    # YAW (Looking Left/Right)
    left_dist = abs(nose.x - left_side.x)
    right_dist = abs(nose.x - right_side.x)
    yaw_ratio = left_dist / (right_dist + 1e-6)

    # PITCH (Looking Up/Down)
    nose_to_chin = distance_3d(nose, chin)
    nose_to_forehead = distance_3d(nose, forehead)
    pitch_ratio = nose_to_chin / (nose_to_forehead + 1e-6)

    if yaw_ratio > 2.0:
        return "LOOKING RIGHT"
    elif yaw_ratio < 0.5:
        return "LOOKING LEFT"
    elif pitch_ratio < 0.65:
        return "LOOKING DOWN (NODDING OFF)"
    elif pitch_ratio > 1.5:
        return "LOOKING UP"
    
    return "FORWARD"

def get_eye_gaze(landmarks):
    """
    Eye Tracking AI: Uses MediaPipe's advanced Iris points to detect 
    if the eyeballs are looking away from the road.
    """
    # Using the right eye corners and iris center
    eye_inner = landmarks.landmark[362]
    eye_outer = landmarks.landmark[263]
    iris = landmarks.landmark[473] 
    
    eye_width = distance(eye_inner, eye_outer)
    iris_to_inner = distance(iris, eye_inner)
    
    gaze_ratio = iris_to_inner / (eye_width + 1e-6)
    
    # Normal straight gaze sits around 0.45 - 0.55
    if gaze_ratio < 0.35:
        return "EYES OFF ROAD (RIGHT)"
    elif gaze_ratio > 0.65:
        return "EYES OFF ROAD (LEFT)"
    
    return "FOCUSED"