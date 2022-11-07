# Stationszuil
#
# Created by Jay Huissen
# Created on 26-09-2022
#
# Dit programma krijgt de berichten die mensen willen doorgeven aan het systeem. Hiermee kunnen ze hun berichten laten
# zien nadat ze door het moderatieprogramma heen gaan.

from datetime import datetime
import random

with open("stations.txt", "r") as file:
    stations_file = file.read()
    stations = stations_file.split("\n")

station = random.randint(1, len(stations) - 1)

while True:
    anoniem = input("Wilt u anoniem blijven? (ja/nee): ").strip().lower()

    if anoniem == "nee" or anoniem == "n":
        naam = input("\nWat is uw naam? ")
    else:
        print("")
        naam = "Anoniem"

    bericht = input("Wat is uw bericht? ")

    if len(bericht) < 140:
        print(naam + " zegt " + bericht.lower() + " vanaf station " + stations[station])
        correct = input("Klopt dit bericht? (ja/nee) ").strip().lower()
        if correct == "ja" or correct == "j":
            break
    else:
        print("Uw bericht is te lang, probeer opnieuw")

tijd = datetime.now().time()
datum = datetime.now().date()

with open("berichten.txt", "a") as file:
    file.write(naam + ";" + bericht + ";" + stations[station] + ";" + tijd.strftime("%H:%M:%S") + ";" + datum.strftime("%d/%m/%y") + "\n")
