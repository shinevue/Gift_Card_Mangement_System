from django.urls import path

from core import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("all-gcs/", views.AllGiftCardsTableView.as_view(), name="all-gift-cards"),
]
