from django.urls import path

from dispenser import views

urlpatterns = [
    path(
        "denomination-select/",
        views.DenominationSelectView.as_view(),
        name="denomination-select",
    ),
    path(
        "card/<int:denomination>",
        views.GiftCardDetailRedirectView.as_view(),
        name="gc-redirect",
    ),
    path(
        "detail/<int:pk>",
        views.GiftCardUpdateView.as_view(),
        name="gc-detail-update",
    ),
]
