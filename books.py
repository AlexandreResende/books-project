from typing import Optional
from datetime import datetime

from fastapi import  FastAPI, Path, Query, HTTPException, status

from Entities.bookEntity import Book
from Requests.createBookRequest import CreateBookRequest
from Requests.updateBookRequest import UpdateBookRequest

app = FastAPI()

BOOKS = [
    Book(1, "Eragon", "Christopher Paolini", "Inheritance trilogy", 5,  2005),
    Book(2, "Eldest", "Christopher Paolini", "Inheritance trilogy", 4, 2006),
    Book(3, "Brisingr", "Christopher Paolini", "Inheritance trilogy", 5, 2007),
    Book(4, "Inheritance", "Christopher Paolini", "Inheritance trilogy", 3, 2009),
]

@app.get("/healthz")
async def health_check():
    return { "message": "Ok" }

@app.get("/books")
async def get_all_books():
    return { "books": BOOKS }

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(new_book: CreateBookRequest):
    BOOKS.append(
        Book(len(BOOKS) + 1, **new_book.model_dump())
    )

    return {}

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/")
async def get_books_by_filter(rating: Optional[int] = Query(gt=0, lt=6, default=None), published_year_date: Optional[int] = Query(gt=1300, lt=datetime.now().year, default=None)):
    books = [
        book for book in BOOKS
        if (rating is None or book.rating == rating)
        and (published_year_date is None or book.published_year_date == published_year_date)
    ]

    return { "books": books }

@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: UpdateBookRequest):
    for book in BOOKS:
        if book.id == book_id:
            book.update_book(updated_book.author, updated_book.title, updated_book.description, updated_book.rating)

            return book

    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)

    return { "message": "Book deleted successfully" }