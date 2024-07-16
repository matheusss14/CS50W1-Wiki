from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("search", views.search, name="search"),
    path("edit", views.edit, name="edit"),
    path('save', views.save, name="save"),
    path('random', views.random, name="random"),
    path("wiki/<str:page>", views.page, name="page"),
]
