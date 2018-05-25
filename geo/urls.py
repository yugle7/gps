from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from geo import views

# Create a router and register our viewsets with it.


router = DefaultRouter()

router.register(r'user', views.UserViewSet)
router.register(r'city', views.CityViewSet)

router.register(r'person', views.PersonViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'groups', views.GroupsViewSet)

router.register(r'location', views.LocationViewSet)
router.register(r'position', views.PositionViewSet)
router.register(r'way', views.WayViewSet)

router.register(r'track', views.TrackViewSet)
router.register(r'tracks', views.TracksViewSet)

router.register(r'attract', views.AttractViewSet)
router.register(r'attracts', views.AttractsViewSet)

router.register(r'point', views.PointViewSet)

router.register(r'polygon', views.PolygonViewSet)
router.register(r'circle', views.CircleViewSet)

router.register(r'act', views.ActViewSet)
router.register(r'acts', views.ActsViewSet)

router.register(r'build', views.BuildViewSet)
router.register(r'builds', views.BuildsViewSet)

router.register(r'place', views.PlaceViewSet)
router.register(r'places', views.PlacesViewSet)

router.register(r'holiday', views.HolidayViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.


urlpatterns = [
    url(r'^', include(router.urls))
]
