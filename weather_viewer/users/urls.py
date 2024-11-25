from django.contrib.auth.views import LogoutView
from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserAuthorizationView.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='registration'),
]
