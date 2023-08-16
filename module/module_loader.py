import pandas as pd
import pygame

def get_all_modules():
    pdModules = pd.read_excel("module/Modules.ods", engine="odf")
    dictModules = pdModules.to_dict('index')

    allModules = {}

    for m in range(len(dictModules)):
        if type(dictModules[m]["Name"]) == type("string"):  # To skip empty rows
            allModules[dictModules[m]["Name"]] = dictModules[m]

    for m in allModules:  # Assigns each module an image because images cannot be stored in the spreadsheet before hand
        try:
            filelocation = "assets/" + allModules[m]["Category"] + "/" + allModules[m][
                "idName"] + ".png"
            allModules[m]["Image"] = pygame.image.load(open(filelocation))
            allModules[m]["Image"] = pygame.transform.scale2x(allModules[m]["Image"])
        except FileNotFoundError:
            print("No image found for:", m, " | idName:", allModules[m]["idName"])

    return allModules


