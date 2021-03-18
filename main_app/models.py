from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    description = models.TextField()
    product = models.CharField(max_length=100)
    rating = models.IntegerField()
    date = models.DateTimeField("Review Date")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return f"{self.title}, {self.photo}, {self.description},{self.product}, {self.rating}, {self.date}, {self.user}"

class Comment(models.Model):
    comment_text = models.CharField(max_length=240)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("Comment Date", auto_now=True)

    def __str__(self):
        return f"User: {self.user.username}, Review: {self.review.title}, Comment: {self.comment_text}"
    

class UserPhoto(models.Model):
    url = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for user: {self.user_id} @{self.url}"

class ReviewPhoto(models.Model):
    url = models.CharField(max_length=200)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for review: {self.review_id} @{self.url}"