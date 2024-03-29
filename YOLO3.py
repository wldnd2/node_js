import json
import sys
import cv2
import numpy as np
import time

def dataPreprocess(label):
    temp = dict()
    temp[label.split(":")[0]] = float(label.split(":")[1])
    return temp

def detectAndDisplay(frame, min_confidence, classes, output_layers, colors):
    # result = ["class: accuracy"]
    result = []
    start_time = time.time()
    img = cv2.resize(frame, None, fx=0.8, fy=0.8)
    height, width, channels = img.shape
    #cv2.imshow("Original Image", img)

    #-- 창 크기 설정
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    #-- 탐지한 객체의 클래스 예측 
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > min_confidence:
                # 탐지한 객체 박싱
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
    font = cv2.FONT_HERSHEY_DUPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = "{}: {:.2f}".format(classes[class_ids[i]], confidences[i]*100)
            # print(i, label)
            result.append(dataPreprocess(label))
            color = colors[i] #-- 경계 상자 컬러 설정 / 단일 생상 사용시 (255,255,255)사용(B,G,R)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
    end_time = time.time()
    process_time = end_time - start_time
    # print("=== A frame took {:.3f} seconds".format(process_time))
    cv2.imwrite("./result/YOLO3.jpg", img)
    return result

#-- yolo 포맷 및 클래스명 불러오기
model_file = './yolo3/yolov3.weights' #-- 본인 개발 환경에 맞게 변경할 것
config_file = './yolo3/yolov3.cfg' #-- 본인 개발 환경에 맞게 변경할 것
net = cv2.dnn.readNet(model_file, config_file)

#-- 클래스(names파일) 오픈 / 본인 개발 환경에 맞게 변경할 것
classes = []
with open("./yolo3/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# 이미지 경로 설정
image_path = './input.png'
min_confidence = 0.5 # 최소 신뢰도 임계값 설정
# 이미지 읽기
frame = cv2.imread(image_path)

my_list = detectAndDisplay(frame, min_confidence, classes, output_layers, colors)
print(json.dumps(my_list), end="")
sys.stdout.flush()
