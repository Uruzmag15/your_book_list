from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
