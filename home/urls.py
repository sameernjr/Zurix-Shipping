from django.urls import path
from . import views

# app_name = 'index'

urlpatterns = [
    path('', views.index_view, name='home'),
    path('About/', views.about_view , name='about'),
    path('Contact/', views.contact_view, name='contact'),
]


