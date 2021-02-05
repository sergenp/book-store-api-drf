# Book Store API
Book store api written in django rest framework

### Installing

I keep the database updated with the newest additions and data, so it should be just cloning the repository and installing the requirements and you're good to go

Create venv
```bash
py -m venv libraryenv
# after activation the env
pip install -r requirements.txt
```

Start the server
```
cd LibraryMangementSystem
# navigate your bash to LibraryMangementSystem/
py manage.py runserver localhost:5000
```

### Deployment
App is written in Django, so this link should suffice [Django Deployment Checklist](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/) 

### Features

- book, author, publisher, category endpoints return the appropriate serialized models,
- book endpoint has url parameter that makes it easy to filter 
  - you can filter books by author, publisher,category, as well as order them via price, or search books via their names
- These endpoints are all paginated (Max 50 results per page) and will return a data in this structure:
    - /api/author endpoint 
    - ```json
        {
            "count": 15,
            "next": null,
            "previous": null,
            "results": [
                    {
                        "id": 3,
                        "name": "Cornell Crowcombe",
                        "about": "Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris.\r\n\r\nMorbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.\r\n\r\nFusce posuere felis sed lacus. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem.\r\n\r\nSed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus.",
                        "birth_date": null,
                        "death_date": null,
                        "author_image": "http://localhost:5000/media/placeholder_author.png"
                    },
                    {
                        "id": 4,
                        "name": "Yorgo Mebius",
                        "about": "Fusce consequat. Nulla nisl. Nunc nisl.\r\n\r\nDuis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum.\r\n\r\nIn hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo.\r\n\r\nAliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis.\r\n\r\nSed ante. Vivamus tortor. Duis mattis egestas metus.",
                        "birth_date": null,
                        "death_date": null,
                        "author_image": "http://localhost:5000/media/placeholder_author.png"
                    },
                ]
        }
      ```
- These endpoints also can be accessed via their ids in the route, 
    - /api/author/3/ would return a data like this:
        - ```json
                {
                    "id": 3,
                    "name": "Cornell Crowcombe",
                    "about": "Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris.\r\n\r\nMorbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.\r\n\r\nFusce posuere felis sed lacus. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem.\r\n\r\nSed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus.",
                    "birth_date": null,
                    "death_date": null,
                    "author_image": "http://localhost:5000/media/placeholder_author.png"
                }
          ```

- JWT Token Authorization
  - Every POST/GET requests listed in here must have a header (except of course login):
    ```json
        "Authorization" : "JWT token" 
    ```
    
  - User Login/Registration
    - Login at : POST /login
    - Register at : POST /api/user

  - Users can add/remove books to/from their Carts
    - POST to Cart endpoint (/api/cart/) with a book id creates a CartItem in the database:
      ```py
          class CartItemModel(BaseModel):
            cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)   
            book = models.ForeignKey(BookModel, on_delete=models.CASCADE)   
            amount = models.IntegerField(default=1) 
      ```
      if the CartItem already is created, amount is increased by 1
    - DELETE to Cart endpoint:
        - with a book data:
            - If there is CartItem with the book and amount is >1, it decreases amount by 1
            - Otherwise deletes the book
        - without a book data:
            - It deletes the Cart from db (sets the deleted flag 1)
            
  - Users can checkout Carts
    - POST to checkout endpoint( /api/checkout ) creates appropriate Shipping Model in the database for the current User and if said User currently have a Cart


- Payment
    - Carts can be bought via bitcoin. For this repository's purposes, when creating Payment for Carts, bitcoin testnet is being used
    - payment_checker.py in cryptopayment app checks if the created Payment model's bitcoin address has the correct value of bitcoin in it, then it creates an Order and Invoice model based on the Payment information (it checks these wallets per 60 seconds in a different thread)
    - Every Payment will have it's own generated bitcoin address in the database. These addresses are being saved as 'wif's. 
        - TODO
            - Create an utility function that transfers every bitcoin in the payment addresses to another address, this function is not necessary, although the owner of the book store may want to convert every payment to cash, and transferring every fund to one address would make that goal easier to achieve 

### Models

Every model is derived from the same BaseModel (declared in LibraryManagementSystem/libraryfrontend/models.py)

```py
is_test = 1 if settings.DEBUG else 0

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
        if not self.get_deleted:
            return BaseQuerySet(self.model).filter(deleted_at=None, is_test_data = is_test)
        return BaseQuerySet(self.model).filter(is_test_data = is_test)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class BaseModel(models.Model):

    objects = BaseManager()
    all_objects = BaseManager(get_deleted=False)
    
    is_test_data = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    modified_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_createdby', 
                                   null=True, blank=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.SET_NULL)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='%(class)s_deletedby', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        abstract = True
    
    def delete(self):
        self.deleted_at = now()
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()
```

- Models with attributes is_test_data = 1 or deleted_at = 'some date' doesn't show up in the api views
  - Unless django settings.DEBUG is True, then the is_test_data = 1 shows up in the API views, this is here to make sure test datas don't show up in production
  - deleted_at flag is there to make sure no data is lost in the database

- With this implementation (Soft Deleting) you can call delete() method from anywhere without a worry of losing your data

#### Models for Frontend

##### Author

```py
class AuthorModel(BaseModel):
    name = models.CharField(max_length=100)
    about = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    author_image = models.ImageField(default="placeholder_author.png")

    def __str__(self):
        return self.name
```

##### Publisher/Category
```py
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
```

##### Book
```py
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
```

#### Models for Commerce

##### Shipping
```py
class ShippingModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField() # address of the shipping
    city = models.CharField(max_length=85) # city
    country = models.CharField(max_length=74) # country
    zipcode = models.CharField(max_length=12) # zipcode
```

##### Cart
```py
class CartModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(BookModel, through="CartItemModel")
    bought = models.BooleanField() # if the cart has been checkedout

    def __str__(self):
        return f"User {self.user}'s Cart {self.id}"
```

##### CartItem
```py
class CartItemModel(BaseModel):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    
    def delete(self):
        # when deleting a cart item, we need to restore the store_amount of the book
        book = BookModel.objects.get(pk=self.book.id)
        book.store_amount += self.amount
        book.save()
        super(CartItemModel, self).delete()
        
    def __str__(self):
        return f"Cart {self.cart}'s Item {self.id} (Book {self.book})"
```

##### Order
```py
class OrderModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    shipping = models.ForeignKey(ShippingModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Order {self.id} of {self.cart}"
```





















