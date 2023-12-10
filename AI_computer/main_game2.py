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
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
hand_way="None"
mode="tracking"
send_angle=[]
temp_arr=[]
joint_list1 = [[1,5,6],[0,9,10],[0,13,14],[0,17,18],[7,6,5],[11,10,9],[15,14,13],[19,18,17]]
joint_list2 = [[0,1,2],[1,2,3],[2,3,4]]
skip_send=0

def draw_finger_angles1(image, results, joint_list):
    cnt=0
    # Loop through hands
    for hand in results.multi_hand_landmarks:
        global send_angle
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
                if angle>80:
                    angle=((180-angle)/100)*90
                elif angle<80:
                    angle=90
                angle=90-angle
                if angle<10:
                    angle=10
            angle=str(round(angle, 2))
            send_angle.append(angle)
            cv2.putText(image, angle, tuple(np.multiply(b, [640, 480]).astype(int)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 ,cv2.LINE_AA)
            cnt+=1
    return image

def draw_finger_angles2(image, results, joint_list):
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

            if angle>180:
                angle=360-angle
            angle=180-angle
            if cnt==1:
                if angle>60:
                    angle=60
                if angle<=60:
                    angle=(angle/60)*90 
            angle=str(round(angle, 2))
            send_angle.append(angle)
            cv2.putText(image, angle, tuple(np.multiply(b, [640, 480]).astype(int)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 ,cv2.LINE_AA)
            cnt+=1
    return image

def rendring(angle_index,results,image,joint_list):
    global mp_drawing_styles,mp_hands
    if results1.multi_hand_landmarks:
        for num, hand in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
        if angle_index==1:
            draw_finger_angles1(image, results, joint_list)
        if angle_index==2:
            draw_finger_angles2(image, results, joint_list)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5,max_num_hands=1) as hands: 
    while cap1.isOpened() and cap1.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        # BGR 2 RGB
        image1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        
        # Flip on horizontal
        image1 = cv2.flip(image1, 1)
        image2 = cv2.flip(image2, 1)
        
        # Set flag
        image1.flags.writeable = False
        image1.flags.writeable = False
        # Detections
        results1 = hands.process(image1)
        results2 = hands.process(image2)

        
        # Set flag to true
        image1.flags.writeable = True
        image2.flags.writeable = True
        
        # RGB 2 BGR
        image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
        image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR)
        
        # Detections
        if mode=="tracking":
            handway_result1=results1.multi_handedness
            if type(handway_result1) is list:
                if "Right" in str(handway_result1):
                    hand_way="Right"
                    rendring(1,results1,image1,joint_list1)
                elif "Left" in str(handway_result1):
                    hand_way="Left"
            handway_result2=results2.multi_handedness
            if type(handway_result2) is list:
                if "Right" in str(handway_result2):
                    hand_way="Right"
                    rendring(2,results2,image2,joint_list2)
                elif "Left" in str(handway_result2):
                    hand_way="Left"


        if skip_send%3==0:
            try:
                message=f"action:{send_angle[0]}:{send_angle[1]}:{send_angle[2]}:{send_angle[3]}:{send_angle[4]}:{send_angle[5]}:{send_angle[6]}:{send_angle[7]}:{send_angle[8]}:{send_angle[9]}:{send_angle[10]}"
                client_socket.send(message.encode())
                print(f"{Colors.CYAN}[Detected the Hand]{Colors.END} {Colors.WHITE}angle: {send_angle}{Colors.END}")
                send_angle=[]
            except:
                pass
        skip_send+=1
        text = "DiSRHiT"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0,0,0)
        thickness = 2
        cv2.putText(image1,"DiSRHiT", (540, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(image2,"DiSRHiT", (540, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        text = "Mode: {}".format(mode)
        cv2.putText(image1,text,(540,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        cv2.putText(image2,text,(540,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
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
        cv2.putText(image1,text,(540,65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, font_color, 1)
        cv2.putText(image2,text,(540,65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, font_color, 1)
        cv2.imshow("DiSRHiT1", image1)
        cv2.imshow("DiSRHiT2", image2)

        if cv2.waitKey(10) & 0xFF == ord('g'):
            mode="game"
        if mode=="game" and cv2.waitKey(10) & 0xFF == ord('s'):
            pass
        if cv2.waitKey(10) & 0xFF == ord('t'):
            mode="tracking"
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
client_socket.close()