import os
from pathlib import Path
import torch

# Load your YOLOv9 model (adjust the path and model loading as needed)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/jorge/Desktop/masterModel/YOLO/yolov9/runs/train/exp/weights/best.pt', source='local')

def process_images(root_data_folder):
    # Traverse through all subdirectories and files in the root data folder
    for root, _, files in os.walk(root_data_folder):
        for file in files:
            if file.endswith('.jpg'):
                image_path = os.path.join(root, file)
                output_path = os.path.splitext(image_path)[0] + '_detect.txt'

                # Perform object detection on the image
                results = model(image_path)

                # Save the prediction bounding boxes to the output file
                with open(output_path, 'w') as f:
                    for *box, conf, cls in results.xyxy[0].tolist():
                        f.write(f"{int(cls)} {conf} {' '.join(map(str, map(int, box)))}\n")

if __name__ == "__main__":
    root_data_folder = "/root_data_folder"  # Set your root data folder path here
    process_images(root_data_folder)
