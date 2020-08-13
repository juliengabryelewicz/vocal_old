import io
import json
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_FR

class Nlu:

    nlu_engine = SnipsNLUEngine(config=CONFIG_FR)

    def __init__(self,fileNlu):
        with io.open(fileNlu) as f:
            sample_dataset = json.load(f)
        self.nlu_engine = self.nlu_engine.fit(sample_dataset)

    def parse(self,text):
        return self.nlu_engine.parse(text)