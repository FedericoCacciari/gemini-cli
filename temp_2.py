from urllib import response
# import vertexai
from vertexai.generative_models import GenerativeModel, Image, Part
from vertexai import init
import os
from dotenv import load_dotenv

load_dotenv()

import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const", dest="loglevel", const=logging.DEBUG,
    default=logging.WARNING,
)
parser.add_argument(
    '-v', '--verbose',
    help="Be verbose",
    action="store_const", dest="loglevel", const=logging.INFO,
)
args = parser.parse_args()    
logging.basicConfig(level=args.loglevel)


PROJECT_ID = os.environ.get("PROJECT_ID")
REGION = "europe-west3"  # e.g. us-central1
init(project=PROJECT_ID, location=REGION)

model = GenerativeModel('gemini-1.5-flash-001', system_instruction=["Sei un trascrittore di lezioni di quinta liceo. Tu trascrivi i file audio che ti vengono mandati. Se non riesci a trascrivere tutto il file audio in un singolo messaggio, ti dirò \"continua con la trascrizione\" e tu dovrai continuare esattamente da dove ti sei interrotto. Nel caso finissi di trascrivere e io continuassi a scriverti \"continua con la trascrizione\", allora dovrai rispondermi unicamente \"ho finito di trascrivere.\". Cerca mentre trascrivi non solo di scrivere le parole che senti, ma nel caso non avessero senso evidenziale in grassetto e correggile con quelle che pensi potrebbero avere senso. Non aggiungere altre informazioni e non scrivere altre risposte che non siano o la trascrizione o \"ho finito di trascrivere.\"."])

chat = model.start_chat()

print("ho mandato il messaggio")
with open(r"C:\Users\fedec\Downloads\IIS O. Belluzzi - Fioravanti 53.m4a", "rb") as f:
    data = f.read()
print("Ho letto il file")


def get_chat_response(prompt: list) -> str:
    global chat
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

messaggio = [Part.from_text("Trascrivi questa lezione di italiano"), Part.from_data(data, "audio/opus")]

response = get_chat_response(messaggio)
print(response.text)

# response = model.generate_content('The opposite of hot is')

while response.text != "ho finito di trascrivere":
    response = get_chat_response(Part.from_text("continua con la trascrizione"))
    # response = chat.send_message(response.text)
    print(response.text)
