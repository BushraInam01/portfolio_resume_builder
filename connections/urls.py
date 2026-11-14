from django.urls import path

from .views import (
    ConnectionListView,
    SendConnectionRequestView,
    ConnectionRequestActionView,
)

app_name = "connections"

urlpatterns = [
    path("", ConnectionListView.as_view(), name="list"),
    path("send/<int:user_id>/", SendConnectionRequestView.as_view(), name="send_request"),
    path("<int:connection_id>/<str:action>/", ConnectionRequestActionView.as_view(), name="request_action"),
]
