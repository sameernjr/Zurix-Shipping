from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='home'),
    path('About/', views.about_view),
    path('Contact/', views.contact_view, name='contact'),
]


