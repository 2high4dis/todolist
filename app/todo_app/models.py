from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class ToDoList(models.Model):
    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE)
    list_name = models.CharField(max_length=50, blank=True)
    add_date = models.DateTimeField('date published')
    finished = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.list_name


class ListItem(MPTTModel):
    list_parent = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    item_text = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Subitem of...')

    class MPTTMeta:
        order_insertion_by = ['item_text']

    def __str__(self):
        return self.item_text
