from rest_framework import permissions, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from geo.serializers import *

from django.contrib import admin
from django.shortcuts import redirect

admin.autodiscover()


# ----------------------------------
# пользователь

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (
        permissions.IsAdminUser,
    )


# ----------------------------------
# положение

class CityViewSet(viewsets.ModelViewSet):
    """
    read: Город (место)
    create: Добавление города
    positions: Точки внутри города
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = City.objects.all()
    serializer_class = CitySerializer

    @detail_route()
    def positions(self, request, pk=None):
        city = City.objects.get(pk=pk)
        queryset = city.position_set.all()
        serializer = PositionSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)


# ----------------------------------
# люди

class PersonViewSet(viewsets.ModelViewSet):
    """
    list: Люди
    read: Человек
    create: Создание человека
    groups: Список групп человека
    positions: Координаты
    attracts: Точки притяжения
    tracks: Треки
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @detail_route()
    def groups(self, request, pk=None):
        person = Person.objects.get(pk=pk)
        queryset = [q.group for q in person.groups_set.all()]
        serializer = GroupSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)

    @detail_route()
    def positions(self, request, pk=None):
        person = Person.objects.get(pk=pk)
        queryset = person.position_set.all()
        serializer = PositionSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)

    @detail_route()
    def attracts(self, request, pk=None):
        person = Person.objects.get(pk=pk)
        queryset = person.attract_set.all()
        serializer = AttractSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)

    @detail_route()
    def tracks(self, request, pk=None):
        person = Person.objects.get(pk=pk)
        queryset = person.track_set.all()
        serializer = TrackSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    list: Группы
    read: Группа
    create: Создание группы
    persons: Люди из группы
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @detail_route()
    def persons(self, request, pk=None):
        group = Group.objects.get(pk=pk)
        queryset = [q.person for q in group.groups_set.all()]
        serializer = PersonSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)


class GroupsViewSet(viewsets.ModelViewSet):
    """
    create: Добавление человека в группу
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer


# ----------------------------------
# точки

class LocationViewSet(viewsets.ModelViewSet):
    """
    create: Помещение исходной точки в систему
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class PositionViewSet(viewsets.ModelViewSet):
    """
    list: Все обработанные точки
    read: Обработанная точка
    """

    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----------------------------------
# способ перемещения (пешком, метро, машина, автобус)


class WayViewSet(viewsets.ModelViewSet):
    """
    create: Добавление способа перемещения
    positions: Точки
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Way.objects.all()
    serializer_class = WaySerializer

    @detail_route()
    def positions(self, request, pk=None):
        way = Way.objects.get(pk=pk)
        queryset = way.position_set.all()
        serializer = PositionSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)


# ----------------------------------
# треки

class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Треки
    read: Трек
    positions: Точки трека
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    @detail_route()
    def positions(self, request, pk=None):
        track = Track.objects.get(pk=pk)
        queryset = track.position_set.all()
        serializer = PositionSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)


class TracksViewSet(viewsets.ModelViewSet):
    """
    read: Параметры формирования треков
    create: Задать параметры обработки точек
    positions: Обработка точек (сбор треков)
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Tracks.objects.all()
    serializer_class = TracksSerializer

    @detail_route()
    def positions(self, request, pk=None):
        tracks = Tracks.objects.get(pk=pk)
        tracks.positions()
        return redirect('/')


# ----------------------------------
# точки притяжения

class AttractViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Список точек притяжения
    read: Точка притяжения
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Attract.objects.all()
    serializer_class = AttractSerializer


class AttractsViewSet(viewsets.ModelViewSet):
    """
    create: Поиск точек притяжения
    """
    permission_classes = [permissions.IsAuthenticated]

    queryset = Attracts.objects.all()
    serializer_class = AttractsSerializer


# ----------------------------------
# множества точек

class PointViewSet(viewsets.ModelViewSet):
    """
    create: Создание точки
    read: Точка на карте
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Point.objects.all()
    serializer_class = PointSerializer


# ----------------------------------
# область

class CircleViewSet(viewsets.ModelViewSet):
    """
    create: Задание области в форме круга
    read: Круг
    persons: Люди внутри круга
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Circle.objects.all()
    serializer_class = CircleSerializer

    @detail_route()
    def persons(self, request, pk=None):
        circle = Circle.objects.get(pk=pk)
        queryset = circle.persons()
        serializer = PersonSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)


class PolygonViewSet(viewsets.ModelViewSet):
    """
    create: Задание области в форме круга
    read: Полигон
    persons: Люди внутри полигона
    points: Вершны полигона
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer

    @detail_route()
    def persons(self, request, pk=None):
        polygon = Polygon.objects.get(pk=pk)

        queryset = polygon.persons()
        serializer = PersonSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)

    @detail_route()
    def points(self, request, pk=None):
        polygon = Polygon.objects.get(pk=pk)

        queryset = polygon.point_set.all()
        serializer = PointSerializer(data=queryset, many=True, context={'request': request})
        serializer.is_valid()
        return Response(serializer.data)


# ----------------------------------
# активность

class ActViewSet(viewsets.ModelViewSet):
    """
    create: Добавление вида активности
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Act.objects.all()
    serializer_class = ActSerializer


class ActsViewSet(viewsets.ModelViewSet):
    """
    create: Активность в квадрате
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Acts.objects.all()
    serializer_class = ActsSerializer


# ----------------------------------
# строения (остановка, парковка, театр)


class BuildViewSet(viewsets.ModelViewSet):
    """
    create: Добавление типа строения
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Build.objects.all()
    serializer_class = BuildSerializer


class BuildsViewSet(viewsets.ModelViewSet):
    """
    create: Строение в квадрате
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Builds.objects.all()
    serializer_class = BuildsSerializer


# ----------------------------------
# местность (парк, дорога, дом, офис)


class PlaceViewSet(viewsets.ModelViewSet):
    """
    create: Добавление типа местности
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlacesViewSet(viewsets.ModelViewSet):
    """
    create: Местность в квадрате
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Places.objects.all()
    serializer_class = PlacesSerializer


# ----------------------------------

class HolidayViewSet(viewsets.ModelViewSet):
    """
    create: Добавить выходной
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
