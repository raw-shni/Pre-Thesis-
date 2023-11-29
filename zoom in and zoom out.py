import cv2
import mediapipe as mp
import math

def hand_zoom_detection():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    # Initialize the video capture (you can replace '0' with the camera device index or a video file path)
    cap = cv2.VideoCapture(0)

    # Set the fixed viewer size (you can adjust this to your desired dimensions)
    target_aspect_ratio = 16 / 9  # Change to your desired aspect ratio
    viewer_width = 900
    viewer_height = int(viewer_width / target_aspect_ratio)

    # Initialize variables for tracking the zoom state
    zoom_factor = 0.3
    initial_distance = None

    # Create a separate viewer window with a fixed size
    viewer = cv2.namedWindow("Hand Tracking and Zoom", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Hand Tracking and Zoom", viewer_width, viewer_height)

    while cap.isOpened():
        ret, frame = cap.read()

        # Check if the capture was successful
        if not ret:
            break

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Calculate the Euclidean distance between two specific hand landmarks (e.g., thumb and index finger)
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                distance = math.dist((thumb.x, thumb.y), (index.x, index.y))

                if initial_distance is None:
                    initial_distance = distance

                # Detect zoom in and zoom out gestures based on finger movement
                if distance > initial_distance:
                    # Fingers moved apart, zoom in
                    zoom_factor *= 0.5  # Adjust this factor for your desired zoom sensitivity
                    cv2.putText(frame, "Zoom In", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                elif distance < initial_distance:
                    # Fingers moved closer, zoom out
                    zoom_factor /= 0.5  # Adjust this factor for your desired zoom sensitivity
                    cv2.putText(frame, "Zoom Out", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                initial_distance = distance

                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Apply zoom factor to the frame
        zoomed_frame = cv2.resize(frame, (viewer_width, viewer_height))

        # Display the zoomed frame in the viewer window
        cv2.imshow("Hand Tracking and Zoom", zoomed_frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the loop
            break

    cap.release()
    cv2.destroyAllWindows()

hand_zoom_detection()
