#!/usr/bin/env python3

import serial
import webbrowser
from datetime import datetime
import matplotlib.pyplot as plt
import mpld3
import os

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

# Öffne die Textdatei im Schreibmodus nämlich daten.txt ('w')
with open('wetter/daten.txt', 'w') as f:
    for i in range(1, 4):
        y = 0
        t =  y + 1
        print(t)
        th = ser.readline()
        ths = th.split()
        if len(ths) == 2:
            if ths[0].decode('ascii') == 'Temperature:':
                temp = float(ths[1])
                temperaturen.append(temp)
                f.write(f'Temperatur: {temp:.2f}°C\n')
            if ths[0].decode('ascii') == 'Humidity:':
                humidity = float(ths[1])
                feuchtigkeiten.append(humidity)
                f.write(f'Luftfeuchtigkeit: {humidity:.2f}%\n')

# Öffne die Textdateien im Schreibmodus einzeln ('w')
with open('wetter/temperatur.txt', 'w') as f_temp, open('wetter/feuchtigkeit.txt', 'w') as f_hum:
    for i in range(1, 4):
        y = 0
        t =  y + 1
        print(t)
        th = ser.readline()
        ths = th.split()
        if len(ths) == 2:
            if ths[0].decode('ascii') == 'Temperature:':
                temp = float(ths[1])
                f_temp.write(f'Temperatur: {temp:.2f}°C\n')
            if ths[0].decode('ascii') == 'Humidity:':
                humidity = float(ths[1])
                f_hum.write(f'Luftfeuchtigkeit: {humidity:.2f}%\n')

# Schließe die serielle Verbindung
ser.close()

# Diagramm erstellen
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Zeit (s)')
ax1.set_ylabel('Temperatur (°C)', color=color)
ax1.plot(temperaturen, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Feuchtigkeit (%)', color=color)
ax2.plot(feuchtigkeiten, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()

# Öffne die Textdatei im Lesemodus
with open('wetter/daten.txt', 'r') as f:
    lines = f.readlines()

# Erstelle eine HTML-Tabelle
html_table = '<table>'
for line in lines:
    values = line.strip().split(':')
    if len(values) == 2:
        key, value = values
        html_table += f'<tr><td>{key}</td><td>{value}</td></tr>'
html_table += '</table>'

# Füge die aktuelle Zeit zur HTML-Tabelle hinzu
html_table += f'<p>Aktuelle Zeit: {now}</p>'

# Diagramm in HTML umwandeln und speichern
html_str = mpld3.fig_to_html(fig)

# Schreibe die HTML-Tabelle und das Diagramm in eine Datei
with open('wetter/daten.html', 'w') as html_file:
    html_file.write(html_str)
    html_file.write(html_table)

print(now)
