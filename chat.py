import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession, Part

from logging import Logger

from dotenv import load_dotenv
import os
from os import environ

from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Static
from textual.containers import ScrollableContainer

from pyreadline3 import Readline
readline = Readline()

from tinydb import TinyDB as tbd

# database = tbd()


load_dotenv()
# TODO(developer): Update and un-comment below line
# project_id = "PROJECT_ID"
project_id = environ["project_id"]
credentials = environ["GOOGLE_APPLICATION_CREDENTIALS"]

vertexai.init(project=project_id, location="europe-west3")

model = GenerativeModel(model_name="gemini-1.5-pro-preview-0409")

chat = model.start_chat()

def get_chat_response(chat: ChatSession, prompt: list) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

def make_part(prompt:str, data:bytes=None, type:str=None) -> [type, type]:
    if data: return [Part.from_text(prompt), Part.from_data(data, type)]
    return Part.from_text(prompt)
# file_data = open(r"C:\Users\fedec\Documents\Friedrich Nietzsche.pdf", "rb").read()

# prompt = make_part("Riassumimi questo pdf", file_data, "application/pdf")

# print(get_chat_response(chat, prompt))

def chat_do():
    global chat
    console = Console()
    console.clear()
    console.print("Chat con Gemini-AI")
    user_input = console.input("Utente:")
    while user_input != "!!exit":

        console.print(get_chat_response(chat, make_part(user_input)))
        user_input = console.input("Utente:")




if __name__ == "__main__":
    app = StopwatchApp()
    app.run()