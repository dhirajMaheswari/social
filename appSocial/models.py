# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    description = models.TextField(blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    dob = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True)
    facebook= models.URLField(blank=True)


class Tasveer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    # '''
    # the field "uploaded_by" will be the user who uploads the image.
    # This filed will be updated when the image is uploaded, by assigning the currently
    # logged in user. See the upload_image view defined in views.py file
    # '''
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')
    name = models.CharField(max_length=50)
    your_image = models.FileField(upload_to='')
    your_say = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    isVideo = models.BooleanField(default=False)

    class Meta:
        ordering = ['-upload_date',]


class Like(models.Model):
    post = models.ForeignKey(Tasveer, on_delete=models.CASCADE, related_name='liked_image')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{} : {}'.format(self.user, self.post)


class Share(models.Model):
    post = models.ForeignKey(Tasveer, on_delete=models.CASCADE, related_name='shared_image')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sharer')
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{} : {}'.format(self.user, self.post)


class Comment(models.Model):
    post = models.ForeignKey(Tasveer, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.text


class LikeComment(models.Model):
    post = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='liked_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_liker')
    date_created = models.DateTimeField(auto_now_add=True)
    comment_liked = models.TextField()

    def __str__(self):
        return '{} : {}'.format(self.user, self.post)
