import mimetypes

import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, FinishReason

import tkinter as tk
import tkinter.filedialog as fd

import os

from dotenv import load_dotenv
root = tk.Tk()
root.withdraw()

from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt as prompt

load_dotenv()
console = Console()


safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}
console.print(Markdown("# Parla con Gemini:"))
system_input = prompt.ask("Inserire le istruzioni di sistema da dare a Gemini\n")

system_instruction = [Part.from_text(system_input)] if system_input else None

model = GenerativeModel('gemini-1.5-pro', safety_settings=safety_settings, system_instruction=system_instruction)

chat = model.start_chat(response_validation=False)
print("ho mandato il messaggio")




filetypes = (
        ("ALL", "*.*"),
        ('PDF Documents', '*.pdf'),
        ('MP3 Audios', '*.mp3'),
        ('M4A Audios', "*.m4a"),
        ("MP4 Audios", "*.mp4")
    )

def get_chat_response(prompt: list, chat = chat) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return Markdown("".join(text_response))

def get_file():
    file_input = fd.askopenfilenames(filetypes=filetypes)
    data = {}
    for i in file_input:
        with open(i, "rb") as f:
            data[i] = f.read()
    
    testo = Part.from_text("Eccoti le lezioni di italiano")
    mimetypes = {".pdf": "application/pdf", ".mp3":"audio/mpeg", ".m4a":"audio/m4a", ".mp4":"audio/mp4"}
    parts = []
    for i in (data.keys()):
        print(i)
        j = data[i]
        url = Part.from_data(j, mimetypes["".join(list(str(i))[-4:]).lower()])
        parts.append(url)
    messagio = [testo] + parts
    return messagio
# response = model.generate_content('The opposite of hot is')


input_chat = str(prompt.ask("Cosa vuoi chiedermi?"))
while input_chat != "/stop":
    if input_chat == "/file":
        messagio = get_file()
        response = get_chat_response(messagio)
    else:
        response = get_chat_response(Part.from_text(input_chat))
    console.print(response)
    input_chat = str(prompt.ask("Cosa vuoi chiedermi?\n"))

