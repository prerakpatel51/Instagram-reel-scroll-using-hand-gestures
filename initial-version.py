

# best so faarrrr
import cv2
import mediapipe as mp
import pyautogui
import time
# import requests agar apde external webcam joie too but same network par hovo joie!!

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
# url='https://ip:8080/video'
# phone nu ip address ane port number
# use ipwebcam on ur phone
video = cv2.VideoCapture(0)
# video = cv2.VideoCapture(url)

reel_scroll_delay = 0.5  
# Adjust the delay between consecutive reel scrolls like jetli var detect thai etli vaar fraya na kare etla mate

# Variables banaya ane intialize karyaa
finger_up = True  # Initialize karyu True jenathi  ensure thai first scroll thai emm
finger_down = True  # Initialize karyu  True jenathi   ensure thai first scroll thai

# Variables for FPS calculation screen par dekhase 
start_time = time.time()
frames = 0

with mp_hand.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7 ,max_num_hands=1) as hands:
    while True:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []

        # Calculate FPS
        frames += 1
        elapsed_time = time.time() - start_time
        fps = frames / elapsed_time

        # Add FPS text to the image
        cv2.putText(image, f'FPS: {fps:.2f}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2, cv2.LINE_AA)

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmark.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
                image = cv2.line(image, (0, 0), (w, 0), (0, 0, 0), thickness=3)  # Change thickness as needed
        if len(lmList) != 0:
            # Index fingertip position
            first_finger_tip = lmList[8][2]
            
            # Pinky fingertip position
            pinky_finger_tip = lmList[20][2]
            
            # Pinky finger base position
            pinky_finger_tip_base = lmList[17][2]
            
            # Check if the index fingertip is above the pinky finger base for scrolling up
            if first_finger_tip < pinky_finger_tip_base:
                if finger_up:
                    # Scroll up
                    pyautogui.scroll(-5)
                    finger_up = False  # Update finger state
                    time.sleep(reel_scroll_delay)  # Add delay between consecutive scrolls
            else:
                finger_up = True  # Update finger state when the condition is not true

            # Check if the pinky fingertip is below the pinky finger base for scrolling down
            if pinky_finger_tip > pinky_finger_tip_base:
                if finger_down:
                    
                    pyautogui.scroll(5)
                    finger_down = False  # Update finger state
                    time.sleep(reel_scroll_delay)  # Add delay between consecutive scrolls
            else:
                finger_down = True  # Update finger state when the condition is not true

        cv2.imshow("Hand Tracking", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            # baar nikadva mate
            break

    video.release()
    cv2.destroyAllWindows()
