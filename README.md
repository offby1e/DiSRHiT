# 🪬DiSRHiT
*Disaster Site Rescue hand Tracking robot*<br>
> 2023년 미래산업과학고등학교 메이커창작과 교내대회(일경험) - 인공지능 로봇 손

<img src="/md - 작품사진.jpeg" title="DiSRHiT"></img><br/>
[작동영상]: https://m.youtube.com/watch?v=zfUQFC6qfBE

## [DiSRHiT 조작 메뉴얼]

**[라즈베리파이 접속 command - ssh]**
> ssh rkdgus0810@[ip address(inet)] -p 22
<br>*접속하면 현재 띄워져 있는 창은 라즈베리파이 cmd임.

[directory 이동]
> cd Desktop
> cd AI-Hand

[가상환경 활성화]
> source bin/activate
<br>입력 라인 맨 앞에 “(AI-Hand)" 뜨면 성공!!

[socket통신 주소 확인]
1. ip 주소 조회
> ifconfig
<br>2. vscode 에서 main.py 파일 열고 Host 변수 값(ip주소)과 1번을 통해 조회한 ip주소가 같은지 확인

[라즈베리파이 코드 실행]
1. 초록 레버 on
2. 코드 실행
> python main. py

<br>*초기값 log 뜨고 server 켜질 때까지 기다리기
(서버가 시작되면 ip주소랑 port번호 등이 뜸)

[로컬 컴퓨터(AI) 코드 실행]
vscode 터미널에서 다음 명령어 실행
*vscode 터미널 열기ctrl + ~(단, shift x)
> python main.py
<br>*통신이 시작됬다고 뜨면 성공!(초록색 글자로 뜸)

*혹시 만약에 작동 실패하면 [소켓 통심 주소 확인] 다시 한 번해보기!!
*메뉴얼 순서 중요!!
*대소문자 중요!!
