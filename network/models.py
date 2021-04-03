"""
Added validator to ensure likes never drops below 0 
https://docs.djangoproject.com/en/3.1/ref/validators/#module-django.core.validators 
"""

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    """
    Create many to many relationship for users a person is following
    """
    followees = models.ManyToManyField(
        "self",
        blank=True,
        related_name="followees"
    )
    def __str__(self):
        return f"{self.id} {self.username}"

class Post(models.Model):
    """
    Model to store information about posts users make
    """
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name="author"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    content = models.CharField(
        max_length=1000,
        blank=False
    )
    likes = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    liked_by = models.ManyToManyField(
        User,
        blank=True, 
        related_name="liked_by",
    )
    def __str__(self):
        return f"{self.author} post at {self.timestamp}"
