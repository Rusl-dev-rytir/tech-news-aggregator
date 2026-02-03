from django.contrib import admin
from django.urls import path
from news.views import run_parser, index  # Импортируем ОБЕ функции

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),             # Главная страница (Показ новостей)
    path('parse/', run_parser),  # Ссылка для запуска парсера
]