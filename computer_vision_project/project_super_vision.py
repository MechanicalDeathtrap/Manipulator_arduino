import cv2
import mediapipe as mp
import serial
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

arduino = serial.Serial('COM7', 9600)

def count_fingers(landmarks):
    fingers = []
    finger_tips = [8, 12, 16, 20]
    finger_bases = [6, 10, 14, 18]


    if landmarks[4][0] < landmarks[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    for tip, base in zip(finger_tips, finger_bases):
        if landmarks[tip][1] < landmarks[base][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

cap = cv2.VideoCapture(0)

print("Запущено. Покажите пальцы перед камерой. Нажмите пробел для сохранения числа.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = []
            for lm in hand_landmarks.landmark:
                h, w, _ = frame.shape
                landmarks.append((int(lm.x * w), int(lm.y * h)))

            finger_count = count_fingers(landmarks)
            cv2.putText(frame, f'Fingers: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if cv2.waitKey(1) & 0xFF == ord(' '):
                print(f"Сохранено: {finger_count} пальцев")
                try:
                    arduino.write(f'{finger_count}\n'.encode())
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Ошибка отправки данных: {e}")


    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
arduino.close()