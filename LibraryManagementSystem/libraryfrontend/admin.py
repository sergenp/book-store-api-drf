from django.contrib import admin
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel

# Register your models here.
admin.site.register(AuthorModel)
admin.site.register(BookModel)
admin.site.register(CategoryModel)
admin.site.register(PublisherModel)
