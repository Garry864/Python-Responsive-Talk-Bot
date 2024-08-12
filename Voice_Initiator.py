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



# ------------------------------------Initiating Engine------------------------------------
translator = Translator()

# Voice Responser
# Initialize pyttsx3 engine once
engine = pyttsx3.init(driverName='sapi5')
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

# print("Successfull")