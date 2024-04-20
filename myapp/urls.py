from django.urls import path, re_path
from . import views
from .dialogue_views import show_dialogues, trigger_fetch_dialogues

urlpatterns = [
    path('', show_dialogues, name='home'),  # Сделать страницу диалогов главной страницей приложения
    path('dialogues/', show_dialogues, name='show_dialogues'),
    path('fetch-dialogues/', trigger_fetch_dialogues, name='fetch_dialogues'),
    path('search-dialogues/', views.search_dialogues, name='search_dialogues'),
    path('add-dialogue/', views.add_dialogue, name='add_dialogue'),
]
