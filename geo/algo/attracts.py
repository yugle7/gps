from geo.algo.city import City
from geo.calc.attract import Attract
from django.db import models
from geo.data.person import Person

# ---------------------------
# поиск точек притяжения
from geo.info.act import Act


class Attracts(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, help_text='Город')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, help_text='Человек')

    d = models.IntegerField(default=200, help_text='Минимальное расстояние между точками притяжения')

    h = models.IntegerField(default=100, help_text='Минимальное время в точке притяжения')
    n = models.IntegerField(default=5, help_text='Максимальное количество точек притяжения')

    class Meta:
        ordering = ['id']

    # ---------------------------

    def save(self, *args, **kwargs):
        self.person.attract_set.all().delete()

        p = self.person.position_set.filter(h__gt=1, city=self.city)

        self.a = [Attract(x=q.x, y=q.y, h=q.h) for q in p]  # точки притяжения
        self.c = list(range(len(self.a)))  # номера кластеров точек

        self.cluster()  # кластеризуем точки
        a = self.find()  # берем несколько точек притяжения

        if a:
            self.act(a, p)  # определяем активность

            for q in a:
                q.person = self.person
                q.city = self.city

            Attract.objects.bulk_create(a)

        super(Attracts, self).save(*args, **kwargs)

    # ---------------------------

    def cluster(self):
        dist = self.city.dist

        t = []
        for i in range(len(self.a)):
            for j in range(i + 1, len(self.a)):
                t.append((dist(self.a[i], self.a[j]), i, j))
        t.sort()

        for d, i, j in t:
            x, y = self.get(i), self.get(j)
            if x != y and dist(self.a[x], self.a[y]) < self.d:
                self.a[x].merge(self.a[y])
                self.c[y] = x
        t.clear()

    # ---------------------------

    def find(self):
        a = [q for i, q in enumerate(self.a) if q.h > self.h and self.c[i] == i]
        a.sort(key=lambda q: -q.h)

        a = a[: self.n]
        for q in a:
            q.person = self.person
            q.city = self.city

        return a

    # ---------------------------

    def act(self, a, p):
        dist = self.city.dist

        for t in a:
            t.live = t.work = 0
            t.act = Act.objects.get(key='visit')

        for q in p:
            for t in a:
                if dist(q, t) < self.d:
                    d, h = divmod(q.m, 24)
                    if d < 5:
                        k = (8 < h < 20) + (10 < h < 18)
                        t.work += k
                        t.live += 2 - k
                    else:
                        t.work -= 1
                        t.live += 1

        live = Act.objects.get(key='live')
        work = Act.objects.get(key='work')

        if len(a) == 1:
            a[0].act = live if a[0].live > a[0].work else work

        else:
            a.sort(key=lambda t: t.live)
            if a[-1].live > a[-1].work: a[-1].act = live

            a.sort(key=lambda t: t.work)
            if a[-1].work > a[-1].live: a[-1].act = work

    # ---------------------------

    def get(self, i):
        if self.c[i] != i:
            self.c[i] = self.get(self.c[i])
        return self.c[i]
