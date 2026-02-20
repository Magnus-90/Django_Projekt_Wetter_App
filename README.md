# 🌤️ Wetter App

## 📝 Features
- Wetter Infos inerhalb der Schweiz
- Stündliche Temperatur und Druck Werte
- Tagesübersicht mit Minimum und Maximum Temperatur Werte
- Animierte Wettericons für verschiedene Wetterlagen
- Favoriten-System für eingeloggte Benutzer
- Benutzer System

## 🛠️ Technologien
- **Backend**: Django 6.0
- **Frontend**: HTML, CSS
- **Wetter API**: [Open-Meteo](https://open-meteo.com/) mit Meteoswiss Model für genauere Wetterdaten in der Schweiz
- **Datenbank**: SQLite
- **Wettericons**: [Meteocons](https://bas.dev/work/meteocons) Animierte Svg's

## ⚙️ Installation

1. **Repository klonen**
```bash
git clone 
cd wetterapp
```

2. **Virtuelle Umgebung erstellen und aktivieren**
```bash
python -m venv app1
app1\Scripts\activate  # Windows
source app1/bin/activate  # Mac/Linux
```

3. **Abhängigkeiten installieren**
```bash
pip install -r requirements.txt
```

4. **Datenbank migrieren**
```bash
python manage.py migrate
```

5. **Superuser erstellen**
```bash
python manage.py createsuperuser
```

6. **Server starten**
```bash
python manage.py runserver
```
