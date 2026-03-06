from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/analyze/", views.api_analyze, name="api_analyze"),
    path("api/model_labels/", views.api_model_labels, name="api_model_labels"),
    path("signup/", views.signup, name="signup"),
]