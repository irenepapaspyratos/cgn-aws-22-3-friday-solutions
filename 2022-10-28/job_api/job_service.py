import os
import glob
import requests
import json  


global urlVar, pathToFolder
externalApi = "https://www.arbeitnow.com/api/job-board-api"
pathToLocalFolder = "../jobs-bucket/"

#----------------General----------------------

def get_json(url):
    res = requests.get(url)
    return res.json()

def create_job(singleJsonObject):
    return {
        "id": singleJsonObject["slug"],
        "title": singleJsonObject["title"],
        "description": singleJsonObject["description"]
    }

def save_job(idVar, jsonObject, pathToFolder = pathToLocalFolder):
    pathToFile = os.path.join(pathToFolder, idVar+'.json')
    with open(pathToFile, 'w') as file:
        json.dump(jsonObject, file)
    return jsonObject

#----------------Service---------------------

def save_jobs(urlVar = externalApi, pathToFolder = pathToLocalFolder):
    try:
        json = get_json(urlVar)
        jobsArray = json["data"]
        for job in jobsArray:
            jobJson = create_job(job)
            save_job(jobJson["id"], jobJson, pathToFolder)
        return True
    except:
        return False
    
def list_jobs(pathToFolder = pathToLocalFolder):
    jobsArray = []
    for filename in glob.glob(pathToFolder + '*.json'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            fileContent = json.loads(f.read())
            jobsArray.append(fileContent)
    return jobsArray
    
def get_job(idVar, pathToFolder = pathToLocalFolder):
    if os.path.isfile(os.path.join(pathToFolder, idVar+'.json')):
        with open(os.path.join(pathToFolder, idVar+'.json'), 'r') as f:
            return json.loads(f.read())

def delete_job(idVar, pathToFolder = pathToLocalFolder):
    os.remove(os.path.join(pathToFolder, idVar+'.json'))
    return idVar
