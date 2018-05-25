from builtins import set

from geo.algo.city import City
from geo.calc.point import Point
from geo.data.person import Person
from geo.data.position import Position
from django.db import models


# ---------------------------
# точка внутри области


class Circle(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text='Город')

    x = models.FloatField(help_text='Долгота')
    y = models.FloatField(help_text='Широта')

    r = models.IntegerField(help_text='Радиус')
    d = models.DateField(help_text='День поиска')

    class Meta:
        ordering = ['id']

    # ---------------------------

    def find(self, q):
        return self.city.dist(q, self) < self.r

    # ---------------------------
    # все люди внутри области за день

    def persons(self):
        s2xy = self.city.s2xy

        t = set()
        d = self.d.toordinal()
        for s in range(self.city.n):
            x, y = s2xy(s)
            q = Point(x=x, y=y)
            if self.find(q):
                t.update(q.person for q in Position.objects.filter(d=d, s=s))

        return list(t)
