import torch
import subprocess

# Assumes yolov5 directory is parallel to predict.py
yolov5_detect = 'yolov5/detect.py'

# type can be enum such as brain, lung, etc
def detect(image_name, image_path, type):
    # change the path
    model_path = f'pre_trained/{type}_tumor_detector.pt'
    command = [
        'python', yolov5_detect,
        '--weights', model_path,
        '--conf', '0.4',
        '--source', image_path,
        '--save-txt',
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running YOLOv5 detection: {result.stderr}")
    
    # Process the result and return the detected objects as byte array format, can be turned into image
    output_path = f'yolov5/runs/detect/exp/{image_name}'
    with open(output_path, 'rb') as file:
        byte_array = file.read()
        return byte_array