from math import pi, sin, cos
from datetime import datetime, date
from random import random

from django.shortcuts import redirect
import pytz

from geo.algo.city import City
from geo.algo.polygon import Polygon
from geo.algo.tracks import Tracks
from geo.calc.attract import Attract
from geo.calc.point import Point
from geo.calc.track import Track
from geo.data.location import Location
from geo.data.person import Person
import csv

from geo.data.position import Position
from geo.info.act import Act
from geo.info.group import Groups, Group
from geo.info.holiday import Holiday
from geo.info.way import Way


# ----------------------------------

def city():
    City.objects.all().delete()
    city = City.objects.create(key='moscow', y=55.905169, x=37.314064, step=100, width=30000, height=40000)

    Tracks.objects.create(city=city)


# ----------------------------------

def track():
    Location.objects.all().delete()

    for q in open('geo/test/track.txt'):
        y, x, t, r, pk = q[:-1].split('\t')

        x, y = float(x), float(y)
        t = datetime.fromtimestamp(int(t))
        r = int(r)
        person = Person.objects.get(pk=int(pk))

        Location(person=person, x=x, y=y, t=t, r=r).save()


def polygon():
    Point.objects.all().delete()
    Polygon.objects.all().delete()

    city = City.objects.get(key='moscow')
    polygon = Polygon.objects.create(city=city, d=date.today())

    y, x, r, n = open('geo/test/polygon.txt').read().split()

    p = Point(x=float(x), y=float(y))
    r, n = int(r), int(n)

    s = []
    f = 0
    while f < pi:
        d = r + r * random()

        x = p.x + d * sin(2 * f) / city.lat
        y = p.y + d * cos(2 * f) / city.lon

        s.append(Point(x=x, y=y, polygon=polygon))

        f += pi / n

    Point.objects.bulk_create(s)


def person():
    Groups.objects.all().delete()
    Person.objects.all().delete()

    persons = [Person(pk=i) for i in range(20)]
    Person.objects.bulk_create(persons)


def location():
    Location.objects.all().delete()
    Position.objects.all().delete()

    Track.objects.all().delete()
    Attract.objects.all().delete()

    src = open('geo/test/location.csv')
    locations = []

    for d in csv.reader(src, delimiter=';', quotechar='"'):
        pk = int(d[11])
        dt = d[16]
        x = float(d[6])
        y = float(d[5])
        r = float(d[12])
        b = d[21] == 't'

        d, t = dt.split('T')

        Y, M, D = d.split('-')
        H, min, sec = t.split(':')
        sec, micro = sec.split('.')

        Y, M, D, H, min, sec, micro = map(int, [Y, M, D, H, min, sec, micro])

        t = datetime(Y, M, D, H, min, sec, micro * 1000, tzinfo=pytz.UTC)
        person = Person.objects.get(pk=pk)

        q = Location(person=person, x=x, y=y, t=t, r=r, b=b)
        if q.set_city(): locations.append(q)

    Location.objects.bulk_create(locations)


def holiday():
    Holiday.objects.all().delete()
    city = City.objects.get(key='moscow')

    src = open('geo/test/holiday.txt')
    holidays = []

    for q in src.readlines():
        Y, M, D = q.split('-')
        d = date(int(Y), int(M), int(D))

        holidays.append(Holiday(city=city, d=d))
    src.close()

    Holiday.objects.bulk_create(holidays)


def way():
    Way.objects.all().delete()

    Way(key='feet', v=2.7, h=300).save()
    Way(key='bike', v=9, h=300).save()
    Way(key='bus', v=19, h=300).save()
    Way(key='car', v=33, h=300).save()


def act():
    Act.objects.all().delete()

    Act(key='visit').save()
    Act(key='work').save()
    Act(key='live').save()


def group():
    Group.objects.all().delete()
    Group(key='test').save()


def init(request):
    city()
    person()
    group()
    act()
    way()
    holiday()
    location()
    polygon()

    return redirect('/')
