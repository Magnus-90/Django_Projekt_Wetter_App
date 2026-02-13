from django.apps import apps
from django.db import migrations
import csv
import os

def migrate_cities_from_csv(apps, schema_editor):
    CityModel = apps.get_model('wetterapp', 'City')
    with open("AMTOVZ_CSV_WGS84.csv", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            adressenanteil = float(row['Adressenanteil'].replace('%', '').strip())
            if adressenanteil > 50:
                print(row['Ortschaftsname'], row['PLZ4'], row['Adressenanteil'], row['E'], row['N'])
                CityModel.objects.create(
                    name=row['Ortschaftsname'],
                    plz=row['PLZ4'],
                    latitude=row['N'],
                    longitude=row['E']
                    )

class Migration(migrations.Migration):

    dependencies = [
        ('wetterapp', '0004_city_plz_alter_city_country'),
    ]

    operations = [
        migrations.RunPython(migrate_cities_from_csv)
    ]
