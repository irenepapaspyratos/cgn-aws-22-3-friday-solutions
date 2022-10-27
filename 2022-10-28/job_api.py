from os import remove
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class Job(BaseModel):
    id: str
    title: str
    description: str
            
jobs = [
    {
        "id": "1",
        "name": "Wladimir",
        "description": "abc"
    },
    {
        "id": "3",
        "name": "Murphy",
        "description": "def"
    },
    {
        "id": "2",
        "name": "Aleksandra",
        "description": "ghi"
    }
]

@app.get("/")
def read_root():
    return {"api-health": "ok"}

@app.get("/job")
def list_all_jobs():
    return jobs

@app.get("/job/{id}")
def get_single_job(id):
    for job in jobs:
        if job["id"] == id:
            return job
    raise HTTPException(status_code=404, detail="Job not found")

@app.post("/job")
async def create_single_job(job: Job):
    jobs.append(job)
    return job

@app.put("/job/{id}")
async def update_single_job(id: str, jobToUpdate: Job):
    counter=0
    for job in jobs:
        if job["id"] == id:
            jobs.pop(counter) 
            job_encoded = jsonable_encoder(jobToUpdate)
            jobs.append(job_encoded)
            return job_encoded
        counter += 1
    raise HTTPException(status_code=404, detail="Job not found")

@app.delete("/job/{id}")
def delete_single_job(id):
    counter=0
    for job in jobs:
        if job["id"] == id:
            return jobs.pop(counter)
        counter += 1
    raise HTTPException(status_code=404, detail="Job not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    