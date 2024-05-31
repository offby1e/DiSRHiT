# 🪬DiSRHiT
*Disaster Site Rescue hand Tracking robot*<br>
> 2023년 미래산업과학고등학교 메이커창작과 교내대회(일경험) - 인공지능 로봇 손

<img src="/md - 작품사진.jpeg" title="DiSRHiT"></img><br/>
[작동영상]: https://m.youtube.com/watch?v=zfUQFC6qfBE<br>
[Team]: Blackout_Retech🏴‍☠️<br>
[Maker]: 김강현(Software), 조윤혁(Leader & Electronic), 장한수(Engeenioring), 김선우(Engeenioring), 장혜원(Desgin)<br>
[Production period]: 2023.11 ~ 2023.12<br>
[Engeenioring Files]: None

## 작품 소개 및 Software

<strong><span style="font-size:big">🦾DiSRHiT - Disaster Site Rescue Hand Tracking Robot</span><strong>

> 지진과 같은 재난 현장에서구조 작업을 돕기위한 인공지능 로봇 손

**[제작 동기]**<br>
사람이 직접 재난 현장에서 접근하기 어련운 경우, 혹은 접근이 어려운 장소에서 사람의 섬세함이 필요한 경우에 현장에서 구조 작업에 도움이 되는 인공지능 모션 트랙킹 기술을 사용한 로봇을 개발함.<br>

## DiSRHiT Software 및 기술 설명
>모션 트랙킹을 활용하여 손을 인식하고 각 손가락 관절을 찾아 그 각도를 구해 로봇 손이 사용자의 손 모양과 똑같이 구사하도록 한다.

Raspberry PI를 사용하여 제어함.

**[모션 트랙킹 및 각도 구하기]**<br>
>손가락을 인식하고 각 손가락 관절 마다의 각도를 구한다.

1. Hand Motion Tracking<br>
	(Mediapipe 손가락 랜드마크 사진)
	- Python의 Mediapipe 라이브러리를 사용하여 손을 인식하고 트랙킹한다.
	- 로봇 손의 각 모터에 해당하는 관절의 랜드마크를 지정하여 해당 랜드마크들을 인식하게 하고 해당	하는 위치에 Opencv 라이브러리를 사용하여 점(spot)을 찍게 함.
	- 

2. Find Finger Joint angle
	- python Numpy 라이브러리와 Opencv 라이브러리 사용하였다.
	- 3개의 랜드마크를 각도를 구하는 메서드의 인자로 넣어주면 백터를 사용하여 가운데 랜드마크의 		   각도를 계산
	- 카메라 각도에 따라 각도의 정확도가 크게 떨어질 수 있음.(개선 방법 연구 중..)

**[서보모터 동시 제어]**<br>
>각 손가락의 관절을 미세하게 조정하기 위해 인터넷에 널리 알려진 실로 제어하는 방법이 아닌 서보모터를 사용하여 각 관절을 제어하였습니다.

1. 손가락 관절(모터) 위치
	(그림)
	[전자]: 총 12개의 모터를 제어하기 위하여 저희 서보모터 다채널 드라이버(PCA9685)를 사용하
        여 제어하였습니다.

2. Thread를 사용한 모터 동시 제어
	Thread를 사용하는 이유는....GPIO를 통해 모터를 제어할 때 보통은 한번에 하나의 모터만 제어할 	수 있다.(이는 컴퓨터가 하나의 프로세스에서 하나의 작업만 수행 할 수 있기 때문이다.) 해서 동시에 	12개의 모터를 제어하기 위하여 사용한다.<br>
	[Thread 개념]: https://www.yalco.kr/14_process_thread/

	- python의 threading 라이브러리를 사용하여 드라이버의 각 채널마다 연결 되어 있는 모터를 제	어 함.
	- 각 채널을 편리하게 제어하기 위해 Class(2.1)를 사용하여 다양한 제어 메서드를 제작 후 각 인스	턴스	 (즉, 채널 제어 메서드)의 모터 제어 메서드를 thread에 넣어줌. 

**[인공지능 PC 와 로봇 손(Raspberry Pi) 통신]**<br>
Socket 통신이란?..
> 🔖네트워크상에서 가동되는 두 개의 프로그램 간 양방향 통신의 하나의 엔드포인트

소켓은 TCP/IP 기반 네트워크 통신에서 데이터 송수신의 마지막 접점을 이야기한다. 즉, 소켓은 서버와 클라이언트 간 데이터를 주고받는 양방향 연결 지향성 통신.
소켓을 사용하기 위해서는 클라이언트와 서버 소켓으로 각각 구분되고, 통신을 하기 위해 IP주소와 포트번호를 이용한다.
- Python의 Pysocket 라이브러리 사용하였다.
- Bluetooth 모듈을 사용항 블루투스 통신을 시도하였지만 보낼 수 있는 데이터 비트 수 제한과 속도 제한으로 인하여 Socket 통신을 사용하였다.


## DiSRHiT 조작 메뉴얼

**[라즈베리파이 접속 command - ssh]**
> ssh rkdgus0810@[ip address(inet)] -p 22

*접속하면 현재 띄워져 있는 창은 라즈베리파이 cmd임.

**[directory 이동]**
> cd Desktop
> cd AI-Hand

**[가상환경 활성화]**
> source bin/activate

*입력 라인 맨 앞에 “(AI-Hand)" 뜨면 성공!!

**[socket통신 주소 확인]**
1. ip 주소 조회
> ifconfig

2. vscode 에서 main.py 파일 열고 Host 변수 값(ip주소)과 1번을 통해 조회한 ip주소가 같은지 확인

**[라즈베리파이 코드 실행]**
1. 초록 레버 on
2. 코드 실행
> python main. py

*초기값 log 뜨고 server 켜질 때까지 기다리기
(서버가 시작되면 ip주소랑 port번호 등이 뜸)

**[로컬 컴퓨터(AI) 코드 실행]**
<br>vscode 터미널에서 다음 명령어 실행
*vscode 터미널 열기ctrl + ~(단, shift x)
> python main.py

*통신이 시작됬다고 뜨면 성공!(초록색 글자로 뜸)

**[참고 및 주의 사항!!]**<br>
*혹시 만약에 작동 실패하면 [소켓 통심 주소 확인] 다시 한 번해보기!!
*메뉴얼 순서 중요!!
*대소문자 중요!!
