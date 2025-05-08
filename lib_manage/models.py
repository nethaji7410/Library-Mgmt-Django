
from django.db import models


# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=30)
    photo=models.ImageField(upload_to="uploads",default="a.png")
    email=models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    

class reader(models.Model):
        reference_id=models.CharField(max_length=200)
        reaedr_name=models.CharField(max_length=200)
        reader_contact=models.CharField(max_length=200)
        reader_address=models.TextField()
        active=models.BooleanField(default=True)

        def __str__(self):
            return self.reaedr_name
        