from math import cos, pi
from django.db import models


# ---------------------------

class City(models.Model):
    key = models.CharField(max_length=30, primary_key=True, help_text='Название')

    # ---------------------------

    x = models.FloatField(default=37.630752, help_text='Долгота')
    y = models.FloatField(default=55.827488, help_text='Широта')

    width = models.IntegerField(default=1460, help_text='Ширина')
    height = models.IntegerField(default=1130, help_text='Длина')

    # ---------------------------

    lon = models.FloatField(default=111111, help_text='метров в одном градусе по долготе (в центре карты)')
    lat = models.FloatField(help_text='метров в одном градусе по широте')

    cy = models.FloatField()
    cx = models.FloatField()

    # ---------------------------

    step = models.IntegerField(default=100, help_text='шаг в метрах')

    dx = models.FloatField()
    dy = models.FloatField()

    rows = models.IntegerField()  # размеры карты
    cols = models.IntegerField()

    a = models.FloatField()
    b = models.FloatField()

    n = models.IntegerField()

    # ---------------------------
    # скорости

    stop = models.FloatField(default=0.3)
    walk = models.FloatField(default=2)
    bike = models.FloatField(default=6)
    bus = models.FloatField(default=14)
    car = models.FloatField(default=30)

    # ---------------------------

    def __str__(self):
        return self.key

    class Meta:
        ordering = ['key']

    def save(self, *args, **kwargs):
        self.cy = self.y + self.height / (2 * self.lon)
        self.lat = self.lon * cos(pi * self.cy / 180)
        self.cx = self.x + self.width / (2 * self.lat)

        self.dx = self.step / self.lat
        self.dy = self.step / self.lon

        self.rows = self.height // self.step  # размеры карты
        self.cols = self.width // self.step

        self.a = self.x + self.dx * self.cols
        self.b = self.y - self.dy * self.rows

        self.n = self.cols * self.rows

        assert self.n

        super(City, self).save(*args, **kwargs)

    # ---------------------------
    # определение квадрата точки

    def xy2s(self, x, y):
        x = int((x - self.x) / self.dx)
        y = int((self.y - y) / self.dy)
        s = y * self.cols + x
        assert 0 <= s < self.n
        return s

    def s2xy(self, s):
        assert 0 <= s < self.n
        y, x = divmod(s, self.cols)

        x = (x * self.dx + self.dx / 2) + self.x
        y = self.y - (y * self.dx + self.dy / 2)

        return x, y

    # ---------------------------
    # проверка находится ли точка внутри карты

    def inside(self, q):
        return self.x <= q.x < self.a and self.b < q.y <= self.y

    # ---------------------------
    # расстояние между точками

    def dist(self, a, b):
        return ((self.lat * (a.x - b.x)) ** 2 + (self.lon * (a.y - b.y)) ** 2) ** 0.5

    # ---------------------------
    # время в пути между точками

    def span(self, a, b):
        return abs(b.t - a.t)
