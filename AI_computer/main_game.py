import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
from matplotlib import pyplot as plt
from gtts import gTTS
import pygame
import time
import socket
import threading

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    END = '\033[0m'

HOST = '10.244.84.105'  # 서버에 출력되는 IP를 입력하세요
PORT = 7672

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
except ConnectionError as e:
    print(f"{Colors.YELLOW}[Socket]{Colors.END}{Colors.RED}[Error] {e}{Colors.END}")
    exit()

def recv_data(client_socket):
    global mode
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Received: {Colors.END}{Colors.WHITE}{repr(data.decode())}{Colors.END}")
        except ConnectionError as e:
            print(f"{Colors.YELLOW}[Socket]{Colors.END}{Colors.RED}[Error: receiving data]: {e}{Colors.END}")
            break

recv_thread = threading.Thread(target=recv_data, args=(client_socket,))
recv_thread.start()
print(f'{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Connected to the Server{Colors.END}')

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
hand_way="None"
mode="tracking"
send_angle=[]
temp_arr=[]
joint_list = [[1,5,6],[0,9,10],[0,13,14],[0,17,18],[7,6,5],[11,10,9],[15,14,13],[19,18,17],[1,2,3],[2,3,4]]
skip_send=0

def draw_finger_angles(image, results, joint_list):
    global skip_send
    cnt=0
    # Loop through hands
    for hand in results.multi_hand_landmarks:
        global send_angle,temp_arr
        temp_arr=[]
        #Loop through joint sets
        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y]) # First coord
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y]) # Second coord
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y]) # Third coord

            radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)

            if angle > 180.0:
                angle = 360-angle
            if cnt<4:
                angle=180-angle
                if angle>90:
                    angle=90
            if cnt>=4 and cnt<=7:
                if angle>90:
                    angle=((180-angle)/90)*90
                elif angle<90:
                    angle=90
                angle=90-angle
                if angle<10:
                    angle=10
                pass
            if cnt==8:
                angle=180-angle
                if angle>30:
                    angle=30
                if angle<=50:
                    angle=(angle/30)*90
            if cnt==9:
                angle=180-angle
                if angle>90:
                    angle=90
                angle=90-angle
            angle=str(round(angle, 2))
            temp_arr.append(angle)
            cv2.putText(image, angle, tuple(np.multiply(b, [640, 480]).astype(int)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 ,cv2.LINE_AA)
            cnt+=1
        if skip_send%3==0:
            send_angle=temp_arr
            message=f"action:{send_angle[0]}:{send_angle[1]}:{send_angle[2]}:{send_angle[3]}:{send_angle[4]}:{send_angle[5]}:{send_angle[6]}:{send_angle[7]}:{send_angle[8]}:{send_angle[9]}:0"
            client_socket.send(message.encode())
            print(f"{Colors.CYAN}[Detected the Hand]{Colors.END} {Colors.WHITE}angle: {send_angle}{Colors.END}")
        skip_send+=1
    return image

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5,max_num_hands=1) as hands: 
    while cap.isOpened():
        ret, frame = cap.read()
        
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Flip on horizontal
        image = cv2.flip(image, 1)
        
        # Set flag
        image.flags.writeable = False
        # Detections
        results = hands.process(image)
        
        # Set flag to true
        image.flags.writeable = True
        
        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Detections
        if mode=="tracking":
            handway_result=results.multi_handedness
            if type(handway_result) is list:
                if "Right" in str(handway_result):
                    hand_way="Right"
                    # Rendering results
                    if results.multi_hand_landmarks:
                        for num, hand in enumerate(results.multi_hand_landmarks):
                            mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
                        draw_finger_angles(image, results, joint_list)
                elif "Left" in str(handway_result):
                    hand_way="Left"
        if mode=="game":
            image.flags.writeable = False
            results = hands.process(image)

            image.flags.writeable = True
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_height, image_width, _ = image.shape

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 엄지를 제외한 나머지 4개 손가락의 마디 위치 관계를 확인하여 플래그 변수를 설정합니다. 손가락을 일자로 편 상태인지 확인합니다.
                    thumb_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height:
                                thumb_finger_state = 1

                    index_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height:
                                index_finger_state = 1

                    middle_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height:
                                middle_finger_state = 1

                    ring_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height:
                                ring_finger_state = 1

                    pinky_finger_state = 0
                    if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height:
                                pinky_finger_state = 1

                
                    text = ""
                    if thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                        text = "보"
                    elif thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "가위"
                    elif   index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                        text = "주먹"

                    print(text)

                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
                

        text = "DiSRHiT"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0,0,0)
        thickness = 2
        cv2.putText(image,"DiSRHiT", (540, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        text = "Mode: {}".format(mode)
        cv2.putText(image,text,(540,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        if hand_way=="Right":
            text = "Hand: Right"
            font_color=(255,0,0)
        elif hand_way=="Left":
            text="Hand: Left"
            font_color=(0,0,255)
        else:
            text="Hand: None"
            font_color=(255,255,255)
        hand_way="None"
        cv2.putText(image,text,(540,65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, font_color, 1)
        cv2.imshow("DiSRHiT", image)

        if cv2.waitKey(10) & 0xFF == ord('g'):
            mode="game"
        if mode=="game" and cv2.waitKey(10) & 0xFF == ord('s'):
            pass
        if cv2.waitKey(10) & 0xFF == ord('t'):
            mode="tracking"
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
client_socket.close()