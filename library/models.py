from django.db import models
import datetime
# Create your models here.
from django.db import models
from django.forms import ValidationError


    
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    
    

    def __str__(self):
        return self.name

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    image_url = models.ImageField(upload_to="media/books/",blank=True,null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    isbn = models.CharField(max_length=13, unique=True)
    count = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    

    def __str__(self):
        return self.name

class Record(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=5))
    count = models.IntegerField(default=1)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title + " borrowed by " + self.customer.name
    
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.due_date and self.due_date < self.issue_date:
            raise ValidationError({'due_date': 'Due date cannot be in the past.'})
        

    def save(self, *args, **kwargs):
        self.book.save()  # Save the Book instance with updated count
        super().save(*args, **kwargs)  # Call the original save method


