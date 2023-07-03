from django.db import models
import mptt


class ToDoList(models.Model):
    list_name = models.CharField(max_length=50)
    add_date = models.DateTimeField('date published')

    def __str__(self):
        return self.list_name


class ListItem(models.Model):
    list_parent = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    item_text = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Sublist of...')

    def __str__(self):
        return self.item_text


mptt.register(ListItem)
