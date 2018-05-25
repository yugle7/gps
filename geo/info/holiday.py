from django.db import models
from geo.algo.city import City


# ----------------------------------
# выходные дни


class Holiday(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text='Город')
    d = models.DateField(help_text='Дата')

    def __str__(self):
        return self.d

    class Meta:
        ordering = ['d']
