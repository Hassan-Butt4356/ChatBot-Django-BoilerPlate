from django.urls import path
from myapp.views import chatbot
urlpatterns = [
    path('',chatbot,name="chatbot"),
]
