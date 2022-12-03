from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from .views import CategoryListView, PostByCategoryView


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('myorders/', views.LoanedOrdersByUserListView.as_view(), name='my-order'),
    path('myorders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path(r'customer/', views.LoanedOrdersAllListView.as_view(), name='all-order'),
    path('order/create/', views.OrderCreate.as_view(), name='order-create'),
    path('myorders/<int:pk>/update/', views.OrderUpdate.as_view(), name='order-update'),
    path('myorders/<int:pk>/delete/', views.OrderUserDelete.as_view(), name='order-delete'),
    path('myorders/<int:pk>/delete/', views.OrderAdminDelete.as_view(), name='order-delete'),
    path('admin/', admin.site.urls),
    path('', CategoryListView.as_view(), name='category-list'),
    path('<str:slug>/', PostByCategoryView.as_view(), name='post-by-category'),
]
