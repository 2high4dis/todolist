from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('<int:todolist_id>/', list_view, name='list_view'),
    path('<int:todolist_id>/saved', set_checked, name='set_checked')
]
