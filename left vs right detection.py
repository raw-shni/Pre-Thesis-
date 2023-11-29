# 1. Install and Import Dependencies
import mediapipe as mp
import cv2
import uuid
import os

# 2. Draw Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 3. Initialize Video Capture
cap = cv2.VideoCapture(0)

# 4. Hand Tracking Loop
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
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

        # Check if results is not None
        if results is not None:
            # Set flag to true
            image.flags.writeable = True

            # RGB 2 BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Rendering results
            if results.multi_hand_landmarks:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    # Get handness (left or right)
                    handness_str = results.multi_handedness[num].classification[0].label
                    print(f"Hand {num + 1}: {handness_str}")

                    # Calculate the position for the text label
                    text_position = (int(hand.landmark[mp_hands.HandLandmark.WRIST].x * image.shape[1]),
                                     int(hand.landmark[mp_hands.HandLandmark.WRIST].y * image.shape[0]))

                    # Draw text label
                    cv2.putText(image, handness_str, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                                cv2.LINE_AA)

                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                              )

            cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the loop
            break

    cap.release()
    cv2.destroyAllWindows()
