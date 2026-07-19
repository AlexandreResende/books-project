from fastapi import FastAPI, Response, status

app = FastAPI()

books = [
    { 'id': 1, 'title': 'Eragon', 'author': 'Christopher Paolini', 'category': 'fantasy'}
]

@app.get("/healthz")
async def health_check():
    return { "message": "Application healthy" }

@app.get("/books")
async def get_books():
    return { "books": books }

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int, response: Response):
    for b in books:
        if b.get('id') == book_id:
            return b

    response.status_code = status.HTTP_404_NOT_FOUND
    return { "message": "Book not found" }
