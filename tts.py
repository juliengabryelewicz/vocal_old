import pyttsx3

class Tts:

    engine = pyttsx3.init()

    def setVoice(self,id):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[id].id)

    def speak(self,text):
        self.engine.say(text)
        self.engine.runAndWait()