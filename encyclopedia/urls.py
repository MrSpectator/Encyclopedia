from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.entry, name="entry"),
    path("newpage/", views.newpage, name="newpage"),
    path("edit/<str:name>/", views.edit, name="edit"),
    path("random/", views.random, name="random"),
    path("search/", views.search, name="search"),
]
