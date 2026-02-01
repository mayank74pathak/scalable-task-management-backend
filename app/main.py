from fastapi import FastAPI

app = FastAPI(title="Scalable Task Management Backend")

@app.get("/")
def root():
    return {"message": "FastAPI app is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
