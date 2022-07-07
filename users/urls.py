from django.urls import path
from rest_framework import views
from .views import CustomUserCreate, BlacklistTokenUpdateView  , UpdateUser , UserDetail

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('update_user/<int:pk>/', UpdateUser.as_view() , name='update_user'),
    path('<int:pk>/', UserDetail.as_view(), name='user_detail')
]
