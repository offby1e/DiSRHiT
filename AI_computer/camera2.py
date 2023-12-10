import cv2

# 웹캠 열기
cap = cv2.VideoCapture(1)  # 0은 기본 카메라를 의미합니다. 다른 숫자를 사용하여 다른 카메라를 선택할 수 있습니다.

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 프레임이 제대로 읽혔는지 확인
    if not ret:
        print("웹캠에서 프레임을 읽을 수 없습니다.")
        break

    # 프레임 표시
    cv2.imshow('Webcam', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()
