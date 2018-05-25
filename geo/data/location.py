from django.db import models

from geo.algo.city import City
from geo.data.person import Person
from geo.data.position import Position


# ----------------------------------
# исходная точка


class Location(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text='Город')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Человек')

    t = models.DateTimeField(help_text='Время получения')

    x = models.FloatField(help_text='Долгота')
    y = models.FloatField(help_text='Широта')
    r = models.FloatField(help_text='Погрешность')

    b = models.BooleanField(default=False, help_text='Заряжается')

    position = models.BooleanField(default=False, help_text='Обработана ли точка')

    # ----------------------------------
    # определяем город

    def set_city(self):
        for city in City.objects.all():
            if city.inside(self):
                self.city = city
                return True
        return False

    def save(self, *args, **kwargs):
        self.set_city()
        super(Location, self).save(*args, **kwargs)

    class Meta:
        ordering = ["t"]
