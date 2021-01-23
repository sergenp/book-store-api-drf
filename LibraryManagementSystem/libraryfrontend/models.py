from django.db import models
from django.conf import settings
from django.utils.timezone import now

class BaseModel(models.Model):

    is_test_data = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=now)
    modified_on = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_createdby', null=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class AuthorModel(BaseModel):
    name = models.CharField(max_length=100)
    about = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    author_image = models.ImageField(default="placeholder_author.png")

    def __str__(self):
        return self.name


class PublisherModel(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CategoryModel(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BookModel(BaseModel):
    name = models.CharField(max_length=100)
    published_date = models.DateField(null=True, blank=True)
    book_cover = models.ImageField(default="placeholder_cover.png")
    description = models.TextField()
    # how many books that are currently in storage
    store_amount = models.IntegerField(default=1)
    # page count of the book, no need to specify it
    pages = models.IntegerField(null=True, blank=True)
    #ISBN doesn't exist for books that have been published before 1970
    ISBN = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(AuthorModel, on_delete=models.RESTRICT)
    category = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT, null=True, blank=True)
    publisher = models.ForeignKey(PublisherModel, on_delete=models.RESTRICT, null=True, blank=True)
    

    def __str__(self):
        return self.name
