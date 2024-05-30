import base64
import mimetypes

import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, FinishReason


import os
from dotenv import load_dotenv


import tkinter as tk
from tkinter import filedialog as fd

load_dotenv()
root = tk.Tk()
root.withdraw()

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}



system_instruction=[Part.from_text("Sei un trascrittore di lezioni di quinta liceo. Tu trascrivi i file audio che ti vengono mandati. Se non riesci a trascrivere tutto il file audio in un singolo messaggio, ti dirò \"continua con la trascrizione\" e tu dovrai continuare esattamente da dove ti sei interrotto. Nel caso finissi di trascrivere e io continuassi a scriverti \"continua con la trascrizione\", allora dovrai rispondermi unicamente \"ho finito di trascrivere.\". Cerca mentre trascrivi non solo di scrivere le parole che senti, ma nel caso non avessero senso evidenziale in grassetto e correggile con quelle che pensi potrebbero avere senso. Non aggiungere altre informazioni e non scrivere altre risposte che non siano o la trascrizione o \"ho finito di trascrivere.\".")]
model = GenerativeModel('gemini-1.5-pro', safety_settings=safety_settings, system_instruction=system_instruction)
chat = model.start_chat(response_validation=False)


print("ho mandato il messaggio")
filetypes = (
        ('PDF Documents', '*.pdf'),
        ('MP3 Audios', '*.mp3'),
        ('M4A Audios', "*.m4a"),
        ("MP4 Audios", "*.mp4")
    )
file_input = fd.askopenfilename(filetypes=filetypes)

with open(file_input, "rb") as f:
    data = f.read()

def get_chat_response(prompt: list, chat = chat) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)
print("system instruction done")
testo = Part.from_text("Trascrivi questa lezione di italiano")
print("testo done")
mimetypes = {".pdf": "document/pdf", ".mp3":"audio/mpeg", ".m4a":"audio/m4a", ".mp4":"audio/mp4"}
url = Part.from_data(data, mimetypes["".join(list(file_input)[-4:]).lower()])
print("url done")

messagio = [testo, url]
response = get_chat_response(messagio)
print(response)
out = []
out.append(response)
# response = model.generate_content('The opposite of hot is')

while response not in "ho finito di trascrivere":
    response = get_chat_response(Part.from_text("continua con la trascrizione"))
    # response = chat.send_message(response.text)
    print(response)
    out.append(response)

with open("out.txt", "w") as f:
    f.write("".join(out))

input_chat = str(input("Cosa vuoi chiedermi?"))
while input_chat != "/stop":
    response = get_chat_response(Part.from_text(input_chat))
    print(response)
    input_chat = str(input("Cosa vuoi chiedermi?"))