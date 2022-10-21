import json
import requests

urlBase = "https://api.covid19api.com"
urlVariable = "/country/germany?from=2022-10-14T00:00:00Z&to=2022-10-21T00:00:00Z"

pathToJsonFile = "./corona-data.json"


def get_json(urlVar):
    response = requests.get(urlVar)
    return response.json()

def create_jsonObject(singleJsonObject):
    return {
        "cases": singleJsonObject["Confirmed"],
        "active": singleJsonObject["Active"],
    }

def calculate(jsonData):
    dayFirst = create_jsonObject(jsonData[0])
    dayLast = create_jsonObject(jsonData[6])

    calculatedCases = dayLast["cases"] - dayFirst["cases"]

    calculatedActives = dayLast["active"] - dayFirst["active"]
    trendValue = "Up" if calculatedActives > 0 else "Down"

    lockdownFulfilled = False
    for day in range(0,7):
        if jsonData[day]["active"] > 10000:
            lockdownFulfilled = True
            break
    
    return [calculatedCases, calculatedActives, trendValue, lockdownFulfilled]

def magicFunction(pathToFileVar):
    jsonData = get_json(urlBase + urlVariable)
    with open(pathToFileVar, 'w') as file:
        json.dump(calculate(jsonData), file)


# Do the magic
magicFunction(pathToJsonFile)