import sys
import os

from local_model.yolov5 import train

yolo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'local_model', 'yolov5')


def train_yolo():
    data_path = os.path.join(yolo_path, '..', '..', 'local_model', 'dataset.yaml')
    train.run(
        data=data_path,
        imgsz=640,
        batch_size=16,
        epochs=100,
        weights=os.path.join(yolo_path, 'yolov5s.pt'),  # Start with pre-trained YOLOv5 weights
        project=os.path.join(yolo_path, '..', '..', 'results'),
        name='brain_tumor_detector',
        exist_ok=True
    )


if __name__ == "__main__":
    train_yolo()
