from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout'),

    path('delete-note', views.delete_note, name='delete_note'),
]