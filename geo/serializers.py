from django.contrib.auth.models import User
from rest_framework import serializers

from geo.algo.attracts import Attracts
from geo.algo.circle import Circle
from geo.algo.city import City
from geo.algo.polygon import Polygon
from geo.algo.tracks import Tracks
from geo.calc.attract import Attract
from geo.calc.point import Point
from geo.calc.track import Track
from geo.data.location import Location
from geo.data.person import Person
from geo.data.position import Position
from geo.info.act import Act, Acts
from geo.info.build import Build, Builds
from geo.info.group import Group, Groups
from geo.info.holiday import Holiday
from geo.info.place import Place, Places
from geo.info.way import Way


# ----------------------------------


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('url', 'id', 'city', 'person', 'x', 'y', 'r', 't', 'position')
        extra_kwargs = {
            'position': {'read_only': True},
        }


class PositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Position
        fields = ('url', 'id', 'city', 'person', 'd', 't', 'h', 'x', 'y', 'r', 'b', 's', 'v', 'track', 'way')
        extra_kwargs = {
            'city': {'read_only': True},
            'person': {'read_only': True},
            'x': {'read_only': True},
            'y': {'read_only': True},
            'r': {'read_only': True},
            'd': {'read_only': True},
            't': {'read_only': True},
            'h': {'read_only': True},
            'b': {'read_only': True},
            's': {'read_only': True},
            'v': {'read_only': True},
            'track': {'read_only': True},
            'way': {'read_only': True},
        }


class WaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Way
        fields = ('url', 'key', 'v', 'h')


# ----------------------------------

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('url', 'id')


# ----------------------------------

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'is_staff', 'password', 'username', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# ----------------------------------

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'key')


class GroupsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Groups
        fields = ('url', 'group', 'person')


# ----------------------------------

class TracksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tracks
        fields = ('url', 'city', 'h', 't', 'v', 's', 'r')


class AttractsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attracts
        fields = ('url', 'city', 'person', 'd', 'h', 'n')


# ----------------------------------

class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ('url', 'person', 'a', 'b', 'h', 'n')


class AttractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attract
        fields = ('url', 'person', 'x', 'y', 'h', 'act')


# ----------------------------------

class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('url', 'key', 'x', 'y', 'width', 'height', 'step')


# ----------------------------------

class CircleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Circle
        fields = ('url', 'city', 'd', 'x', 'y', 'r')


class PolygonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Polygon
        fields = ('url', 'city', 'd')


# ----------------------------------

class PointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Point
        fields = ('url', 'x', 'y')


# ----------------------------------

class ActSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Act
        fields = ('url', 'key')


class ActsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Acts
        fields = ('url', 'city', 'act', 's', 'p')


# ----------------------------------

class BuildSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Build
        fields = ('url', 'key')


class BuildsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Builds
        fields = ('url', 'city', 'build', 's', 'p')


# ----------------------------------

class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = ('url', 'key')


class PlacesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Places
        fields = ('url', 'city', 'place', 's', 'p')


# ----------------------------------

class HolidaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Holiday
        fields = ('url', 'city', 'd')
