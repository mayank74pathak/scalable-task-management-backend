from fastapi import FastAPI,HTTPException
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


# CREATE task
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


# READ all tasks
@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    return tasks


# READ task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )



# UPDATE task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskCreate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_data.title
            task["description"] = task_data.description
            return task
    return {"error": "Task not found"}


# DELETE task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return {"message": "Task deleted successfully"}
    return {"error": "Task not found"}

