import asyncio
import cv2
import numpy as np
import sys
import time
import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

# Timing settings
inside_rect_f = inside_rect_h = inside_rect_p = inside_rect_q = False
start_time = 0
required_time_in_rect = 2

async def opencv_stuff():
    s = 0
    if len(sys.argv) > 1:
        s = sys.argv[1]

    source = cv2.VideoCapture(s)
    win_name = 'Hand Tracking Interface'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    while cv2.waitKey(1) != 27:  # Escape key to exit
        has_frame, frame = source.read()
        if not has_frame:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        # Define rectangles
        rectangles = {
            "FRIDAY": ((70, 70), (170, 120), (0, 0, 255)),
            "HELP": ((50, 300), (100, 350), (0, 255, 0)),
            "PROJECTS": ((450, 70), (550, 120), (255, 0, 0)),
            "QUIT": ((530, 300), (580, 350), (78, 54, 41)),
        }

        for name, ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y), color) in rectangles.items():
            cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), color, 2)

        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            for name, ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y), _) in rectangles.items():
                if (x < bottom_right_x and x + w > top_left_x and y < bottom_right_y and y + h > top_left_y):
                    if not locals()[f'inside_rect_{name.lower()}']:
                        locals()[f'inside_rect_{name.lower()}'] = True
                        start_time = time.time()
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= required_time_in_rect:
                        cv2.putText(frame, f"Action Triggered: {name}!", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                else:
                    locals()[f'inside_rect_{name.lower()}'] = False

        cv2.imshow(win_name, frame)

    source.release()
    cv2.destroyAllWindows()

async def google():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)

    r = sr.Recognizer()
    generation_config = {
        "temperature": 2,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Can you please research and try to mimic yourself around friday from iron man please. By this I mean the mannerisms of friday, along with the adjective of friday which is helping iron man in figuring out how to handle his engineering endeavors. Lastly, please refer to me as __Name__",
    )

    history = []
    print("Friday: Hello __name__, what project can I help you with today?")

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

        try:
            user_input = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Try again.")
            continue
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            continue

        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response = response.text

        print(f"Friday: {model_response}")
        engine.say(model_response)
        engine.runAndWait()

        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})

async def main():
    print("We are starting")
    await asyncio.gather(opencv_stuff(), google())

if __name__ == "__main__":
    asyncio.run(main())

asyncio.run(main())
