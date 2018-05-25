from django.db import models


# ----------------------------------
# способ перемещения (пешком, метро, машина, автобус)


class Way(models.Model):
    key = models.CharField(max_length=20, primary_key=True, help_text='Название')

    h = models.IntegerField(default=300, help_text='Характерное время движения')
    v = models.FloatField(default=2, help_text='Максимальная скорость')

    def __str__(self):
        return self.key

    class Meta:
        ordering = ['key']
