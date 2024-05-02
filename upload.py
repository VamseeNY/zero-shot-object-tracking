import os
import json
import re
from pyrebase import pyrebase
# Firebase configuration
config=os.environ['firebase-creds']
# Initialize Pyrebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def parse_detection_data(filepath):
    with open(filepath, 'r') as file:
        data = file.readlines()
    frame_data = {"frame": None, "entities": []}
    for line in data:
        match = re.match(r"frame: (\d+); track: (\d+); class: ([\d.]+); bbox: ([\d.]+);", line)
        if match:
            frame, track, clazz, bbox = match.groups()
            if frame_data["frame"] is None:
                frame_data["frame"] = int(frame) + 1
            entity = {
                "track": int(track),
                "class": float(clazz),
                "bbox": float(bbox)
            }
            frame_data["entities"].append(entity)
    return frame_data

def upload_to_firebase(frame_data, folder_name,experiment_name):
    # Include the folder name in the database path
    db.child("detections").child(experiment_name    ).child(str(frame_data["frame"])).set(frame_data)
    print(f"Uploaded data for frame {frame_data['frame']} under folder {folder_name}")

def process_folder(folder_path):
    experiment_name=folder_path.split('\\')[2]
    folder_name = os.path.basename(folder_path)  # Get the folder name
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            frame_data = parse_detection_data(filepath)
            upload_to_firebase(frame_data, folder_name,experiment_name)


folder_path = "runs\detect\exp10\labels"
process_folder(folder_path)
