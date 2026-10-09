"""Main entry point for the Driver Drowsiness Detection System."""
import cv2
import time
import os
import mediapipe as mp
from config import settings
from utils.camera import Camera
from utils.logger import EventLogger
from detection.face_detector import FaceDetector
from detection.eye_tracker import extract_eye_landmarks, LEFT_EYE_INDICES, RIGHT_EYE_INDICES
from detection.ear_calculator import calculate_ear
from detection.drowsiness_monitor import DrowsinessMonitor
from alerts.alarm import AlarmManager
from ui.overlays import OverlayManager
from detection.advanced_tracking import check_yawn, get_head_pose, get_eye_gaze

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

def ensure_directories():
    """Ensure necessary directories exist."""
    os.makedirs("assets", exist_ok=True)
    os.makedirs(settings.DB_DIR, exist_ok=True)

def main():
    ensure_directories()
    
    # Initialize Modules
    cam = Camera(settings.CAMERA_INDEX, settings.FRAME_WIDTH, settings.FRAME_HEIGHT)
    face_detector = FaceDetector()
    drowsiness_monitor = DrowsinessMonitor(
        ear_threshold=settings.EAR_THRESHOLD,
        warning_frames=settings.CONSEC_FRAMES_WARNING,
        drowsy_frames=settings.CONSEC_FRAMES_DROWSY
    )
    alarm_manager = AlarmManager(settings.ALARM_PATH, settings.ALARM_VOLUME)
    logger = EventLogger(settings.DB_PATH, settings.DB_DIR)
    
    prev_time = 0
    last_logged_status = "NORMAL"
    distraction_frames = 0

    print("System initialized. Press 'q' to quit.")

    try:
        while True:
            ret, frame = cam.get_frame()
            if not ret:
                break

            current_time = time.time()
            fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
            prev_time = current_time

            landmarks = face_detector.process_frame(frame)
            ear = 0.0
            status = "NORMAL"

            if landmarks:
                # Draw full face mesh
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                )

                h, w = frame.shape[:2]
                
                left_eye = extract_eye_landmarks(landmarks, w, h, LEFT_EYE_INDICES)
                right_eye = extract_eye_landmarks(landmarks, w, h, RIGHT_EYE_INDICES)
                
                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)
                ear = (left_ear + right_ear) / 2.0
                
                is_yawning = check_yawn(landmarks)
                head_pose = get_head_pose(landmarks)
                eye_gaze = get_eye_gaze(landmarks)

                if is_yawning:
                    cv2.putText(frame, "YAWNING!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                
                # --- DISTRACTION LOGIC & DELAY ---
                if head_pose != "FORWARD" or eye_gaze != "FOCUSED":
                    distraction_frames += 1
                    # Override the EAR calculation so looking sideways doesn't trigger "DROWSY"
                    ear = 1.0 
                else:
                    distraction_frames = 0 

                # Show text warning on screen after ~1 second (20 frames)
                if distraction_frames > 20: 
                    if head_pose != "FORWARD":
                        cv2.putText(frame, f"HEAD DISTRACTED: {head_pose}", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    elif eye_gaze != "FOCUSED":
                        cv2.putText(frame, f"EYE WARNING: {eye_gaze}", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
                # ---------------------------------
                
            # Update Drowsiness Monitor (eyes closed)
            status = drowsiness_monitor.update(ear)
            
            # --- ALARM LOGIC ---
            # Trigger alarm if eyes closed OR if head is turned for more than 45 frames (~2.5 seconds)
            if status == "DROWSY" or distraction_frames > 45:
                alarm_manager.play()
            else:
                alarm_manager.stop()
            # -------------------
                
            if status != last_logged_status and status != "NORMAL":
                logger.log_event(ear, status)
            last_logged_status = status

            OverlayManager.display_metrics(frame, ear, fps)
            OverlayManager.display_status(frame, status)

            cv2.imshow("Driver Drowsiness Detection System", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("Application interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        alarm_manager.stop()
        cam.release()
        cv2.destroyAllWindows()
        print("System safely shutdown.")

if __name__ == "__main__":
    main()