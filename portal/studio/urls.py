from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', views.StudioLoginView.as_view(), name='login'),
]
