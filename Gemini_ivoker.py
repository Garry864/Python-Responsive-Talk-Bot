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


class ChatBot:
    def __init__(self, model: str, temperature: float, google_api_key: str):
        self.chat = ChatGoogleGenerativeAI(model = "gemini-1.5-flash", temperature = 0.3, google_api_key = google_api_key)
        self.logic = []

    def add_system_message(self, content: str):
        system_msg = SystemMessage(content=content)
        self.logic.append(system_msg)
        res = self.chat.invoke(system_msg.content)
        msg = res.content
        return msg

    def add_ai_message(self, content: str):
        ai_msg = AIMessage(content=content)
        self.logic.append(ai_msg)
        return ai_msg.content

    def add_human_message(self, content: str):
        human_msg = HumanMessage(content=content)
        self.logic.append(human_msg)

    def get_response(self):
        response = self.chat.invoke(self.logic)
        return response.content

    def clear_conversation(self):
        self.logic.clear()