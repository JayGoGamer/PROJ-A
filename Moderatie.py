# Moderatie
#
# Created by Jay Huissen
# Created on 12-10-2022
#
# [description here]

from datetime import datetime


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

def bestand_split(file_name):
    file = open(file_name, "r").read()

    berichten = file.split("\n")
    berichten.remove("")

    bericht_data = []

    for bericht in berichten:
        data = bericht.split(";")
        bericht_data.append(data)

    return bericht_data

def naar_database(data):
    print("Database")


moderator_naam = input("Wat is je naam? ")
moderator_email = input("Wat is je email adres? ")

while True:
    bericht = bestand_split("berichten.txt")

    print("\nHet bericht om te modereren: " + bericht[0][1])
    print("\nDe naam om te modereren: " + bericht[0][0])

    bericht_correct = bericht_check()
    if bericht_correct:
        naam_correct = naam_check()
        if not naam_correct:
            bericht[0][0] = "Anoniem"

            for data in bericht[0]:
                naar_database(data)


    break
