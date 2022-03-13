from django.contrib import admin
from .models import UserProfile, Tasveer,Like, Share, Comment

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Tasveer)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Share)
