from django.urls import path
from .views import *

urlpatterns = [
    path('teams/',TeamsView.as_view()),
    path('sprints/',SprintView.as_view()),
    path('metrics/<team_name>/<sprint_name>/',metricsView.as_view()),
    path('chatbot/',ChatbotView.as_view())
]