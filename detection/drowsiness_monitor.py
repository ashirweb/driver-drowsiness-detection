"""Tracks consecutive frames and determines driver state."""

class DrowsinessMonitor:
    def __init__(self, ear_threshold: float, warning_frames: int, drowsy_frames: int):
        self.ear_threshold = ear_threshold
        self.warning_frames = warning_frames
        self.drowsy_frames = drowsy_frames
        
        self.closed_frames_count = 0
        self.current_state = "NORMAL"

    def update(self, ear_value: float) -> str:
        """
        Updates the frame counter based on EAR and returns current state.
        States: NORMAL, WARNING, DROWSY
        """
        if ear_value < self.ear_threshold:
            self.closed_frames_count += 1
        else:
            self.closed_frames_count = max(0, self.closed_frames_count - 1)  # Gradual decrease

        if self.closed_frames_count >= self.drowsy_frames:
            self.current_state = "DROWSY"
        elif self.closed_frames_count >= self.warning_frames:
            self.current_state = "WARNING"
        else:
            self.current_state = "NORMAL"

        return self.current_state