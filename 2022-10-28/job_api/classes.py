from pydantic import BaseModel

class Job(BaseModel):
    id: str
    title: str
    description: str
    