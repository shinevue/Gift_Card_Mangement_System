from django.urls import path

from collector import views

urlpatterns = [
    path("collectgc/", views.GiftCardCollectorView.as_view(), name="gc-collector")
]
