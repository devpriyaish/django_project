from django.contrib import admin
from users.models import Profile, FriendRequest

admin.site.register(Profile)
admin.site.register(FriendRequest)
