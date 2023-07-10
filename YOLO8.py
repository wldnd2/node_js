from ultralytics import YOLO
import cv2
from PIL import Image

model = YOLO('yolov8x.pt')

# folder_path = "./FruitsTest/"
# image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

image_files = ['./input.png']
results = []
for image_file in image_files:
    with Image.open(image_file) as img:
        img_size = img.size
    # res = model(image_file,conf=0.5)
    # source에 이미지 url주소도 가능
    res = model.predict(source=image_file, save=True, save_txt=True)
    resized_img = cv2.resize(res[0].plot(), (img.size[0], img.size[1]))
    cv2.imwrite("./result/YOLO8_temp.jpg", resized_img)