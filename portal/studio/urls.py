from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('myorders/', views.LoanedOrdersByUserListView.as_view(), name='my-order'),
    path(r'customer/', views.LoanedOrdersAllListView.as_view(), name='all-order'),
    path('order/create/', views.OrderCreate.as_view(), name='order-create'),
    path('order/<int:pk>/update/', views.OrderUpdate.as_view(), name='order-update'),
]
