import yaml
import json


class Config:
    def __init__(self):
        
        with open("config.yaml", "r") as file:

            data = yaml.safe_load(file)
            things = data["services"] 

            for i in range(len(things)):
                param = things[i]
                name = param["name"]
                config = param["config"]
                # print("name: " + name)
                # print(f"config: {str(config)}")

                if name == "messenger": 
                    self.api_endpoint = config["api_endpoint"]
                    self.token =  config["access_token"] 
                if name == "pdf_analyzer":
                    self.file_directory = config["deck_directory"]

    def getMessengerToken(self):
        return self.token
    def getMessengerEndpoint(self):
        return self.api_endpoint
    def getFileDirectory(self):
        return self.file_directory
    

            

    