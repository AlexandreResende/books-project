from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
async def first_api():
    return { "message": "Application healthy" }