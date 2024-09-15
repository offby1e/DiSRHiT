import cv2

# 첫 번째 웹캠 연결
cap1 = cv2.VideoCapture(0)

# 두 번째 웹캠 연결
cap2 = cv2.VideoCapture(1)

# 웹캠이 정상적으로 열렸는지 확인
if not (cap1.isOpened() and cap2.isOpened()):
    print("웹캠을 열 수 없습니다.")
    exit()

while True:
    # 첫 번째 웹캠에서 프레임 읽기
    ret1, frame1 = cap1.read()
    if not ret1:
        print("첫 번째 웹캠에서 프레임을 읽을 수 없습니다.")
        break

    # 두 번째 웹캠에서 프레임 읽기
    ret2, frame2 = cap2.read()
    if not ret2:
        print("두 번째 웹캠에서 프레임을 읽을 수 없습니다.")
        break

    # 프레임 화면에 표시
    cv2.imshow('Webcam 1', frame1)
    cv2.imshow('Webcam 2', frame2)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 사용이 끝난 웹캠 해제
cap1.release()
cap2.release()

# 모든 창 닫기
cv2.destroyAllWindows()
