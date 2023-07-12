from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('create_list/', create_list, name='create_list'),
    path('<int:todolist_id>/', list_view, name='list_view'),
    path('<int:todolist_id>/change', change_name, name='change_name'),
    path('<int:todolist_id>/add', add_item, name='add_item'),
    path('<int:todolist_id>/<int:list_item_id>/change_status',
         change_status, name='change_status'),
    path('<int:todolist_id>/<int:list_item_id>/add', add_sub, name='add_sub'),
    path('<int:todolist_id>/<int:list_item_id>/delete',
         delete_item, name='delete_item'),
    path('<int:todolist_id>/<int:list_item_id>/change',
         update_item, name='update_item'),
    path('<int:todolist_id>/delete',
         delete_list, name='delete_list'),
]
