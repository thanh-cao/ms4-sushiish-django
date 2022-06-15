from django.db import models

# Create your models here.


class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return f'Contact form from {self.name} - {self.email}'
