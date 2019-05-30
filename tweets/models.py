"""App models."""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Post(models.Model):
    """
    Post model
    """
    text = models.CharField(max_length=280)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    @property
    def num_up_votes(self):
        """Get number of upvotes."""
        return Vote.objects.filter(post=self).filter(vote=1).count()

    @property
    def num_down_votes(self):
        """Get number of downvotes."""
        return Vote.objects.filter(post=self).filter(vote=-1).count()

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
    vote = models.SmallIntegerField(default=0,
                                    validators=[MinValueValidator(-1),
                                                MaxValueValidator(1)])

    class Meta:
        unique_together = ('voter', 'post',)

    def __str__(self):
        return f"User {self.voter} voted {self.vote} on tweet {self.post}"
