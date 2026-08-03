class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year_date: int

    def __init__(self, id, title, author, description, rating, published_year_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year_date = published_year_date

    def update_book(self, author, title, description, rating, published_year_date):
        self.author = author if author is not None else self.author
        self.title = title if title is not None else self.title
        self.description = description if description is not None else self.description
        self.rating = rating if rating is not None else self.rating
        self.published_year_date = published_year_date if published_year_date else self.published_year_date