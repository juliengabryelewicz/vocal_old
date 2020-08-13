from __future__ import print_function
import json
import os.path
import os
import pkg_resources
import pyaudio
import re
from vosk import Model, KaldiRecognizer

from .configuration import Configuration
from .hotword import Hotword
from .nlu import Nlu
from .tts import Tts
from .plugin import PluginList

def main():
    configuration=Configuration("config/config.yaml")

    if not os.path.exists("model/"+configuration.config_list["language"]):
        print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
        exit (1)

    configuration.generate_nlu_file()

    ##HOTWORD
    hotword=Hotword(configuration.config_list["hotword"])

    ##TEXT TO SPEECH
    tts = Tts()
    tts.setVoice(configuration.config_list["voice_id"])

    ##PYAUDIO
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    ##VOSK
    model = Model("model/"+configuration.config_list["language"])
    rec = KaldiRecognizer(model, 16000)


    ###SNIPS
    nlu = Nlu("nlu/"+configuration.config_list["language"]+"/dataset.json")

    # Load plugins
    plugin_directories = [
        os.path.normpath('plugins')
    ]

    plugins_list=PluginList(plugin_directories)
    plugins_list.find_plugins()

    while True:
        data = stream.read(8000, exception_on_overflow = False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            rec_result = json.loads(rec.Result())
            tts.speak(configuration.config_list["sentence_welcome"])
            if rec_result["text"].count(hotword.getWord()) > 0:
                tts.speak(configuration.config_list["sentence_welcome"])
                hotword.setState(True)
            if hotword.getState() == True:
                if rec_result["text"] != "":
                    parsing = nlu.parse(rec_result["text"])
                    if parsing["intent"]["probability"] >= configuration.config_list["min_probability"]:
                        for plugin in plugins_list._plugins:
                            plugin_object = plugins_list._plugins[plugin].plugin_class
                            if plugin_object.has_intent(parsing["intent"]["intentName"]) == True:
                                response = plugin_object.get_response(parsing["intent"]["intentName"],parsing["slots"])
                                tts.speak(response)
                                hotword.setState(False)
                    elif parsing["intent"]["intentName"] == None:
                        hotword.setState(True)
                    else:
                        tts.speak("je ne suis pas sur d'avoir compris, peux-tu répéter?")
