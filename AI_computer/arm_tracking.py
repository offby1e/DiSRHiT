import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
from matplotlib import pyplot as plt
from gtts import gTTS
import pygame
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
hand_way="None"
mode="normal"
#[1,0,5](wrist)
# joint_list = [[4,3,2],[3,2,1],[2,1,0],[8,7,6],[7,6,5],[6,5,0],[12,11,10],[11,10,9],[10,9,0],[16,15,14],[15,14,13],[14,13,0],[20,19,18],[19,18,17],[18,17,0]]
joint_list=[]
def draw_finger_angles(image, results, joint_list):
    point=0
    # Loop through hands
    for hand in results.multi_hand_landmarks:
        #Loop through joint sets
        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y]) # First coord
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y]) # Second coord
            point=joint[1]
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y]) # Third coord

            radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)

            if angle > 180.0:
                angle = 360-angle
            angle=str(round(angle))
            print(angle,point)
            cv2.putText(image, angle, tuple(np.multiply(b, [640, 480]).astype(int)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 ,cv2.LINE_AA)
    return image
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    # if angle >180.0:
    #     angle = 360-angle
    angle=round(angle)
    return angle  
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1) as hands, mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose: 
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

        handway_result=results.multi_handedness
        if type(handway_result) is list:
            if "Right" in str(handway_result):
                hand_way="Right"
                print("Detected the right hand.")
                # Rendering results
                if results.multi_hand_landmarks:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),mp_drawing_styles.get_default_hand_connections_style())
                    draw_finger_angles(image, results, joint_list)
            elif "Left" in str(handway_result):
                hand_way="Left"
        text = "DiSRHiT"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0,0,0)
        thickness = 2
        cv2.putText(image,"2023_Geekble", (480, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        text = "Mode: {}".format(mode)
        cv2.putText(image,text,(480,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
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
        cv2.putText(image,text,(480,65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, font_color, 1)
        results = pose.process(image)
        try:
            landmarks = results.pose_landmarks.landmark
            #LEFT_SHOULDER
            a = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            b = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            c = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            angle=calculate_angle(a,b,c)      
            cv2.putText(image, str(round(angle,2)), tuple(np.multiply(b, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)  
            #LEFT_ELOBOW
            a = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            b = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            c = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            angle=calculate_angle(a,b,c)
            cv2.putText(image, str(round(angle,2)), tuple(np.multiply(b, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)  
            #LEFT_wrist
            a = np.array([hand.landmark[12].x, hand.landmark[12].y]) 
            b = np.array([hand.landmark[0].x, hand.landmark[0].y])
            c = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y])
            radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            angle=str(round(angle, 2))
            cv2.putText(image, angle, tuple(np.multiply(b, [640, 480]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 ,cv2.LINE_AA)
        except:
            pass
        mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            
            # landmark를 사용하여 해당 랜드마크를 그리는 코드
        cv2.imshow("DiSRHiT", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()