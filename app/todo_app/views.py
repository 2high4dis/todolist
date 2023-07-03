from django.shortcuts import render, get_object_or_404
import requests

from .models import ToDoList, ListItem


def index(request):
    todolists_list = ToDoList.objects.order_by('-add_date')
    context = {
        'todolists_list': todolists_list,
    }
    return render(request=request, template_name='todo_app/index.html', context=context)


def list_view(request, todolist_id):
    todolists_list = ToDoList.objects.order_by('-add_date')
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    context = {
        'todolists_list': todolists_list,
        'todolist': todolist,
    }
    return render(request=request, template_name='todo_app/todolist.html', context=context)


def set_checked(request, todolist_id):
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    todolists_list = ToDoList.objects.order_by('-add_date')
    context = {
        'todolists_list': todolists_list,
        'todolist': todolist,
    }
    try:
        list_item = todolist.listitem_set.get(pk=request.POST['list_item'])
    except (KeyError, ListItem.DoesNotExist):
        return render(request, template_name='todo_app/todolist.html', context=context)
    else:
        list_item.completed = True
        list_item.save()
        return render(request, template_name='todo_app/todolist.html', context=context)
