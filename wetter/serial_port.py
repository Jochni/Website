#!/usr/bin/env python3

import serial
import webbrowser
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Zeit abrufen
now = datetime.now().replace(microsecond=0)

# Öffne die serielle Verbindung
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=3)

# Überprüfe, welcher Port verwendet wird
print(ser.name)

# Leere den Puffer
ser.flush()

# Listen für Temperatur und Feuchtigkeit
temperaturen = []
feuchtigkeiten = []

# Zeit und Datum als String formatieren
zeit_als_string = now.strftime("%d/%m/%Y %H:%M:%S")

# In eine Datei schreiben
with open('/var/www/html/wetter/zeit.txt', 'w') as f:
    f.write(zeit_als_string)

# Öffne die Textdatei im Schreibmodus
with open('/var/www/html/wetter/daten.txt', 'w') as f:
    for i in range(1, 4):
        th = ser.readline()
        ths = th.split()
        if len(ths) == 2:
            if ths[0].decode('ascii') == 'Temperature:':
                temp = float(ths[1])
                temperaturen.append(temp)
                f.write(f'{i},{temp},')
            if ths[0].decode('ascii') == 'Humidity:':
                humidity = float(ths[1])
                feuchtigkeiten.append(humidity)
                f.write(f'{humidity}\n')

# Öffne die Textdateien im Anhängemodus ('a')
with open('/var/www/html/wetter/temperatur.txt', 'a') as f_temp, open('/var/www/html/wetter/feuchtigkeit.txt', 'a') as f_hum:
    for i in range(1, 4):
        th = ser.readline()
        ths = th.split()
        if len(ths) == 2:
            if ths[0].decode('ascii') == 'Temperature:':
                temp = float(ths[1])
                f_temp.write(f'{temp:.2f}\n')
            if ths[0].decode('ascii') == 'Humidity:':
                humidity = float(ths[1])
                f_hum.write(f'{humidity:.2f}\n')

# Schließe die serielle Verbindung
ser.close()

# Lade die letzten 100 Werte (oder eine andere Anzahl) aus den Dateien
temperaturen = np.loadtxt('/var/www/html/wetter/temperatur.txt')[-100:]
feuchtigkeiten = np.loadtxt('/var/www/html/wetter/feuchtigkeit.txt')[-100:]

# Filtere ungültige Werte (z.B. zu hohe oder zu niedrige Werte)
temperaturen = temperaturen[np.logical_and(temperaturen >= -50, temperaturen <= 50)]
feuchtigkeiten = feuchtigkeiten[np.logical_and(feuchtigkeiten >= 0, feuchtigkeiten <= 100)]

# Diagramm erstellen
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
ax1.set_xlabel('Zeit (h)', fontsize=12)
ax1.set_ylabel('Temperatur (°C)', color=color, fontsize=12)
ax1.plot(range(1, len(temperaturen) + 1), temperaturen, color=color, marker='o', markersize=5)  # Linienplot
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis='x', labelsize=10)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Feuchtigkeit (%)', color=color, fontsize=12)
ax2.plot(range(1, len(feuchtigkeiten) + 1), feuchtigkeiten, color=color, marker='o', markersize=5)  # Linienplot
ax2.tick_params(axis='y', labelcolor=color)
ax2.tick_params(axis='x', labelsize=10)

# Setze Ticks auf maximal 10 pro Achse
ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax2.xaxis.set_major_locator(ticker.MaxNLocator(10))

# Datenquelle hinzufügen
fig.text(0.5, 0.01, 'Datenquelle: daten.txt', ha='center', va='center', fontsize=10)

# Diagramm als PNG speichern
fig.savefig("/var/www/html/wetter/daten.png")

# HTML-Tabelle erstellen
html_table = '<table>'
img_tag = f'<img src="daten.png" alt="Diagramm">'
html_table += img_tag

# Lies die Datei mit den Temperatur- und Feuchtigkeitsdaten
with open('/var/www/html/wetter/daten.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    values = line.strip().split(',')
    if len(values) == 3:
        zeit, temp, humidity = values
        html_table += f'<tr><td>Temperatur: {temp}°C</td><td>Feuchtigkeit: {humidity}%</td></tr>'
html_table += '</table>'

# Aktuelle Zeit zur HTML-Tabelle hinzufügen
html_table += f'<p>Aktuelle Zeit: {now}</p>'

# HTML-Datei speichern
with open('/var/www/html/wetter/daten.html', 'w') as html_file:
    html_file.write(html_table)

print(now)
