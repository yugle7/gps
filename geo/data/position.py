from django.db import models

from geo.algo.city import City
from geo.calc.track import Track
from geo.data.person import Person
from geo.info.way import Way


# ----------------------------------
# обработанная точка


class Position(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text='Город')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Человек')

    t = models.FloatField(help_text='Время')
    m = models.IntegerField(help_text='Момент')
    d = models.IntegerField(help_text='День')
    h = models.FloatField(default=0, help_text='Проведенное в точке время')

    x = models.FloatField(help_text='Долгота')
    y = models.FloatField(help_text='Широта')
    r = models.FloatField(help_text='Погрешность')

    b = models.BooleanField(default=False, help_text='Заряжается')

    s = models.IntegerField(help_text='Квадрат')
    v = models.FloatField(default=0, help_text='Скорость')

    track = models.ForeignKey(Track, on_delete=models.CASCADE, help_text='Трек')
    way = models.ForeignKey(Way, blank=True, null=True, on_delete=models.CASCADE, help_text='Метод передвижения')

    class Meta:
        ordering = ['id']