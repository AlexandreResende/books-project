from typing import Optional

from fastapi import  FastAPI, Response, status

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

@app.post("/books")
async def create_book(response: Response, new_book: CreateBookRequest):
    BOOKS.append(
        Book(len(BOOKS) + 1, **new_book.model_dump())
    )

    response.status_code = status.HTTP_201_CREATED
    return {}

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int, response: Response):
    for book in BOOKS:
        if book.id == book_id:
            return book

    response.status_code = status.HTTP_404_NOT_FOUND
    return { "message": "Book not found" }

@app.get("/books/")
async def get_books_by_filter(rating: Optional[int] = None, published_year_date: Optional[int] = None):
    books = [
        book for book in BOOKS
        if (rating is None or book.rating == rating)
        and (published_year_date is None or book.published_year_date == published_year_date)
    ]

    return { "books": books }

@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: UpdateBookRequest, response: Response):
    for book in BOOKS:
        if book.id == book_id:
            book.update_book(updated_book.author, updated_book.title, updated_book.description, updated_book.rating)

            return book

    response.status_code = status.HTTP_404_NOT_FOUND
    return { "message": "Book not found" }

@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)

    return { "message": "Book deleted successfully" }