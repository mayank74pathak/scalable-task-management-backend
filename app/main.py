from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="Scalable Task Management Backend")

# In-memory storage
tasks = []
task_id_counter = 1


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool


@app.get("/")
def root():
    return {"message": "FastAPI app is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# POST request for creating a task
@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    global task_id_counter

    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "completed": False
    }

    tasks.append(new_task)
    task_id_counter += 1

    return new_task
