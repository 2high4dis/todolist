from django.shortcuts import render, get_object_or_404, redirect
from .models import ToDoList, ListItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest


def index(request):
    todolists_list = ToDoList.objects.order_by('-add_date')
    context = {
        'todolists_list': todolists_list,
    }
    return render(request=request, template_name='todo_app/index.html', context=context)


@login_required
def create_list(request: HttpRequest):
    todolist = ToDoList.objects.create(
        add_date=timezone.now(), author=request.user)
    todolist.save()
    return redirect('list_view', todolist.id)


@login_required
def list_view(request, todolist_id):
    todolists_list = ToDoList.objects.order_by('-add_date')
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    items = todolist.listitem_set.all()
    context = {
        'todolists_list': todolists_list,
        'todolist': todolist,
        'items': items,
    }
    return render(request=request, template_name='todo_app/todolist.html', context=context)


@login_required
def change_name(request: HttpRequest, todolist_id: int):
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    if request.method == 'POST':
        todolist_name = request.POST.get('todolist_name')
        todolist.list_name = todolist_name
        todolist.save()
        return redirect('list_view', todolist_id)
    if request.method == 'GET':
        todolists_list = ToDoList.objects.order_by('-add_date')
        items = todolist.listitem_set.all()
        context = {
            'todolists_list': todolists_list,
            'todolist': todolist,
            'items': items,
            'change_name': True,
        }
        return render(request=request, template_name='todo_app/todolist.html', context=context)


@login_required
def add_item(request: HttpRequest, todolist_id: int):
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    if request.method == 'POST':
        item_text = request.POST.get('item_text')
        item = ListItem.objects.create(
            list_parent=todolist, item_text=item_text, completed=False, parent=None)
        item.save()
        todolist.finished = None
        todolist.save()
        return redirect('list_view', todolist_id)
    if request.method == 'GET':
        todolists_list = ToDoList.objects.order_by('-add_date')
        items = todolist.listitem_set.all()
        context = {
            'todolists_list': todolists_list,
            'todolist': todolist,
            'items': items,
            'add_item': True
        }
        return render(request=request, template_name='todo_app/todolist.html', context=context)


@login_required
def change_status(request: HttpRequest, todolist_id: int, list_item_id: int):
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    list_item = get_object_or_404(ListItem, pk=list_item_id)
    list_item.completed = 1 - int(list_item.completed)
    list_item.save()
    if all(item.completed for item in todolist.listitem_set.all()):
        todolist.finished = (timezone.now() - todolist.add_date)
    else:
        todolist.finished = None
    todolist.save()
    return redirect('list_view', todolist_id)


@login_required
def add_sub(request: HttpRequest, todolist_id: int, list_item_id: int):
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    list_item = get_object_or_404(ListItem, pk=list_item_id)
    if request.method == 'POST':
        item_text = request.POST.get('item_text')
        item = ListItem.objects.create(
            list_parent=todolist, item_text=item_text, completed=False, parent=list_item)
        item.save()
        todolist.finished = None
        todolist.save()
        return redirect('list_view', todolist_id)
    if request.method == 'GET':
        todolists_list = ToDoList.objects.order_by('-add_date')
        items = todolist.listitem_set.all()
        context = {
            'todolists_list': todolists_list,
            'todolist': todolist,
            'items': items,
            'add_sub': list_item_id
        }
        return render(request=request, template_name='todo_app/todolist.html', context=context)


@login_required
def delete_item(request: HttpRequest, todolist_id: int, list_item_id: int):
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    list_item = get_object_or_404(ListItem, pk=list_item_id)
    list_item.delete()
    if all(item.completed for item in todolist.listitem_set.all()):
        todolist.finished = (timezone.now() - todolist.add_date)
    else:
        todolist.finished = None
    todolist.save()
    return redirect('list_view', todolist_id)


@login_required
def update_item(request: HttpRequest, todolist_id: int, list_item_id: int):
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    list_item = get_object_or_404(ListItem, pk=list_item_id)
    if request.method == 'POST':
        item_text = request.POST.get('item_text')
        list_item.item_text = item_text
        list_item.save()
        return redirect('list_view', todolist_id)
    if request.method == 'GET':
        todolists_list = ToDoList.objects.order_by('-add_date')
        items = todolist.listitem_set.all()
        context = {
            'todolists_list': todolists_list,
            'todolist': todolist,
            'items': items,
            'update_item': list_item_id,
        }
        return render(request=request, template_name='todo_app/todolist.html', context=context)


@login_required
def delete_list(request: HttpRequest, todolist_id: int):
    todolist = get_object_or_404(ToDoList, pk=todolist_id)
    todolist.delete()
    return redirect('index')
