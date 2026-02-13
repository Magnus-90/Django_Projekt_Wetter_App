import csv
with open("AMTOVZ_CSV_WGS84.csv", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        adressenanteil = float(row['Adressenanteil'].replace('%', '').strip())
        if adressenanteil > 50:
            print(row['Ortschaftsname'], row['PLZ4'], row['Adressenanteil'], row['E'], row['N'])
            City.objects.create(
                name=row['Ortschaftsname'],
                plz=row['PLZ4']
                latitude=row['N'],
                longitude=row['E']
            )
