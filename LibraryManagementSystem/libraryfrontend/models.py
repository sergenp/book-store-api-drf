from django.db import models
from django.conf import settings
from django.utils.timezone import now

class BaseModel(models.Model):

    is_test_data = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=now)
    modified_on = models.DateTimeField(default=now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_createdby', null=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class AuthorModel(BaseModel):
    __tablename__ = "author"
    name = models.CharField(max_length=100)
    about = models.TextField()
    birth_date = models.DateField()
    death_date = models.DateField()
    author_image = models.ImageField()

    def __repr__(self):
        return '<Author %r>' % self.name


class PublisherModel(BaseModel):
    __tablename__ = "publisher"
    name = models.CharField(max_length=100)

    def __repr__(self):
        return '<Publisher %r>' % self.name


class CategoryModel(BaseModel):
    __tablename__ = "category"
    name = models.CharField(max_length=50)

    def __repr__(self):
        return '<Category %r>' % self.name


class BookModel(BaseModel):
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
