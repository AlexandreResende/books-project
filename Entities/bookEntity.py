class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

    def update_book(self, author, title, description, rating):
        self.author = author if author is not None else self.author
        self.title = title if title is not None else self.title
        self.description = description if description is not None else self.description
        self.rating = rating if rating is not None else self.rating