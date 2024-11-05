'''
Install the Google AI Python SDK

$ pip install google-generativeai
'''

import os
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # make a .env and put in your own api key

# Create the model
generation_config = {
  "temperature": 2, # This gives FRDAIY the ability to determine how much creativeity they can put into their idea
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192, # Change this for length of FRIDAYS text
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
  system_instruction="Can you please research and try to mimic yourself around friday from iron man please. By this I mean the mannerisms of friday, along with the adjective of friday which is helping iron man in figuring out how to handle his engineering endeavors. Lastly, please refer to me as __name__.",
  
)

history = []

print("Friday: Hello __name__, what project can I help you with today?")

while True: # this while true allows us to go back and forth in convo for as long as we want

  user_input = input("You: ") 

  chat_session = model.start_chat(
    history=history
    # This is as we talk to the chatbot, we want it to have a memory of the session.
  )

  response = chat_session.send_message(user_input)

  model_response = response.text

  print()
  print(f"Friday: {model_response}")
  print()

  history.append({"role": "user", "parts": [user_input]})
  history.append({"role": "model", "parts": [model_response]})
  
  
