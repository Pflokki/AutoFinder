
class Car:
    def __init__(self, url, image, title, sub_title, year, description, date, price, city):
        self.url = url
        self.image = image
        self.title = title
        self.sub_title = sub_title
        self.year = year
        self.description = description
        self.date = date
        self.price = price
        self.city = city

    def to_dict(self):
        return {
            "url": self.url,
            "image": self.image,
            "title": self.title,
            "year": self.year,
            "sub_title": self.sub_title,
            "description": self.description,
            "date": self.date,
            "price": self.price,
            "city": self.city,
        }