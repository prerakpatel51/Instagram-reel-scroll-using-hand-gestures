try:
    import cv2
except ImportError:
    print("OpenCV not installed. Installing...")
    import subprocess
    subprocess.call(['pip', 'install', 'opencv-python'])

try:
    import mediapipe as mp
except ImportError:
    print("Mediapipe not installed. Installing...")
    import subprocess
    subprocess.call(['pip', 'install', 'mediapipe'])

try:
    import pyautogui
except ImportError:
    print("PyAutoGUI not installed. Installing...")
    import subprocess
    subprocess.call(['pip', 'install', 'pyautogui'])

import time
import importlib
required_modules = ['cv2', 'mediapipe', 'pyautogui']
for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        print(f"{module} not installed. Installing...")
        import subprocess
        subprocess.call(['pip', 'install', module])


import cv2
import mediapipe as mp
import pyautogui
import time
# import requests agar apde external webcam joie too but same network par hovo joie!!
# use python 3.9.17 for best results with opencv and mediapipe both are fully compatible here
# Adjust the delay between consecutive reel scrolls like jetli var detect thai etli vaar fraya na kare etla mate
REEL_SCROLL_DELAY = 0.5


finger_up = True  
finger_down = True  
# initialize kari finger values ne

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def initialize_webcam():
    return cv2.VideoCapture(0) 
# inbuilt camera is 0 and 1 as external webcam. 
# url='https://ip:8080/video'
# phone nu ip address ane port number
# use ipwebcam on ur phone
# video = cv2.VideoCapture(url)

def process_frame(image, hands):
    results = hands.process(image)

    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            detect_gestures(lmList)

    return image


def detect_gestures(lmList):

    global finger_up, finger_down 

    
    first_finger_tip = lmList[8][2]
    pinky_finger_tip = lmList[20][2]
    pinky_finger_tip_base = lmList[17][2]

    
    if first_finger_tip < pinky_finger_tip_base and finger_up:
        pyautogui.scroll(-5)
        finger_up = False
        time.sleep(REEL_SCROLL_DELAY)
    elif first_finger_tip >= pinky_finger_tip_base:
        finger_up = True

    if pinky_finger_tip > pinky_finger_tip_base and finger_down:
        pyautogui.scroll(5)
        finger_down = False
        time.sleep(REEL_SCROLL_DELAY)
    elif pinky_finger_tip <= pinky_finger_tip_base:
        finger_down = True


with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
    video = initialize_webcam()

    start_time = time.time()
    frames = 0

    while True:
        ret, image = video.read()
        image = process_frame(image, hands)

        
        # Variables for FPS calculation screen par dekhase 
        
        frames += 1
        elapsed_time = time.time() - start_time
        fps = frames / elapsed_time
        # Add FPS text to the image position font size opacity
        
        cv2.putText(image, f'FPS: {fps:.2f}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Hand Tracking", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            # press 'q' in the camera window to stop the code
            break

    video.release()
    cv2.destroyAllWindows()
    # release the resources
