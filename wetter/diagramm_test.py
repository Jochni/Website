#!/usr/bin/python
import serial
import webbrowser
from datetime import datetime
import matplotlib.pyplot as plt
import mpld3
import os

# Listen für Temperatur und Feuchtigkeit
temperaturen = []
feuchtigkeiten = []

# Diagramm erstellen
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Zeit (s)')
ax1.set_ylabel('Temperatur (°C)', color=color)
ax1.plot(range(1, len(temperaturen) + 1), temperaturen, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Feuchtigkeit (%)', color=color)
ax2.plot(range(1, len(feuchtigkeiten) + 1), feuchtigkeiten, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()

# Datenquelle hinzufügen
fig.text(0.5, 0.01, 'Datenquelle: daten.txt', ha='center', va='center')

# Öffne die Textdatei im Lesemodus
with open('wetter/daten.txt', 'r') as f:
    lines = f.readlines()

# Erstelle eine HTML-Tabelle
html_table = '<table>'
for line in lines:
    values = line.strip().split(',')
    if len(values) == 3:
        zeit, temp, humidity = values
        html_table += f'<tr><td>Temperatur: {temp}°C</td><td>Feuchtigkeit: {humidity}%</td></tr>'
html_table += '</table>'

# Füge die aktuelle Zeit zur HTML-Tabelle hinzu
#html_table += f'<p>Aktuelle Zeit: {now}</p>'

# Diagramm in HTML umwandeln und speichern
html_str = mpld3.fig_to_html(fig)

# Schreibe die HTML-Tabelle und das Diagramm in eine Datei
with open('wetter/daten.html', 'w') as html_file:
    html_file.write(html_str)
    html_file.write(html_table)

#print(now)
