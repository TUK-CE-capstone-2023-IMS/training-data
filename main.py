from cvzone.PoseModule import PoseDetector
import cv2
import socket
import csv
from datetime import datetime

# file name
csv_name = "20240319_1.csv"

# Parameters
width, height = 1280, 720

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Pose Detector
detector = PoseDetector(staticMode=False,
                        modelComplexity=1,
                        smoothLandmarks=True,
                        enableSegmentation=False,
                        smoothSegmentation=True,
                        detectionCon=0.5,
                        trackCon=0.5)

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5051)

# CSV 파일에 데이터를 저장하는 함수
def save_to_csv(filename, data):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# 캡처한 각 프레임에서 x, y, z 좌표를 CSV 파일에 저장
frame_count = 0
while True:
    success, img = cap.read()
    frame_count += 1  # 프레임 번호 증가
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)

    count = 0
    if lmList:
        for lm in lmList:
            count += 1
            timestamp = datetime.now()
            data = [timestamp, frame_count, lm[0], height - lm[1], lm[2]]  # 타임스탬프, 프레임 번호, x, y, z 좌표
            save_to_csv(csv_name, data)

            # 소켓을 통해 서버로 전송
            sock.sendto(str.encode(str(data)), serverAddressPort)

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)