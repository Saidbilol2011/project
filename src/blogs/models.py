from django.db import models
from users.models import User
from general.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.TextField(max_length=65)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.FileField(upload_to='posts/images', null=True, blank=True)

    def __str__(self):
        return self.title


class PostImage(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', max_length=500, null=True)

    def __str__(self):
        return self.post.title



class PostComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.user} on {self.text}'


class PostLike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')


class PostSave(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

