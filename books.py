from fastapi import  FastAPI, Body, Response, status

from Entities.bookEntity import Book

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
async def create_book(response: Response, new_book=Body()):
    print(new_book)
    BOOKS.append(
        Book(len(BOOKS) + 1, new_book.get("title"), new_book.get("author"), new_book.get("description"), new_book.get("rating"))
    )

    response.status_code = status.HTTP_201_CREATED
    return {}