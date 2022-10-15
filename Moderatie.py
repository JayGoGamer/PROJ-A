# Moderatie
#
# Created by Jay Huissen
# Created on 12-10-2022
#
# [description here]

from datetime import datetime
import json


def berichten():
    with open("berichten.txt", "r") as file:
        read_file = file.read()
        split_file = read_file.split("\n")

        if split_file[0] == "":
            return False

        return True

def bericht_check():
    correct_bericht = input("\nVind u het een gepast bericht? (ja/nee) ").strip().lower()

    if correct_bericht == "j" or correct_bericht == "ja":
        print("Het bericht is goedgekeurd")
        return True
    else:
        print("het bericht is afgekeurd")
        return False


def naam_check():
    correcte_naam = input("\nVind U het een gepaste naam? (ja/nee) ").strip().lower()

    if correcte_naam == "j" or correcte_naam == "ja":
        print("De naam is goedgekeurd")
        return True
    else:
        print("De naam is afgekeurd, deze word veranderd naar anoniem")
        return False




def moderator():
    gegevens = []
    naam = input("Wat is uw naam? ")
    email = input("Wat is uw email? ")

    if "@" not in email:
        print("Geen geldig email adres, probeer opnieuw")
        moderator()

    else:
        gegevens.append(naam)
        gegevens.append(email)
        return gegevens

def bestand_split(file_name):
    file = open(file_name, "r").read()

    berichten = file.split("\n")
    berichten.remove("")

    bericht_data = []

    for bericht in berichten:
        data = bericht.split(";")
        bericht_data.append(data)

    return bericht_data


def goedgekeurd(bericht):
    bericht_correct = bericht_check()
    if not bericht_correct:
        return False

    if not naam_check():
        bericht[0][0] = "Anoniem"

    return True

def naar_database(data, gegevens):
    with open("gemodereerde_berichten.txt", "a") as file:
        for i in range(0, 4):
            file.write(str(data[0][i]) + ";")
        file.write(gegevens[0] + ";" + gegevens[1] + "\n")


def naar_afgekeurde(data, gegevens):
    with open("afgekeurde_berichten.txt", "a") as file:
        for i in range(0, 4):
            file.write(str(data[0][i]) + ";")
        file.write(gegevens[0] + ";" + gegevens[1] + "\n")


def remove_line(data):
    with open("berichten.txt", "w") as file:
        for i in range(1, len(data)):
            for x in range(0, len(data[0])):
                file.write(data[i][x] + ";")
            file.write("\n")

moderator_gegevens = moderator()

while True:

    if not berichten():
        print("Er zijn geen berichten om te modereren")
        break

    if input("\nWilt u stoppen? (ja/nee)").lower().strip() == "ja":
        break

    bericht = bestand_split("berichten.txt")

    print("\nHet bericht om te modereren: " + bericht[0][1])
    print("\nDe naam om te modereren: " + bericht[0][0])

    if goedgekeurd(bericht):
        naar_database(bericht, moderator_gegevens)
        remove_line(bericht)

    else:
        naar_afgekeurde(bericht, moderator_gegevens)
        remove_line(bericht)
