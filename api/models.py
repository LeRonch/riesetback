from django.db import models
from django.contrib.auth.models import User

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

