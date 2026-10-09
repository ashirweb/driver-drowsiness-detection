"""Manages audible alarm playback using Pygame."""
import pygame
import logging
import os

class AlarmManager:
    def __init__(self, sound_path: str, volume: float = 0.8):
        self.sound_path = sound_path
        self.is_playing = False
        self.sound_loaded = False
        
        try:
            pygame.mixer.init()
            if os.path.exists(self.sound_path):
                self.alarm_sound = pygame.mixer.Sound(self.sound_path)
                self.alarm_sound.set_volume(volume)
                self.sound_loaded = True
            else:
                logging.warning(f"Alarm sound file not found at {self.sound_path}")
        except pygame.error as e:
            logging.error(f"Failed to initialize Pygame mixer: {e}")

    def play(self):
        """Starts playing the alarm continuously."""
        if self.sound_loaded and not self.is_playing:
            self.alarm_sound.play(loops=-1)  # Loop indefinitely
            self.is_playing = True

    def stop(self):
        """Stops the alarm."""
        if self.sound_loaded and self.is_playing:
            self.alarm_sound.stop()
            self.is_playing = False