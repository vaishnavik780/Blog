from django.db import models
from django.contrib.auth.models import User
import datetime 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    class Meta:
        verbose_name="Categorie"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)