import cv2
import mediapipe as mp
import sys

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

capture = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
) as hands:

    if not capture.isOpened():
        print("Could not open video capture device")
        sys.exit()

    while capture.isOpened():
        timer = cv2.getTickCount()
        ret, frame = capture.read()

        frame.flags.wriable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        annotations = hands.process(frame)

        frame.flags.writable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if annotations.multi_hand_landmarks:
            for hand_landmarks in annotations.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks,
                    mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmark_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        
        cv2.imshow('Annotated Hands', cv2.flip(frame, 1))
        
        if cv2.waitKey(5) & 0xFF == 27:
            break