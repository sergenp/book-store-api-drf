from django.db import models

class AuthorModel(models.Model):
    __tablename__ = "author"
    name = models.CharField(max_length=100)
    about = models.TextField()
    birth_date = models.DateField()
    death_date = models.DateField()
    author_image = models.ImageField()

    def __repr__(self):
        return '<Author %r>' % self.name


class PublisherModel(models.Model):
    __tablename__ = "publisher"
    name = models.CharField(max_length=100)

    def __repr__(self):
        return '<Publisher %r>' % self.name


class CategoryModel(models.Model):
    __tablename__ = "category"
    name = models.CharField(max_length=50)

    def __repr__(self):
        return '<Category %r>' % self.name


class BookModel(models.Model):
    __tablename__ = "book"
    name = models.CharField(max_length=100)
    published_date = models.DateField()
    book_cover = models.ImageField()
    description = models.TextField()
    amount = models.IntegerField()
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    publisher = models.ForeignKey(PublisherModel, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Book %r>' % self.name
