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
    author_image = models.ImageField()

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
    book_cover = models.ImageField()
    description = models.TextField()
    amount = models.IntegerField(default=1)
    author = models.ForeignKey(AuthorModel, on_delete=models.RESTRICT)
    category = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT, null=True, blank=True)
    publisher = models.ForeignKey(PublisherModel, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.name
