import os
import json
from pathlib import Path

def getSettingsFile(appName = "diags", fileName = "settings.json"):
    if os.name == "posix":
        settingsDir = os.path.join(os.path.expanduser("~"), ".config", appName)
    elif os.name == "nt":
        settingsDir = os.path.join(os.getenv("LOCALAPPDATA"),appName)
    else:
        raise NotImplementedError("Système d'exploitation non reconnu")

    os.makedirs(settingsDir, exist_ok=True)
    return os.path.join(settingsDir, fileName)

def setDefaultSettings(fileName):
    appSettings = dict()
    appSettings["title_state"] = True 
    appSettings["numPage_state"] = True
    appSettings["numDiag_state"] = True
    appSettings["color_state"] = True
    appSettings["format_text"] = "portrait"
    appSettings["flip_state"] = True
    appSettings["legend_state"] = True
    appSettings["cols_value"] = 3
    appSettings["diags_value"] = 15
    appSettings["margin_value"] = 20
    appSettings["coord_state"] = True
    appSettings["down_state"] = True
    appSettings["up_state"] = True
    appSettings["left_state"] = True
    appSettings["right_state"] = True
    with open(fileName, "w") as outfile:
        json.dump(appSettings, outfile, indent=4)

def getSettings(fileName):
    if not Path(fileName).exists():
        setDefaultSettings(fileName)

    with open(fileName, "r") as openfile:
        appSettings = json.load(openfile)
    return(appSettings)

def setNewSettings(fileName, newSettings):
    with open(fileName, "w") as outfile:
        json.dump(newSettings, outfile, indent=4)

def initializeUserInput():
    userInput = dict()
    userInput["title_text"] = ''
    userInput["numPage_value"] = 1
    userInput["numDiag_value"] = 1

    userInput["fens"] = list()
    userInput["legends"] = list()
    userInput["symbols"] = list()
    userInput["arrows"] = list()
    userInput["lichess"] = list()
    return(userInput)

def initializeImagesDict():
    appImages = dict()
    appImages["temp"] = None
    appImages["page"] = None
    appImages["boxes"] = list()
    return(appImages)
