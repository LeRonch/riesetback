from re import L
from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):

    name= models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserPicture(models.Model):

    user = models.OneToOneField(
        User,
        related_name='profile_picture',
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        default=1
    )
    profile_picture = models.ImageField(upload_to='pictures', default='pictures/default.jpeg')
    twitter_link = models.CharField(null=True, blank=True, max_length=50)
    patreon_link = models.CharField(null=True, blank=True, max_length=50)
    paypal_link = models.CharField(null=True, blank=True, max_length=50)
    location = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    label = models.CharField(max_length=10)
    count = models.IntegerField()

    def __str__(self):
        return self.label

class Creation(models.Model):

    creation = models.ImageField(upload_to='creations', default='pictures/default.jpeg')
    title = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True, max_length=250)
    user = models.ForeignKey(
        User,
        related_name='creation',
        null=False,
        blank=True,
        on_delete=models.CASCADE,
        default=0
    )
    type = models.CharField(max_length=5)
    download_count = models.IntegerField(default=0)
    date = models.DateTimeField()
    tags = models.ManyToManyField(Tag, blank=True )

    def __str__(self):
        return self.title

class Comment(models.Model):

    content = models.TextField(max_length=250)
    commenting_user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation = models.ForeignKey(Creation, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.content
