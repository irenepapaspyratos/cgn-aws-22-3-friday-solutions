from genericpath import exists
import os
import glob
import requests
import json  


global urlVar, pathToFolder
externalApi = 'https://www.arbeitnow.com/api/job-board-api'
nameFolder = 'jobs-bucket'
pathToLocalFolder = '../' + nameFolder + '/'

#----------------General----------------------

def check_folder(pathToFolder):
    if not exists(pathToFolder): os.mkdir(pathToFolder)

def get_json(url):
    res = requests.get(url)
    return res.json()

# Create a job in the requested json-format by return. This is the function to create the json, not yet used
def create_job(singleJsonObject):
    return {
        "id": singleJsonObject["slug"],
        "title": singleJsonObject["title"],
        "description": singleJsonObject["description"]
    }

# Save the job in a file with the name idVar.json: id of the Object with a json extension
def save_job(idVar, jsonObject, pathToFolder = pathToLocalFolder):
    check_folder(pathToFolder)
    pathToFile = os.path.join(pathToFolder, idVar+'.json')
    with open(pathToFile, 'w') as file:
        json.dump(jsonObject, file)
    return jsonObject

#----------------Service---------------------

# Save all jobs in a folder with help of a for loop
def save_jobs(urlVar = externalApi, pathToFolder = pathToLocalFolder):
    check_folder(pathToFolder)
    try:
        json = get_json(urlVar)
        jobsArray = json["data"]
        for job in jobsArray:
            jobJson = create_job(job)
            save_job(jobJson["id"], jobJson, pathToFolder)
        return True
    except:
        return False

# Create a list of all jobs, that are stored in the folder pathToFolder. Only files with a json-extension are taken.
# The function of glob.glob retrieves files/path-names that correspond to a certain pattern. It must be imported but not installed.
def list_jobs(pathToFolder = pathToLocalFolder):
    jobsArray = []
    for filename in glob.glob(pathToFolder + '*.json'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            fileContent = json.loads(f.read())
            jobsArray.append(fileContent)
    return jobsArray

# Get one Job by it's id
def get_job(idVar, pathToFolder = pathToLocalFolder):
    if os.path.isfile(os.path.join(pathToFolder, idVar+'.json')):
        with open(os.path.join(pathToFolder, idVar+'.json'), 'r') as f:
            return json.loads(f.read())

# Delete one Job by it's id
def delete_job(idVar, pathToFolder = pathToLocalFolder):
    os.remove(os.path.join(pathToFolder, idVar+'.json'))
    return idVar
