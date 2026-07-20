from fastapi import FastAPI, Response, status

app = FastAPI()

books = [
    { 'id': 1, 'title': 'Eragon', 'author': 'Christopher Paolini', 'category': 'fantasy'}
]

@app.get("/healthz")
async def health_check():
    return { "message": "Application healthy" }

# using category query param to filter the result on get_books endpoint
@app.get("/books")
async def get_books(category: str = None):
    result = []

    if category is None:
        return { "books": books }

    for book in books:
        if book.get('category').casefold() == category.casefold():
            result.append(book)

    return { 'books': result }

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int, response: Response):
    for b in books:
        if b.get('id') == book_id:
            return b

    response.status_code = status.HTTP_404_NOT_FOUND
    return { "message": "Book not found" }
