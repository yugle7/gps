from math import atan

from geo.algo.city import City
from geo.data.position import Position
from django.db import models


# ---------------------------
# точка внутри полигона

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


class Polygon(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text='Город')

    d = models.DateField(help_text='День поиска')

    class Meta:
        ordering = ['id']

    # ---------------------------
    # точка внутри полигона

    def find(self, q):

        s = 0
        c = self.p[-1]

        x = c.x - q.x
        y = c.y - q.y

        b = Point(x, y)

        for c in self.p:
            x = c.x - q.x
            y = c.y - q.y
            a = Point(x, y)

            d = b.x * a.y - a.x * b.y
            xy = a.x * b.x + a.y * b.y

            s += atan((b.x * b.x + b.y * b.y - xy) / d)
            s += atan((a.x * a.x + a.y * a.y - xy) / d)

            b = a

        return abs(s) > 0.0001

    # ---------------------------
    # все люди внутри области за день

    def persons(self):
        s2xy = self.city.s2xy

        self.p = list(self.point_set.all())

        t = set()
        if len(self.p) > 2:

            d = self.d.toordinal()
            for s in range(self.city.n):
                x, y = s2xy(s)
                q = Point(x, y)

                if self.find(q):
                    t.update(q.person for q in Position.objects.filter(d=d, s=s))

        return list(t)
