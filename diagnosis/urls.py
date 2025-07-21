from django.urls import path
from .views import symptom_checker, diagnosis_history
urlpatterns = [
    path('', symptom_checker, name='symptom_checker'),
    path('history/', diagnosis_history, name='history'),
]
