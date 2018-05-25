from django.db import models

from geo.algo.polygon import Polygon
from geo.info.group import Group


# ---------------------------
# точка с координатами


class Point(models.Model):
    x = models.FloatField(help_text='Долгота')
    y = models.FloatField(help_text='Широта')

    polygon = models.ForeignKey(Polygon, blank=True, null=True, on_delete=models.CASCADE, help_text='Полигон')

    class Meta:
        ordering = ['id']