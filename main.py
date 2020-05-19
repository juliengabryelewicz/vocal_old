from __future__ import print_function
import os.path
import os
from vosk import Model, KaldiRecognizer
import pyaudio

from nlu import Nlu
from tts import Tts

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

STATE_WAKE = False
WAKE = "jeannette"

##TEXT TO SPEECH
tts = Tts()
tts.setVoice(3)

##PYAUDIO
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

##VOSK
model = Model("model")
rec = KaldiRecognizer(model, 16000)


###SNIPS
nlu = Nlu("nlu/test_dataset.json")

while True:
    data = stream.read(8000, exception_on_overflow = False)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
        if rec.Result().count(WAKE) > 0:
            tts.speak("Que puis-je faire pour toi?")
            STATE_WAKE = True
        if STATE_WAKE == True:
            parsing = nlu.parse(rec.Result())
            if parsing["intent"]["intentName"]=="askBeverage":
                tts.speak("je te prépare ta"+parsing["slots"][0]["rawValue"])
                STATE_WAKE = False
