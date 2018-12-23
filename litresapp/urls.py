from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list_view, name='book_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('page/<path:cursor>/', views.book_list_view, name='page'),
]
