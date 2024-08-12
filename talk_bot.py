import os
import sys
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from googletrans import Translator
from langdetect import detect

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import re

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

# Text Parser for the Voice

def clean_text(text: str):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", flags=re.UNICODE)
    result = emoji_pattern.sub(r'', text).replace("*", '')
    return result

# Initialize translator
translator = Translator()

# Voice Responser
# Initialize pyttsx3 engine once
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def talk(text):
    try:
        lang_c = detect(text)
        if lang_c == 'en':
            engine.setProperty('voice', voices[0].id)
        elif lang_c == 'hi':
            engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in talk function: {e}")

def receive_voice():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener = sr.Recognizer()
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source, timeout=5, phrase_time_limit=10)
            info = listener.recognize_google(voice)
            return info.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except Exception as e:
        print(f"Error in receive_voice function: {e}")
        return None

# System Instructions
# instructions = """
#     Consider yourself Robert and you are acting as a strict Examiner and ask verbal questions about the Subject. Ask one question at a time and give honest and critical feedback to the user's answers. Tell the user to repeat if the answer is unsatisfactory or incomplete.
#
#     For the instance, introduce yourself and ask the user for their name and topic.
# """

instructions = """
    Role: Your name is Tom, an AI Freind of Human being you should behave Humbly and politely.
    For instanstance introduce yourself short
"""

# Initialize the Chat Model
chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

system_msg = SystemMessage(content=instructions)
Logic = [system_msg]

MSG = chat.invoke(system_msg.content)

# aimsg = "I am Alfred. How are you?"

intro = "Introduce yourself Properly with your name"

AI_msg = AIMessage(content=MSG.content)
Logic.append(AI_msg)

# Display the initial AI message

print("Chatbot:\n" + AI_msg.content + "\n")
words = clean_text(AI_msg.content)
talk(words)
while True:
    prompt = receive_voice()

    if prompt:
        print("Voice input: " + prompt)
        Logic.append(HumanMessage(content=prompt))

        if "end" in prompt or "bye" in prompt or "finish" in prompt:
            # print("Ending the program.")
            convo = chat.invoke(prompt)
            words = clean_text(convo.content)
            print("\nChatbot:\n" + convo.content + "\n")
            talk(words)
            sys.exit()

        response = chat.invoke(Logic)
        Logic.append(AIMessage(content=response.content))

        print("\nChatbot:\n" + response.content + "\n")
        words = clean_text(response.content)
        talk(words)
