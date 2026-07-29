from fastapi import  FastAPI, Response

app = FastAPI()

BOOKS = []

@app.get("/healthz")
async def health_check():
    return { "message": "Ok" }

