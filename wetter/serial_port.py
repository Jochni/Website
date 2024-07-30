#!/usr/bin/env python3

import serial
import webbrowser
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mpld3
import os
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

# Lade die Daten aus den Dateien
temperaturen = np.loadtxt('/var/www/html/wetter/temperatur.txt')
feuchtigkeiten = np.loadtxt('/var/www/html/wetter/feuchtigkeit.txt')




# Diagramm erstellen
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Zeit (h)')
ax1.set_ylabel('Temperatur (°C)', color=color)
ax1.scatter(range(1, len(temperaturen) + 1)[::60], temperaturen[::60], color=color)  # Plot every 60th value
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Feuchtigkeit (%)', color=color)
ax2.scatter(range(1, len(feuchtigkeiten) + 1)[::60], feuchtigkeiten[::60], color=color)  # Plot every 60th value
ax2.tick_params(axis='y', labelcolor=color)

# ticker

ax1.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(1))

# Datenquelle hinzufügen
fig.text(0.5, 0.01, 'Datenquelle: daten.txt', ha='center', va='center')



# Öffne die Textdatei im Lesemodus
with open('/var/www/html/wetter/daten.txt', 'r') as f:
    lines = f.readlines()

# Erstelle eine HTML-Tabelle
html_table = '<table>'
# Diagramm wird in PNG-Datei Gespeichert
fig.savefig("/var/www/html/wetter/daten.png")

# HTML-Tag für das Bild erstellen
img_tag = f'<img src="daten.png" alt="Diagramm">'

# Füge das img_tag zur HTML-Tabelle hinzu
html_table += img_tag

for line in lines:
    values = line.strip().split(',')
    if len(values) == 3:
        zeit, temp, humidity = values
        html_table += f'<tr><td>Temperatur: {temp}°C</td><td>Feuchtigkeit: {humidity}%</td></tr>'
html_table += '</table>'

# Füge die aktuelle Zeit zur HTML-Tabelle hinzu
html_table += f'<p>Aktuelle Zeit: {now}</p>'

# Diagramm in HTML umwandeln und speichern
#html_str = mpld3.fig_to_html(fig)



# Schreibe die HTML-Tabelle und das Diagramm in eine Datei
with open('/var/www/html/wetter/daten.html', 'w') as html_file:
    #html_file.write(html_str)
    html_file.write(html_table)

print(now)
# plt.show()
