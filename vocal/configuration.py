import glob
import os
import yaml

class Configuration:

    config_list = {}
    join_yaml = " "

    def __init__(self,fileConfiguration):
        with open(fileConfiguration) as file:
            self.config_list = yaml.load(file, Loader=yaml.FullLoader)

    def generate_nlu_file(self):
    	nlu_files = glob.glob('plugins/**/nlu/'+self.config_list["language"]+'/*.yaml')
    	os.system('snips-nlu generate-dataset '+self.config_list["language"][:2]+' '+self.join_yaml.join(nlu_files)+' > nlu/'+self.config_list["language"]+'/dataset.json')