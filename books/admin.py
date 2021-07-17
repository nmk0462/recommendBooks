from django.contrib import admin
from .models import books,User,Click
# Register your models here.
from django.contrib.auth.admin import UserAdmin
# Register your models here.



admin.site.register(User, UserAdmin)
admin.site.register(books)
admin.site.register(Click)