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

# Create a job like the json after return. Here is the template for the json not the active creation
def create_job(singleJsonObject):
    return {
        "id": singleJsonObject["slug"],
        "title": singleJsonObject["title"],
        "description": singleJsonObject["description"]
    }

# Here we are save the job in a file with the name idvar.json that is like the id of the Object and a json ending
def save_job(idVar, jsonObject, pathToFolder = pathToLocalFolder):
    pathToFile = os.path.join(pathToFolder, idVar+'.json')
    with open(pathToFile, 'w') as file:
        json.dump(jsonObject, file)
    return jsonObject

#----------------Service---------------------

# Here is the function where we save all jobs in the API with the help of the for loop
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

# Here we are list all jobs in the folder pathToFolder. But only this files that have a json ending
# The function of glob.glob is to retrieve files/path names that correspond to a certain pattern. You must import that but not install
def list_jobs(pathToFolder = pathToLocalFolder):
    jobsArray = []
    for filename in glob.glob(pathToFolder + '*.json'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            fileContent = json.loads(f.read())
            jobsArray.append(fileContent)
    return jobsArray

# Here we are get one Job with the id
def get_job(idVar, pathToFolder = pathToLocalFolder):
    if os.path.isfile(os.path.join(pathToFolder, idVar+'.json')):
        with open(os.path.join(pathToFolder, idVar+'.json'), 'r') as f:
            return json.loads(f.read())

# Here we are delete one job with the id
def delete_job(idVar, pathToFolder = pathToLocalFolder):
    os.remove(os.path.join(pathToFolder, idVar+'.json'))
    return idVar

