from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("<str:name>",views.page,name="page"),
    path("edit/<str:editPage>", views.edit_page, name="edit_page"),
    path("search/",views.search,name="search")

    
]
