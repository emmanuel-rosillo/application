import os
from config import Config


def createPersonalPath(name):
    localPath = Config.compareFacesPath
    personalPath = localPath + '/' + name
    if not os.path.exists(personalPath):
        print("Se creo carpeta: ", personalPath)
        os.makedirs(personalPath)
    else:
        print("la persona ya se registro")
    return personalPath
