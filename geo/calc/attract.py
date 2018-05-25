from django.db import models
from geo.data.person import Person
from geo.info.act import Act


# ----------------------------------
# точка притяжения


class Attract(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Человек')

    x = models.FloatField(help_text='Долгота')
    y = models.FloatField(help_text='Широта')

    h = models.IntegerField(help_text='Проведенное в точке время')
    act = models.ForeignKey(Act, blank=True, null=True, on_delete=models.CASCADE, help_text='Активность')

    class Meta:
        ordering = ['id']

    # ----------------------------------

    def merge(self, q):
        self.x = self.h * self.x + q.h * q.x
        self.y = self.h * self.y + q.h * q.y

        self.h += q.h
        self.x /= self.h
        self.y /= self.h
