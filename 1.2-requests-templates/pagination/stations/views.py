from django.core.paginator import Paginator
from django.shortcuts import render
import csv
from django.conf import settings

def bus_stations(request):
    # Получаем номер страницы из GET-параметра, по умолчанию 1
    page_number = request.GET.get('page', 1)
    
    # Чтение данных из CSV файла
    stations = []
    try:
        with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stations.append({
                    'Name': row['Name'],
                    'Street': row['Street'],
                    'District': row['District']
                })
    except FileNotFoundError:
        # Если файл не найден, используем тестовые данные
        stations = [
            {'Name': 'Тестовая остановка 1', 'Street': 'Улица Тестовая', 'District': 'Район Тестовый'},
            {'Name': 'Тестовая остановка 2', 'Street': 'Улица Пример', 'District': 'Район Пример'},
        ]
    
    # Создаем пагинатор - 10 элементов на страницу
    paginator = Paginator(stations, 10)
    
    # Получаем запрошенную страницу
    page = paginator.get_page(page_number)
    
    # Формируем контекст
    context = {
        'bus_stations': page, 
        'page': page  
    }
    
    return render(request, 'stations/index.html', context)