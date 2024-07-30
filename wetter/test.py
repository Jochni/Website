import matplotlib.pyplot as plt

wert1 = open("temperatur.txt")
wert2 = open("feuchtigkeit.txt")
ywerte = [wert1]
xwerte = [wert2]
plt.plot(xwerte, ywerte)
plt.scatter(xwerte, ywerte)
plt.xlabel("X-Werte")
plt.ylabel("Y-Werte")
plt.show()