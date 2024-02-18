from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('customer/<int:pk>', views.customer_record, name="customer"),
    path('delete_customer/<int:pk>', views.delete_customer, name="delete_customer"),
    path('edit_customer/<int:pk>', views.edit_customer, name="edit_customer"),
    path('add_customer', views.add_customer, name="add_customer"),
]
