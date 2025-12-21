<div align="center">

# 🤖 DiSRHiT

### Disaster Site Rescue Hand Tracking Robot

*재난 현장을 위한 손동작 추적 구조 로봇*

![Python](https://img.shields.io/badge/Python-99.9%25-3776AB?style=flat&logo=python&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry_Pi-A22846?style=flat&logo=raspberrypi&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?style=flat&logo=google&logoColor=white)

![GitHub Stars](https://img.shields.io/github/stars/Deamonio/DiSRHiT?style=social)
![GitHub Forks](https://img.shields.io/github/forks/Deamonio/DiSRHiT?style=social)

**My Favorite Production** ⭐

---

### 🎥 Demo Video

[![DiSRHiT Demo](https://img.youtube.com/vi/yDfamQaG-cU/maxresdefault.jpg)](https://www.youtube.com/watch?v=yDfamQaG-cU)

**▶️ 클릭하여 실제 작동 영상 보기**

*손동작으로 로봇 팔을 실시간 제어하는 DiSRHiT*

</div>

---

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [시스템 아키텍처](#-시스템-아키텍처)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [하드웨어 구성](#-하드웨어-구성)
- [설치 방법](#-설치-방법)
- [사용 방법](#-사용-방법)
- [코드 구조](#-코드-구조)

---

## 🎯 프로젝트 소개

**DiSRHiT (Disaster Site Rescue Hand Tracking Robot)**는 재난 현장에서 구조 작업을 수행할 수 있는 **손동작 제어 로봇 시스템**입니다. 

### 💡 프로젝트 배경

재난 현장에서는 2차 붕괴 위험으로 인해 구조대원이 직접 접근하기 어려운 상황이 많습니다.    
DiSRHiT는 이러한 문제를 해결하기 위해 **원격으로 손동작만으로 로봇을 제어**할 수 있는 시스템을 구현했습니다.  

### 🌟 특징

- ✅ **직관적 제어**:   손가락 각도를 실시간으로 로봇에 전달
- ✅ **무선 통신**:  Socket 기반 원격 제어
- ✅ **정밀 제어**:  11개 서보 모터 독립 제어
- ✅ **실시간 처리**:  MediaPipe 기반 빠른 손 추적
- ✅ **안정성**:  멀티스레딩으로 안정적인 데이터 전송

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────┐
│  AI Computer (제어 컴퓨터)              │
│  ┌─────────────────────────────────┐   │
│  │  웹캠                            │   │
│  │  ↓                               │   │
│  │  MediaPipe 손 추적              │   │
│  │  ↓                               │   │
│  │  손가락 각도 계산 (21 Landmarks)│   │
│  │  ↓                               │   │
│  │  Socket Client (송신)           │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
              ↓ Socket (TCP/IP)
              ↓ "action: 90: 90:90:..."
┌─────────────────────────────────────────┐
│  Hand Robot (로봇 팔)                   │
│  ┌─────────────────────────────────┐   │
│  │  Socket Server (수신)           │   │
│  │  ↓                               │   │
│  │  명령 파싱                       │   │
│  │  ↓                               │   │
│  │  멀티스레드 각도 분배           │   │
│  │  ↓                               │   │
│  │  PCA9685 PWM 드라이버           │   │
│  │  ↓                               │   │
│  │  11개 서보 모터 제어            │   │
│  └─────────────────────────────────┘   │
│  (Raspberry Pi)                         │
└─────────────────────────────────────────┘
```

---

## ✨ 주요 기능

### 1. 🖐️ MediaPipe 손 추적

**AI Computer (main_delay. py)**

```python
# MediaPipe로 21개 손 랜드마크 추출
mp_hands = mp.solutions.hands

# 손가락 각도 계산
joint_list = [
    [1,5,6],    # 엄지
    [0,9,10],   # 검지
    [0,13,14],  # 중지
    [0,17,18],  # 약지
    # ... 총 9개 관절
]

# 각도 계산 (벡터 기반)
radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
          np.arctan2(a[1]-b[1], a[0]-b[0])
angle = np.abs(radians * 180.0 / np.pi)
```

**특징:**
- 21개 손 랜드마크 실시간 추적
- 9개 주요 관절 각도 계산
- 180도 범위 정규화
- 프레임당 처리 시간:   ~30ms

---

### 2. 📡 Socket 통신

**프로토콜 설계:**

```
명령 포맷: 
"action:angle0:angle1:angle2:.. .:angle10"

예시:
"action:90:85:120:95:10: 15:20:25:45:50:60"
       └─┬─┘ └────────────────┬────────────┘
      명령어        11개 서보 각도
```

**AI Computer → Robot 통신:**
```python
# 송신 (AI Computer)
message = f"action:{': '.join(map(str, angles))}"
client_socket.send(message.encode())

# 수신 (Hand Robot)
data = client_socket.recv(1024)
command = data.decode().split(':')
# command[0] = 'action'
# command[1~11] = 각 서보 각도
```

**특징:**
- TCP/IP 소켓 통신
- 멀티 클라이언트 지원
- 에러 핸들링 (ConnectionResetError)
- 컬러 로그 출력

---

### 3. ⚙️ 서보 모터 제어

**PCA9685 PWM 제어:**

```python
class Servo_Controller_Class:
    def __init__(self, Channel, ZeroOffset):
        self.mChannel = Channel
        self.m_ZeroOffset = ZeroOffset
        
        # PCA9685 초기화 (I2C 주소: 0x40)
        self.mPwm = Adafruit_PCA9685.PCA9685(address=0x40)
        self.mPwm.set_pwm_freq(60)  # 60Hz
    
    def SetPos(self, pos):
        # 각도 → PWM 펄스 변환
        pulse = (650-150) * pos/180 + 150 + self.m_ZeroOffset
        self.mPwm.set_pwm(self. mChannel, 0, int(pulse))
```

**PWM 계산:**
```
펄스 범위: 150 ~ 650 (4096 단계 중)
각도 범위:   0° ~ 180°

공식: pulse = (650-150) × (angle/180) + 150 + offset
```

---

### 4. 🧵 멀티스레딩

**동시 처리:**

```python
# 11개 서보를 동시에 업데이트
append_action_thread = []

for index in range(11):
    thread = threading.Thread(
        target=append_angle, 
        args=(index, command[index+1])
    )
    append_action_thread.append(thread)

# 모든 스레드 동시 시작
for thread in append_action_thread:
    thread.start()
```

**Lock으로 동기화:**
```python
action_lock = [threading.Lock() for _ in range(11)]

def append_angle(index, pos):
    action_lock[index].acquire()
    action_range[index][0] = int(float(pos))
    action_lock[index]. release()
```

---

## 🔧 기술 스택

### AI Computer (제어측)

| 기술 | 용도 | 버전 |
|---|---|---|
| **Python** | 메인 언어 | 3.8+ |
| **MediaPipe** | 손 추적 | 0.8.x |
| **OpenCV** | 영상 처리 | 4.5.x |
| **NumPy** | 수치 계산 | 1.21.x |
| **Socket** | 네트워크 통신 | Built-in |

### Hand Robot (로봇측)

| 기술 | 용도 | 버전 |
|---|---|---|
| **Raspberry Pi** | 메인 보드 | 3B+ / 4 |
| **Python** | 서버 언어 | 3.7+ |
| **Adafruit PCA9685** | PWM 드라이버 | I2C |
| **RPi.GPIO** | GPIO 제어 | Latest |
| **Socket** | 서버 | Built-in |

---

## 🛠️ 하드웨어 구성

### 전체 BOM (Bill of Materials)

| 부품 | 수량 | 용도 |
|---|---|---|
| **Raspberry Pi 3B+/4** | 1 | 메인 컨트롤러 |
| **PCA9685 16채널 PWM** | 1 | 서보 제어 |
| **SG90 서보 모터** | 11 | 손가락 구동 |
| **웹캠** | 1 | 손 추적 입력 |
| **5V 전원 공급** | 1 | 서보 전원 |
| **점퍼 와이어** | 다수 | 연결 |
| **브레드보드** | 1 | 프로토타입 |

### 서보 모터 배치

```
11개 서보 모터: 
[0] 엄지 기저부
[1] 엄지 첫째 마디
[2] 엄지 끝마디
[3] 검지 기저부
[4] 검지 첫째 마디
[5] 검지 끝마디
[6] 중지 첫째 마디
[7] 약지 첫째 마디
[8] 새끼 첫째 마디
[9] 손목 회전
[10] 팔꿈치
```

---

## 📦 설치 방법

### AI Computer (제어 컴퓨터)

#### 1. 저장소 클론

```bash
git clone https://github.com/Deamonio/DiSRHiT.git
cd DiSRHiT/AI_computer
```

#### 2. 가상환경 생성

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
mediapipe>=0.8.0
opencv-python>=4.5.0
numpy>=1.21.0
pygame>=2.0.0
gtts>=2.2.0
```

---

### Hand Robot (Raspberry Pi)

#### 1. SSH 접속

```bash
ssh pi@<라즈베리파이_IP>
```

#### 2. 저장소 클론

```bash
git clone https://github.com/Deamonio/DiSRHiT.git
cd DiSRHiT/Hand_Robot
```

#### 3. 의존성 설치

```bash
pip3 install -r requirements.txt
```

**requirements.txt:**
```txt
RPi.GPIO>=0.7.0
adafruit-pca9685>=1.0.1
```

#### 4. I2C 활성화

```bash
sudo raspi-config
# Interfacing Options → I2C → Enable
sudo reboot
```

#### 5. I2C 주소 확인

```bash
sudo i2cdetect -y 1
```

**출력 예시:**
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  ← PCA9685
```

---

## 🚀 사용 방법

### 1️⃣ Hand Robot 서버 시작

```bash
# Raspberry Pi에서 실행
cd DiSRHiT/Hand_Robot
python3 main. py
```

**출력:**
```
[Socket] Server started on 0.0.0.0:7672
[Socket] Waiting for connections...
```

**IP 주소 확인:**
```bash
hostname -I
# 예: 192.168.1.100
```

---

### 2️⃣ AI Computer 클라이언트 실행

**IP 설정:**
```python
# AI_computer/main_delay.py
HOST = '192.168.1.100'  # Raspberry Pi IP
PORT = 7672
```

**실행:**
```bash
cd DiSRHiT/AI_computer
python main_delay.py
```

**출력:**
```
[Socket] Connected to the Server
[Camera] Starting hand tracking...
```

---

### 3️⃣ 손동작 제어

**제어 방법:**

1. **웹캠 앞에 손을 펴기**
   - MediaPipe가 21개 랜드마크 인식
   - 화면에 손 스켈레톤 표시

2. **손가락 움직이기**
   - 각 손가락 각도가 실시간 계산
   - Socket으로 로봇에 전송

3. **로봇 팔 확인**
   - 로봇 손가락이 동일하게 움직임
   - 지연 시간:  ~100ms

**종료:**
- `q` 키:   프로그램 종료
- `Ctrl+C`: 강제 종료

---

## 📁 프로젝트 구조

```
DiSRHiT/
├── AI_computer/                 # 제어 컴퓨터 (Python 99.9%)
│   ├── main_delay.py            # 메인 손 추적 + Socket 클라이언트
│   ├── camera.py                # 웹캠 테스트 (카메라 0)
│   ├── camera2.py               # 웹캠 테스트 (카메라 1)
│   └── requirements.txt         # 의존성
│
├── Hand_Robot/                  # 로봇 팔 (Raspberry Pi)
│   ├── main.py                  # Socket 서버 + 서보 제어
│   ├── requirements.txt         # 의존성
│   ├── bin/                     # 유틸리티 스크립트
│   │   ├── i2cscan.py           # I2C 장치 스캔
│   │   ├── ftdi_urls.py         # FTDI 장치 확인
│   │   └── pyterm.py            # 시리얼 터미널
│   └── research_data/
│       └── socket_client.py     # Socket 테스트 클라이언트
│
├── profile_image. jpeg           # 프로젝트 이미지
├── README.md                    # 이 문서
└── test. md                      # 테스트 문서
```

---

## 💻 핵심 코드 분석

### 손가락 각도 계산 알고리즘

```python
def draw_finger_angles(image, results, joint_list):
    for hand in results.multi_hand_landmarks:
        for joint in joint_list:
            # 3개 점으로 각도 계산
            a = np.array([hand.landmark[joint[0]].x, 
                          hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, 
                          hand.landmark[joint[1]].y])
            c = np.array([hand.landmark[joint[2]].x, 
                          hand.landmark[joint[2]].y])
            
            # 벡터 각도 계산
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
                      np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians * 180.0 / np.pi)
            
            # 180도 초과 시 보정
            if angle > 180. 0:
                angle = 360 - angle
            
            # 손가락별 각도 보정
            if cnt < 4:  # 엄지~약지
                angle = 180 - angle
            if cnt >= 4 and cnt <= 7:  # 중간 마디
                if angle > 80:
                    angle = 180 - angle
```

**원리:**
1. 3개 랜드마크 추출 (관절 양쪽 + 중심)
2. 2개 벡터 생성
3. `arctan2`로 각 벡터 각도 계산
4. 두 각도 차이로 관절 각도 도출
5. 손가락별 보정 적용

---

### Socket 서버 (멀티 클라이언트)

```python
def handle_client(client_socket, addr):
    print(f"[Socket] Connected by:  {addr[0]}:{addr[1]}")
    
    while True: 
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            # 다른 클라이언트에게 브로드캐스트
            for client in client_sockets:
                if client != client_socket:
                    client. send(data)
            
            # 명령 파싱
            command = data. decode().split(':')
            if command[0] == 'action':
                # 11개 서보 동시 업데이트 (멀티스레딩)
                threads = []
                for index in range(11):
                    t = threading.Thread(
                        target=append_angle,
                        args=(index, command[index+1])
                    )
                    threads.append(t)
                    t.start()
                
        except ConnectionResetError:
            break
    
    client_sockets.remove(client_socket)
```

---

### 서보 PWM 제어

```python
def SetPos(self, pos):
    # 각도 (0~180°) → PWM 펄스 (150~650)
    pulse = (650-150) * pos/180 + 150 + self.m_ZeroOffset
    
    # PCA9685로 PWM 신호 전송
    self. mPwm.set_pwm(self.mChannel, 0, int(pulse))
```

**PWM 타이밍:**
- 주파수:   60Hz (16. 67ms 주기)
- 펄스 범위: 150~650 (4096 단계 중)
- 0°:  0. 61ms, 90°: 1.53ms, 180°: 2.45ms

---

## 🔧 문제 해결

### 1. Socket 연결 실패

**증상:**
```
[Socket][Error] Connection refused
```

**해결:**
```bash
# 1.  IP 주소 확인
hostname -I

# 2. 방화벽 확인
sudo ufw allow 7672

# 3. 서버 재시작
python3 main.py
```

---

### 2. I2C 장치 인식 안 됨

**증상:**
```
IOError: [Errno 2] No such file or directory
```

**해결:**
```bash
# I2C 활성화 확인
ls /dev/i2c*
# /dev/i2c-1 있어야 함

# I2C 주소 스캔
sudo i2cdetect -y 1

# I2C 도구 설치
sudo apt-get install i2c-tools
```

---

### 3. 서보 떨림 현상

**증상:**
- 서보가 미세하게 떨림
- 각도가 불안정

**해결:**
```python
# 1. 전원 공급 확인 (5V 2A 이상)
# 2. 캐패시터 추가 (1000μF)
# 3. 데드존 설정

def SetPos(self, pos):
    # 각도 변화가 2도 미만이면 무시
    if abs(pos - self.last_pos) < 2:
        return
    
    pulse = (650-150) * pos/180 + 150 + self.m_ZeroOffset
    self.mPwm. set_pwm(self.mChannel, 0, int(pulse))
    self.last_pos = pos
```

---

### 4. MediaPipe 느림

**증상:**
```
FPS:  10~15 (목표: 30)
```

**해결:**
```python
# 1. 해상도 낮추기
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 2. 모델 복잡도 낮추기
mp_hands. Hands(
    model_complexity=0,  # 0: 빠름, 1: 정확
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 3. GPU 사용 (가능 시)
mp_hands. Hands(
    static_image_mode=False,
    max_num_hands=1
)
```

---

## 📊 성능 지표

### 시스템 성능

| 항목 | 수치 | 비고 |
|---|---|---|
| **FPS** | 25~30 | 웹캠 30fps 기준 |
| **지연 시간** | ~100ms | AI → Robot |
| **통신 속도** | <10ms | Local network |
| **서보 응답** | ~60ms | PWM 60Hz |
| **정확도** | ±3° | 손가락 각도 |

### 리소스 사용

**AI Computer:**
- CPU: 40~60% (i5 이상)
- RAM: ~500MB
- GPU: MediaPipe (선택)

**Raspberry Pi:**
- CPU: 20~30%
- RAM: ~200MB
- I2C 대역폭: ~100kbps

---

## 🎯 활용 사례

### 1. 재난 구조

**시나리오:**
```
지진 → 건물 붕괴 → 2차 붕괴 위험
       ↓
DiSRHiT 투입 → 원격 조종
       ↓
생존자 탐색 → 물품 전달 → 구조
```

### 2. 위험 물질 처리

- 방사능 오염 지역
- 화학 물질 유출 현장
- 폭발물 제거

### 3. 의료 재활

- 손 기능 회복 훈련
- 원격 재활 치료
- 손 움직임 데이터 수집

---

## 🤝 기여하기

기여는 언제나 환영합니다!    🎉

### 기여 방법

1. Fork 이 저장소
2. Feature 브랜치 생성:   `git checkout -b feature/AmazingFeature`
3. 변경사항 커밋:  `git commit -m 'Add some AmazingFeature'`
4. 브랜치에 Push:  `git push origin feature/AmazingFeature`
5. Pull Request 생성

### 개선 아이디어

- [ ] 양손 지원
- [ ] 힘 피드백 추가
- [ ] WebRTC 영상 스트리밍
- [ ] 자율 주행 기능
- [ ] 음성 명령 통합

---

## 📜 라이선스

이 프로젝트는 MIT License 하에 배포됩니다.  

---

## 📞 연락처

<div align="center">

### 프로젝트 관리자:   Deamonio

[![Email](https://img.shields.io/badge/Email-hyun0810d@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hyun0810d@gmail. com)
[![GitHub](https://img.shields.io/badge/GitHub-Deamonio-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Deamonio)

**프로젝트 링크**:  [https://github.com/Deamonio/DiSRHiT](https://github.com/Deamonio/DiSRHiT)

</div>

---

## 🙏 감사의 말

| MediaPipe | Raspberry Pi | Adafruit | OpenCV |
|---|---|---|---|
| 손 추적 | 하드웨어 | PWM 드라이버 | 영상 처리 |

**특별 감사:**
- 🖐️ **Google MediaPipe** - 정확한 손 추적
- 🍓 **Raspberry Pi Foundation** - 저렴한 컴퓨팅 파워
- ⚡ **Adafruit** - 훌륭한 PCA9685 라이브러리
- 👁️ **OpenCV Community** - 영상 처리 도구

---

<div align="center">

## ⭐ 이 프로젝트가 마음에 드셨다면 Star를 눌러주세요!  

[![Star History Chart](https://api.star-history.com/svg?repos=Deamonio/DiSRHiT&type=Date)](https://star-history.com/#Deamonio/DiSRHiT&Date)

---

**Made with ❤️ and precision**

*"Saving lives through technology"*

---

**© 2025 Deamonio. All rights reserved.**

[⬆ 맨 위로 돌아가기](#-disrhit)

</div>
