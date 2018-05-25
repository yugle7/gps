from django.db import models
from geo.data.person import Person


# ----------------------------------
# группа человека (старики, москвичи)


class Group(models.Model):
    key = models.CharField(max_length=20, primary_key=True, help_text='Название')

    def __str__(self):
        return self.key

    class Meta:
        ordering = ['key']

# ----------------------------------

class Groups(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Человек')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, help_text='Группа')

    class Meta:
        ordering = ['id']
