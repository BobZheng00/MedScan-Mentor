# import torch
import os
import subprocess

# Assumes yolov5 directory is in local_model
yolov5_detect = 'local_model/yolov5/detect.py'

def check_file_exist(path):
    if not os.path.exists(path):
        print(f'File {path} does not exist.')
        exit(1)

check_file_exist(yolov5_detect)
# type can be enum such as brain, lung, etc
def detect(image_name = 'gg (9).jpg', image_path = 'dataset/Val/Glioma/images', type = 'brain'):
    check_file_exist(image_path)
    # change the trained model path
    model_path = f'results/{type}_tumor_detector/weights/best.pt'
    check_file_exist(model_path)
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
    output_path = f'local_model/yolov5/runs/detect/exp/{image_name}'
    
    with open(output_path, 'rb') as file:
        byte_array = file.read()
        return byte_array

print(detect())