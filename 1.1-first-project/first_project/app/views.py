from django.shortcuts import render
from django.http import HttpResponse
import os
from datetime import datetime

def home_view(request):
    # Домашняя страница со списком доступных страниц
    pages = [
        {'name': 'Главная страница', 'url': '/'},
        {'name': 'Текущее время', 'url': '/current_time/'},
        {'name': 'Содержимое рабочей директории', 'url': '/workdir/'}
    ]
    
    # Используем шаблон (если он есть) или возвращаем простой HTML
    return render(request, 'home.html', {'pages': pages})

def current_time_view(request):
    # Показываем текущее время
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"Текущее время: {current_time}")

def workdir_view(request):
    # Выводим содержимое рабочей директории
    try:
        # Получаем список файлов и папок в текущей директории
        files = os.listdir('.')
        files_list = "<h1>Содержимое рабочей директории:</h1><ul>"
        
        for file in files:
            files_list += f"<li>{file}</li>"
            
        files_list += "</ul>"
        return HttpResponse(files_list)
    except Exception as e:
        return HttpResponse(f"Ошибка при чтении директории: {e}")