from django.urls import path, include
from knox import views as knox_views
from .api import UserAPI, LoginAPI, RegisterAPI, AllUsersAPI


urlpatterns = [
    path('api/auth/register', RegisterAPI.as_view()),
    path("api/auth/login", LoginAPI.as_view()),
    path("api/auth/user", UserAPI.as_view()),
    path("api/auth/get_all_users", AllUsersAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(),name='knox_logout'),
    path('api/auth', include('knox.urls')),
]