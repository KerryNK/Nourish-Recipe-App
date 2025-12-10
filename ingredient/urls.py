from django.urls import path
from . import views

app_name = 'ingredient'

urlpatterns = [
    path('ai/', views.ai_view, name='ai'),
    path('statistic/', views.statistic_view, name='statistic'),
]
