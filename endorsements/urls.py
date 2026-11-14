from django.urls import path

from .views import EndorseSkillView


app_name = "endorsements"

urlpatterns = [
    path("skill/<int:skill_id>/", EndorseSkillView.as_view(), name="endorse_skill"),
]