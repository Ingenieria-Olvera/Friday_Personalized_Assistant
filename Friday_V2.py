"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai
import speech_recognition as sr # im not sure if I need too since this is recognizing the speech
import pyttsx3

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192, # this could be changed to less but that is really just an idea. DEFAULT 8192
  "response_mime_type": "text/plain",
}


'''
Saftey settings were supposed to be here yet I am not sure as to why they are not
'''

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash", 
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Can you please research and try to mimic yourself around friday from iron man please. By this I mean the mannerisms of friday, along with the adjective of friday which is helping iron man in figuring out how to handle his engineering endeavors. These endevours should be things like maknig an ionic wind generator, a coil gun, or anything that could be good on an MIT college application. Lastly, please refer to me as Jonathan.",
  #this is the prompt that makes it be like friday, this could be refined in the playground to see the best possible objective
)


history = []

print("Friday: Hello Jonathan, what project can I help you with today?")

while True: # this while true allows us to go back and forth in convo for as long as we want
  
 # Use speech recognition to get user input
  with sr.Microphone() as source:
    print("Listening...")
    audio = r.listen(source)

  try:
    user_input = r.recognize_google(audio)

  except sr.UnknownValueError:
    print("Sorry, I didn't catch that. Try again.")
    continue
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

    continue

  # user_input = input("You: ") 

  chat_session = model.start_chat(
    history=history
    # This is as we talk to the chatbot, we want it to have a memory of the session.
  )

  response = chat_session.send_message(user_input)

  model_response = response.text

  print()
  print(f"Friday: {model_response}")
  print()

  # Speak the model's response
  engine.say(model_response)
  engine.runAndWait()

  
  history.append({"role": "user", "parts": [user_input]})
  history.append({"role": "model", "parts": [model_response]})
  
