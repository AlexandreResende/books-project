from fastapi import  FastAPI, Response, status

from Entities.bookEntity import Book
from Requests.createBookRequest import CreateBookRequest

app = FastAPI()

BOOKS = [
    Book(1, "Eragon", "Christopher Paolini", "Inheritance trilogy", 5),
]

@app.get("/healthz")
async def health_check():
    return { "message": "Ok" }

@app.get("/books")
async def get_all_books():
    return { "books": BOOKS }

@app.post("/books")
async def create_book(response: Response, new_book: CreateBookRequest):
    BOOKS.append(
        Book(len(BOOKS) + 1, **new_book.model_dump())
    )

    response.status_code = status.HTTP_201_CREATED
    return {}