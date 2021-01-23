from django.contrib import admin

from .models import Category, Data, Direction, Method

admin.site.register(Direction)
admin.site.register(Method)
admin.site.register(Category)
admin.site.register(Data)
