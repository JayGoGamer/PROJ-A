# Stationszuil
#
# Created by Jay Huissen
# Created on 26-09-2022
#
# Dit programma krijgt de berichten die mensen willen doorgeven aan het systeem. Hiermee kunnen ze hun berichten laten
# zien nadat ze door het moderatieprogramma heen gaan.

from datetime import datetime
import random

with open("txt/stations.txt", "r") as file:
    stations_file = file.read()
    stations = stations_file.split("\n")

    station = random.choice(stations)

    # open en split het bestand stations.txt om alle mogelijke stations aan te geven. Kies er hierna 1 uit om als
    # station te gebruiken.

while True:
    anoniem = input("Wilt u anoniem blijven? (ja/nee): ").strip().lower()

    if anoniem == "nee" or anoniem == "n":
        naam = input("\nWat is uw naam? ")
    else:
        print("")
        naam = "Anoniem"

    # Check of de reiziger anoniem wil blijven of niet.
    # Als de reiziger anoniem wil blijven word de naam "Anonniem" gezet

    bericht = input("Wat is uw bericht? ")

    # Vraag wat het bericht is en zet deze aan de variabele bericht

    if len(bericht) < 140:
        print(naam + " zegt " + bericht.lower() + " vanaf station " + station)
        correct = input("Klopt dit bericht? (ja/nee) ").strip().lower()
        if correct == "ja" or correct == "j":
            break
    else:
        print("Uw bericht is te lang, probeer opnieuw")

    # Check of het bericht te lang is of illegale karakters bevat.
    # Als het bericht niet correct is, doe dan de functie opnieuw

tijd = datetime.now().time()    # Haal de tijd op met datetime
datum = datetime.now().date()   # Haal de datum op met datetime

with open("txt/berichten.txt", "a") as file:
    file.write(naam + ";" + bericht + ";" +
               station + ";" + tijd.strftime("%H:%M:%S") +
               ";" + datum.strftime("%d/%m/%y") + "\n")

    # Open het bestand berichten.txt om de berichten ernaar te schrijven met ; tussen de data voor makkelijk aflezen
    # in module 2
