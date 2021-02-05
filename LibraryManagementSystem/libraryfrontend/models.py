from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User


class BaseQuerySet(models.QuerySet):
    def delete(self):
        return super(BaseQuerySet, self).update(deleted_at=now())

    def hard_delete(self):
        return super(BaseQuerySet, self).delete()


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.get_deleted = kwargs.pop('get_deleted', False)
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.get_deleted:
            return BaseQuerySet(self.model).filter(is_test_data=settings.DEBUG)
        else:
            return BaseQuerySet(self.model).filter(deleted_at=None, is_test_data=settings.DEBUG)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class BaseModel(models.Model):

    objects = BaseManager()
    all_objects = BaseManager(get_deleted=True)
    
    is_test_data = models.BooleanField(default=settings.DEBUG)
    created_at = models.DateTimeField(default=now)
    modified_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    created_by = models.ForeignKey(User, related_name='%(class)s_createdby', 
                                   null=True, blank=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(User,
                            related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.SET_NULL)
    deleted_by = models.ForeignKey(User,
                            related_name='%(class)s_deletedby', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        abstract = True
    
    def delete(self, deleted_by_user=None):
        self.deleted_by = deleted_by_user
        self.deleted_at = now()
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()
       
        
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
    descripton = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class CategoryModel(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

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
    author = models.ForeignKey(AuthorModel, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey(PublisherModel, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return self.name
