from django.urls import path
from .import views

urlpatterns = [
    path("compare/", views.compare_files_view, name='compare_files'),
]