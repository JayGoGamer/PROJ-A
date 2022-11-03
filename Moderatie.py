# Moderatie
#
# Created by Jay Huissen
# Created on 12-10-2022
#
# [description here]

from datetime import datetime
import json
import psycopg2


def berichten():
    with open("berichten.txt", "r") as file:
        read_file = file.read()
        split_file = read_file.split("\n")

        if split_file[0] == "":
            return False

        return True

def bericht_check():
    correct_bericht = input("\nVind u het een gepast bericht? (ja/nee) ").strip().lower()

    if correct_bericht == "stop":
        return -1

    if correct_bericht == "j" or correct_bericht == "ja":
        print("Het bericht is goedgekeurd")
        return 1
    else:
        print("het bericht is afgekeurd")
        return 0


def naam_check():
    correcte_naam = input("\nVind U het een gepaste naam? (ja/nee) ").strip().lower()

    if correcte_naam == "stop":
        return -1

    if correcte_naam == "j" or correcte_naam == "ja":
        print("De naam is goedgekeurd")
        return 1
    else:
        print("De naam is afgekeurd, deze word veranderd naar anoniem")
        return 0


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
        print(gegevens)
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

    if bericht_correct == -1:
        return -1

    if bericht_correct == 0:
        return 0

    naam_correct = naam_check()
    if naam_correct == 0:
        bericht[0][0] = "Anoniem"

    if naam_correct == -1:
        return -1

    return 1


def open_database(psswrd):
    connection = psycopg2.connect(database="nsBerichten",
                                  host="127.0.0.1",
                                  user="postgres",
                                  password=psswrd,
                                  port="5432")

    return connection


def mod_to_database(gegevens, connection):
    cursor = connection.cursor()

    moderatie_tijd = datetime.now().time()
    moderatie_datum = datetime.now().date()

    cursor.execute("INSERT INTO moderator (naam, emailadress, datum, tijd) VALUES(%s, %s, %s, %s)",
                   (gegevens[0], gegevens[1], moderatie_datum.strftime("%y/%m/%d"), moderatie_tijd.strftime("%H:%M:%S")))


def pull_modID(connection, gegevens):
    cursor = connection.cursor()

    cursor.execute("SELECT moderatieid FROM moderator WHERE emailadress = %s", (gegevens[1],))
    moderatieid = cursor.fetchone()

    return moderatieid


def add_database(data, connection, modID, status):
    cursor = connection.cursor()
    if status == 1:
        gekeurd = True
    else:
        gekeurd = False

    cursor.execute("""INSERT INTO bericht (naam, bericht, datum, tijd, locatie, goedgekeurd, moderatorID, stationID) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
                   (data[0][0], data[0][1], data[0][4], data[0][3], data[0][2], gekeurd, modID, data[0][2]))


def remove_line(data):
    with open("berichten.txt", "w") as file:
        for i in range(1, len(data)):
            for x in range(0, len(data[0])):
                file.write(data[i][x] + ";")
            file.write("\n")


print("\n==================== Moderatie ====================\n")

moderator_gegevens = moderator()
wachtwoord = input("Wat is het wachtwoord van de database? ")

database_connection = open_database(wachtwoord)

print("\nTyp stop op elk moment om het modereren te stoppen")

mod_to_database(moderator_gegevens, database_connection)

database_connection.commit()
database_connection.close()

database_connection = open_database(wachtwoord)

moderatorID = pull_modID(database_connection, moderator_gegevens)

while True:

    if not berichten():
        print("Er zijn geen berichten om te modereren")
        database_connection.commit()
        database_connection.close()
        break

    bericht = bestand_split("berichten.txt")

    print("\nHet bericht om te modereren: " + bericht[0][1])
    print("\nDe naam om te modereren: " + bericht[0][0])

    correct = goedgekeurd(bericht)

    if correct == -1:
        print("\nBedankt voor het modereren!")
        print("\n====================================================\n")
        database_connection.commit()
        database_connection.close()
        break

    elif correct == 1 or correct == 0:
        add_database(bericht, database_connection, moderatorID, correct)
        remove_line(bericht)