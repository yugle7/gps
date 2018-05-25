from django.db import models
from geo.algo.city import City


# ----------------------------------
# активность (живет, работает, гуляет, посещает)


class Act(models.Model):
    key = models.CharField(max_length=20, primary_key=True, help_text='Название')

    def __str__(self):
        return self.key

    class Meta:
        ordering = ['key']


# ----------------------------------

class Acts(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text='Город')
    act = models.ForeignKey(Act, on_delete=models.CASCADE, help_text='Активность')

    s = models.IntegerField(help_text='Квадрат')
    p = models.FloatField(default=1, help_text='Уверенность')

    class Meta:
        ordering = ['id']