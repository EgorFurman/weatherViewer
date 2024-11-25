from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search')
]
