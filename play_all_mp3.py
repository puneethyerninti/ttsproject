import os
from playsound import playsound  # pip install playsound==1.2.2

# Path to the folder where MP3s are extracted
folder = "tts_batch"

# List all MP3 files and sort them
mp3_files = sorted(f for f in os.listdir(folder) if f.endswith(".mp3"))

# Play each MP3 one by one
for mp3 in mp3_files:
    path = os.path.join(folder, mp3)
    print(f"Playing {mp3}...")
    playsound(path)

print("All MP3s played!")
