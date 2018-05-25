from collections import deque, defaultdict
from datetime import date, datetime

from geo.algo.city import City
from geo.calc.track import Track
from geo.data.location import Location
from geo.data.position import Position

from django.db import models

# ----------------------------------
# объединение точек в треки
from geo.info.way import Way


class Tracks(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text='Город')

    h = models.IntegerField(default=10, help_text='Оценка времени нахождения в точке')

    t = models.IntegerField(default=120, help_text='Максимальное время между точками трека')

    v = models.FloatField(default=0.3, help_text='Максимальная скорость покоя')
    s = models.IntegerField(default=10, help_text='Минимальное время между точками трека')

    d = models.IntegerField(default=100, help_text='Минимальное расстояние до выброса')
    r = models.IntegerField(default=100, help_text='Максимальная погрешность')

    class Meta:
        ordering = ['id']

    # ----------------------------------
    # обработка точек

    def positions(self):
        def span(a, b):
            return (a.t - b.t).total_seconds()

        p = deque()
        d = defaultdict(list)

        self.holidays = {q.d for q in self.city.holiday_set.all()}

        for x in Location.objects.filter(position=False, city=self.city):
            while p and span(x, p[0]) > self.t:
                y = p.popleft()

                if d[y.person][-1] == y:
                    t = d.pop(y.person)

                    # ----------------------------------
                    # преобразуем

                    for q in t:
                        q.position = True
                        q.save()

                    a, b = t[0].t, t[-1].t
                    t = [Position(t=q.t.timestamp(), x=q.x, y=q.y, r=q.r, b=q.b) for q in t]
                    h = t[-1].t - t[0].t

                    track = Track.objects.create(person=y.person, h=h, a=a, b=b, n=len(t))

                    # ----------------------------------
                    # обрабатывем

                    self.outlier(t)
                    self.prune(t)
                    self.smooth(t)

                    # ----------------------------------
                    # вычисляем

                    self.V(t)
                    self.H(t)
                    self.S(t)

                    # ----------------------------------
                    # вычисляем способ перемещения

                    self.way(t)
                    self.moment(t)

                    # ----------------------------------
                    # присваиваем

                    for q in t:
                        q.city = self.city
                        q.person = y.person
                        q.track = track

                        q.d = date.fromtimestamp(q.t).toordinal()

                    # ----------------------------------

                    Position.objects.bulk_create(t)

            d[x.person].append(x)
            p.append(x)

    # ----------------------------------
    # выбросы

    def outlier(self, p):
        dist = self.city.dist
        i = j = len(p) - 1

        while i:
            i -= 1

            if p[i].r < self.r:
                d = dist(p[i], p[j])

                k = j - 1
                while k > i:
                    x = dist(p[i], p[k])
                    y = dist(p[k], p[j])
                    if x > self.d and y > self.d and x + y > 3 * d:
                        p.pop(k)
                        j -= 1
                    k -= 1
                j = i

    # ----------------------------------
    # прореживание

    def prune(self, p):
        span = self.city.span
        n = len(p) - 1

        i = 0
        while i < n:
            s = span(p[i], p[i + 1])

            if s < self.s:
                d = int(p[i].r < p[i + 1].r)
                p.pop(i + d)
                n -= 1
            else:
                i += 1

    # ----------------------------------
    # сглаживание

    def smooth(self, p):
        span = self.city.span
        n = len(p) - 1

        x = [q.x * self.city.lat for q in p]
        y = [q.y * self.city.lon for q in p]

        a, b = x[:], y[:]

        for k in range(2):
            u, v = a[:], b[:]

            for i in range(1, n):
                s = span(p[i - 1], p[i]) / span(p[i - 1], p[i + 1])

                a[i] = u[i - 1] + (u[i + 1] - u[i - 1]) * s
                b[i] = v[i - 1] + (v[i + 1] - v[i - 1]) * s

                r = ((a[i] - x[i]) ** 2 + (b[i] - y[i]) ** 2) ** 0.5
                s = ((x[i + 1] - x[i - 1]) ** 2 + (y[i + 1] - y[i - 1]) ** 2) ** 0.5

                if r > 0:
                    d = min(p[i].r, r) / (r + s)

                    a[i] = x[i] + (a[i] - x[i]) * d
                    b[i] = y[i] + (b[i] - y[i]) * d

        for i in range(1, n):
            p[i].x = a[i] / self.city.lat
            p[i].y = b[i] / self.city.lon

    # ----------------------------------
    # скорость

    def V(self, p):
        dist = self.city.dist
        span = self.city.span

        n = len(p) - 1

        i = 0
        while i < n:
            d = dist(p[i], p[i + 1])
            s = span(p[i], p[i + 1])

            p[i].v = d / s
            i += 1

    # ----------------------------------
    # остановки

    def H(self, p):
        span = self.city.span

        n = len(p) - 1

        if not n:  # одиночная точка
            q = p[0]

            q.h = self.h

        i = 0
        while i < n:
            if p[i].v < self.v:
                q = p.pop(i)
                n -= 1

                p[i].x = (p[i].x + q.x) / 2
                p[i].y = (p[i].y + q.y) / 2
                p[i].r = (p[i].r + q.r) / 2

                p[i].t = (q.t + p[i].t) / 2
                p[i].h = q.h + span(p[i], q)
            else:
                i += 1

    # ----------------------------------

    def S(self, p):
        xy2s = self.city.xy2s

        for q in p:
            q.s = xy2s(q.x, q.y)

    # ----------------------------------

    def way(self, p):
        span = self.city.span

        feet = Way.objects.get(key='feet')
        bike = Way.objects.get(key='bike')

        bus = Way.objects.get(key='bus')
        car = Way.objects.get(key='car')

        v = max(q.v for q in p)
        t = [feet, bike, bus, car][(v > feet.v) + (v > bike.v) + (v > bus.v)]

        for q in p: q.way = t

        if t != feet:
            i = j = 0
            while j < len(p):
                if p[j].v > feet.v:
                    if span(p[i], p[j]) > feet.h:
                        for k in range(i, j):
                            p[k].way = feet
                    j += 1
                    i = j
                else:
                    j += 1

            if span(p[i], p[-1]) > feet.h:
                for k in range(i, j):
                    p[k].way = feet

    def moment(self, p):
        for q in p:
            t = datetime.fromtimestamp(q.t)

            k = 7 if t.date() in self.holidays else t.weekday()
            q.m = k * 24 + t.hour
