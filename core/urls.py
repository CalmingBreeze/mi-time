from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("practices/", views.practices, name="practices"),
    path("practices/<slug:practice_slug>/", views.practiceBySlug, name="practice"),
    #path("practice/<int:practice_id>/", views.practice, name="practice"),
    path("massages/", views.massages, name="massages"),
    path("massages/<slug:massage_slug>/", views.massageBySlug, name="massage"),
    #path("massage/<int:massage_id>/", views.massageById, name="massage"),
]