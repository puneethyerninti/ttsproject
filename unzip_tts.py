import zipfile
import os

# Path to the zip file
zip_path = "tts_batch.zip"

# Destination folder
dest_folder = "tts_batch"

# Create folder if it doesn't exist
os.makedirs(dest_folder, exist_ok=True)

# Unzip the contents
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(dest_folder)

print(f"All files extracted to '{dest_folder}'")
