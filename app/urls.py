from django.urls import path,include
from rest_framework import views
from .views import LeaderViewSet 
from rest_framework.routers import DefaultRouter

app_name = 'app'

router = DefaultRouter()
router.register('', LeaderViewSet, basename='leader')

urlpatterns = [
    path('', include(router.urls)),
    # path('checkleaderuuid', CheckUUID.as_view(), name='checkleaderuuid')
]



