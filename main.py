from __future__ import print_function
import os.path
import os
import io
import json
import pyttsx3
from vosk import Model, KaldiRecognizer
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_FR
import pyaudio
if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

STATE_WAKE = False
WAKE = "jeannette"


##TEXT TO SPEECH
engine = pyttsx3.init()
voices = engine.getProperty('voices') 
#WE want a french female voice
engine.setProperty('voice', voices[3].id)


##PYAUDIO
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


##VOSK
model = Model("model")
rec = KaldiRecognizer(model, 16000)


###SNIPS
with io.open("nlu/test_dataset.json") as f:
    sample_dataset = json.load(f)
nlu_engine = SnipsNLUEngine(config=CONFIG_FR)
nlu_engine = nlu_engine.fit(sample_dataset)

def speak(text):
    engine.say(text)
    engine.runAndWait()

while True:
    data = stream.read(8000, exception_on_overflow = False)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
        if rec.Result().count(WAKE) > 0:
            speak("Que puis-je faire pour toi?")
            STATE_WAKE = True
        if STATE_WAKE == True:
            parsing = nlu_engine.parse(rec.Result())
            if parsing["intent"]["intentName"]=="askBeverage":
                speak("je te prépare ta"+parsing["slots"][0]["rawValue"])
                STATE_WAKE = False
