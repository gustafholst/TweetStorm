from django.db import models

from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Post(models.Model):
    """
    Post model
    """
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.text

class Vote(models.Model):
    """
    Vote model
    """
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(1)])
