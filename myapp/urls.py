# myproject/myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_dialogues, name='home'),  # Сделать страницу диалогов главной страницей приложения
    path('load-dialogues-from-telegram/', views.load_dialogues, name='load-dialogues-from-telegram'),
    path('delete-dialogue/', views.delete_dialogue, name='delete-dialogue'),
    path('search-dialogues/', views.search_dialogues, name='search-dialogues'),
    path('add-dialogue/', views.add_dialogue, name='add-dialogue'),
    path('load-dialogues/', views.fetch_and_save_messages, name='load-dialogues'),
    path('get-recent-messages/', views.get_recent_messages, name='get-recent-messages'),  # Новый маршрут
]
