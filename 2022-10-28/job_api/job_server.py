from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn

from classes import Job
import job_service

app = FastAPI()

externalApiUrl = "https://www.arbeitnow.com/api/job-board-api"
pathToBucketFolder = "./jobs-bucket/"

# The JSONResponse is a quick way to send custom statuscode with content to display
@app.get("/")
def read_root():
    return JSONResponse(status_code=200, content={"message": "Your API is working fine!"})

# A custom default status_code after the route can be set to be returned
# Otherwise the regular default HTTP status will be sent (would be 200 in this case)
# The status_code can be changed if anything happens, 
# but for consistence and conventional reasons for each situation the standard status code should be taken (in this example: 200 for " OK ")
@app.get("/job/request-jobs", status_code=status.HTTP_201_CREATED)
def save_jobs():
    if job_service.save_jobs() is False: 
        raise HTTPException(status_code=400, detail="No connection to external API")
    else:
        return "All requested jobs saved."

# A type can be set/requested for the response to be format-safe
@app.get("/job", response_model = list[Job])
def get_jobs():
    jobs = job_service.list_jobs()
    if jobs: return jobs
    else: raise HTTPException(status_code=404, detail="No Jobs could be loaded")

# A type can also be set/requested to check an "input"
@app.get("/job/{id}")
def get_job(id: str):
    if job_service.get_job(id): return job_service.get_job(id)
    raise HTTPException(status_code=404, detail="Job not found")

# Save one Job to the Job-folder. 
# MUST be assured, that incoming type is right (here type of our self-created class -> job: Job)!!!
# A pydantic Model (here: Job) is not subscriptable, means: properties are not reachable,
# therefore the item has to be transformed to json in order to get the id of the job.
# If it was succenful, status 201 for created is set be responded
# If it wasn't successful, status 500 for server error is set to be responded
@app.post("/job", status_code=status.HTTP_201_CREATED)
def save_job(job: Job):
    job_encoded = jsonable_encoder(job)
    id = job_encoded["id"]
    if job_service.save_job(id, job_encoded): return job_encoded
    raise HTTPException(status_code=500, detail="Job could not be saved")

# The Response-Model can assure to send as answer: custom HTTP-status AND a result to display in certain format
# Upsert => update old one or create new one, if this one isn't existing yet
@app.put("/job/{id}", status_code=200)
def upsert_job(jobNew: Job, response: Response):
    jobNewVersion = jsonable_encoder(jobNew)
    id = jobNewVersion["id"]
    if job_service.get_job(id):
        if job_service.delete_job(id) is False:
            raise HTTPException(status_code=500, detail="Old job could not be deleted -> Abort")
        else:
            if job_service.save_job(id, jobNewVersion): return job_service.save_job(id, jobNewVersion)
            else: raise HTTPException(status_code=500, detail="New job version could not be saved, but old one already deleted")
    else:
        if job_service.save_job(id, jobNewVersion): 
            response.status_code = 201
            return job_service.save_job(id, jobNewVersion)
        else: 
            raise HTTPException(status_code=500, detail="New job could not be saved")

# Delete job by id
@app.delete("/job/{id}", response_model= str)
def delete_job(id):
    result = job_service.delete_job(id)
    if result is False: raise HTTPException(status_code=404, detail="Job not found")
    return result
    
# Start the main Method
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
