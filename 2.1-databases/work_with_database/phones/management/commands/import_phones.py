import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from phones.models import Phone

class Command(BaseCommand):
    help = 'Import phones from CSV file'

    def handle(self, *args, **options):
        # Файл phones.csv находится в корне проекта
        csv_file = 'phones.csv'
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            for row in reader:
                phone_data = {
                    'id': int(row['id']),
                    'name': row['name'],
                    'price': int(row['price']),
                    'image': row['image'],
                    'release_date': parse_date(row['release_date']),
                    'lte_exists': row['lte_exists'].lower() == 'true'
                }
                 
                phone = Phone(**phone_data)
                phone.save()
                self.stdout.write(f'Imported: {phone.name}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported all phones')
            )