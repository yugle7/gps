from django.db import models
from geo.data.person import Person
from geo.info.way import Way


# ----------------------------------
# трек


class Track(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Человек')

    a = models.DateTimeField(help_text='Начало')
    b = models.DateTimeField(help_text='Конец')

    h = models.FloatField(help_text='Продолжительность')
    n = models.IntegerField(help_text='Точек')

    class Meta:
        ordering = ['id']

