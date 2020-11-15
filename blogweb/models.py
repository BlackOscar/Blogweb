from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.



    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.CharField(max_length = 300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f'Comment of {self.user.username}'

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ManyToManyField(Comment, blank=True, null=True)

    def __str__(self):
        return f'Comments of {self.post}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='proflie_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            ouput_size = (300, 300)
            img.thumbnail(ouput_size)
            img.save(self.image.path)

