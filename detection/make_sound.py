import numpy as np
import scipy.io.wavfile as wavfile
import os

# Ensure the assets folder exists
os.makedirs("assets", exist_ok=True)

# Generate a 1000 Hz beep sound
sample_rate = 44100
duration = 0.5  # half a second
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_data = (np.sin(2 * np.pi * 1000 * t) * 32767).astype(np.int16)

# Save it as alarm.wav in the assets folder
wavfile.write("assets/alarm.wav", sample_rate, audio_data)
print("Success! alarm.wav has been created in the assets folder.")