from django.urls import path
from gpt import views


urlpatterns = [
    path('chat/', views.OpenAIChatView.as_view(), name='openai-chat'),

]
