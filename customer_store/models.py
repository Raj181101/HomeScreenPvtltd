from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=48, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(validators=[
        RegexValidator(
            regex=r'^(\+\d{1,3}[- ]?)?\d{10}$',
            message="Invalid Number")], max_length=15)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True, null=True)

    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    langitude = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.name


class Bookmark(models.Model):
    title  = models.CharField(max_length=400)
    slug = models.SlugField(max_length=500,blank=True, null=True,unique=True)	
    url = models.URLField(max_length=600, blank=True, null=True)
    source_name = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        value = str(self.title)
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)	

    def __str__(self):
        return self.title

class CustomerBookmark(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    bookmarks = models.ManyToManyField(Bookmark,blank=True)

    total_bookmarks = models.PositiveIntegerField()

    def __str__(self):
        return self.customer.name
