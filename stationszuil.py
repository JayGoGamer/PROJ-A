# Stationszuil
#
# Created by Jay Huissen
# Created on 26-09-2022
#
# [description here]

import datetime
import random

station_file = open("stations.txt", "r").read()
stations = station_file.split("\n")

station = random.randint(1, len(stations) - 1)

while True:
    anoniem = input("Wilt u anoniem blijven? (ja/nee): ").strip().lower()

    if anoniem == "nee" or anoniem == "n":
        naam = input("\nWat is uw naam? ")
    else:
        print("")
        naam = "Anoniem"

    bericht = input("Wat is uw bericht? ")

    print(naam + " zegt " + bericht + " vanaf station " + stations[station])
    correct = input("Klopt dit bericht? (ja/nee) ").strip().lower()

    if correct == "ja" or correct == "j":
        break

file = open("berichten.txt", "a")
file.write(naam + ";" + bericht + ";" + stations[station] + "\n")
