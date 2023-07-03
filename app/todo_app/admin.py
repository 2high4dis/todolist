from django.contrib import admin

from .models import ToDoList, ListItem

admin.site.register(ToDoList)
admin.site.register(ListItem)
