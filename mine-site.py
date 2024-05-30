import os
from os import environ
from dotenv import load_dotenv

import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession, Part
from vertexai.generative_models import HarmCategory, HarmBlockThreshold

import google.generativeai as genai


import langchain
from langchain_google_vertexai import ChatVertexAI as GoogleAi
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage




import streamlit as st
#TODO: Save to DB
from tinydb import TinyDB as tbd


## Load .env and access google cloud

load_dotenv()
project_id = environ["project_id"]
credentials = environ["GOOGLE_APPLICATION_CREDENTIALS"]

vertexai.init(project=project_id, location="europe-west3")




## Backend

def make_chat(model_name):
    safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
    

    model = GoogleAi(model_name=model_name, safety_settings = safety_settings, )

    return model



def get_chat_response(chat, st) -> str:
    response = chat.invoke(st.session_state.messages + [HumanMessage(content = prompt)])
    return response





def on_start():
    st.set_page_config(
        page_title="Gemini AI",
        page_icon="🤖"
    )

    st.title("Chat with PDF files using Gemini🤖")
    

    
    #TODO: Clear chat history
    # st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # Chat input
    # Placeholder for chat messages


def messages():
    global chat
    global history

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [AIMessage(content = "Hello, I am a bot. How can I help you?")]
        
    for message in st.session_state.messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)

    # Chat input

    if prompt := st.chat_input():
        st.session_state.messages.append(AIMessage(content = prompt))
        with st.chat_message("user"):
            st.write(prompt)

    if isinstance(st.session_state.messages[-1], HumanMessage):
        response = get_chat_response(chat, st)
        st.session_state.messges.append(response)
        with st.chat_message("assistant"):
            st.write(response.content)
    
def main():
    global chat
    chat = make_chat("gemini-experimental")
    on_start()
    messages()
    
    # st.code()

# I want to know why the chat is not consistent through messages

main() 