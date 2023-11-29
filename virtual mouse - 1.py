import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set up the camera
cap = cv2.VideoCapture(0)
width, height = 640, 480
cap.set(3, width)
cap.set(4, height)

# Smoothing and scaling parameters
SMOOTHING_FACTOR = 0.3
SCALE_FACTOR = 2

cursor_x, cursor_y = 0, 0

# Function to map hand coordinates to mirrored screen coordinates with smoothing
def map_coordinates_smooth(hand_landmarks, width, height):
    global cursor_x, cursor_y
    x = int((1 - hand_landmarks.landmark[8].x) * width * SCALE_FACTOR)
    y = int(hand_landmarks.landmark[8].y * height * SCALE_FACTOR)
    
    # Apply smoothing using a simple moving average
    cursor_x = int((1 - SMOOTHING_FACTOR) * cursor_x + SMOOTHING_FACTOR * x)
    cursor_y = int((1 - SMOOTHING_FACTOR) * cursor_y + SMOOTHING_FACTOR * y)
    
    return cursor_x, cursor_y

# Function to check if the thumb and index finger are close together (pinch gesture)
def is_pinching(hand_landmarks, thumb_tip_id=4, index_finger_tip_id=8, threshold=50):
    thumb_tip = hand_landmarks.landmark[thumb_tip_id]
    index_finger_tip = hand_landmarks.landmark[index_finger_tip_id]
    
    distance = math.sqrt((thumb_tip.x - index_finger_tip.x)**2 + (thumb_tip.y - index_finger_tip.y)**2)
    
    return distance < threshold

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Get the current camera resolution
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to get hand landmarks
    results = hands.process(rgb_frame)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the smoothed mirrored coordinates of the tip of the index finger
            x, y = map_coordinates_smooth(hand_landmarks, width, height)

            # Move the mouse cursor
            pyautogui.moveTo(x, y)

            # Draw a smaller red circle at the smoothed mirrored tip of the index finger
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

            # Check for the pinch gesture (thumb and index finger close together)
            if is_pinching(hand_landmarks):
                # Simulate a click
                pyautogui.click()

    # Display the frame
    cv2.imshow("Virtual Mouse", frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
