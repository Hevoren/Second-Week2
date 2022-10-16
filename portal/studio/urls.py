from django.urls import path
from . import views

urlpatterns = [
    path('accounts/profile/order-create/<int:pk>', views.OrderCreate.as_view(), name='order-create'),
    path('accounts/profile/order-create', views.OrderCreate.as_view(), name='order-create'),
    path('accounts/register/done/', views.RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', views.StudioLogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login', views.StudioLoginView.as_view(), name='login'),
    path('', views.index, name='index'),
]
