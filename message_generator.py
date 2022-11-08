# Created by: Jay Huissen

import time
from datetime import datetime
import psycopg2
import random


def open_database(psswrd):
    connection = psycopg2.connect(database="nsBerichten",
                                  host="127.0.0.1",
                                  user="postgres",
                                  password=psswrd,
                                  port="5432")

    return connection


def add_database(data, connection, modID, status):
    cursor = connection.cursor()
    if status == 1:
        gekeurd = True
    else:
        gekeurd = False

    moderatie_tijd = datetime.now().time()
    moderatie_datum = datetime.now().date()

    cursor.execute("""INSERT INTO berichten 
                          (naam, bericht, datum, tijd, locatie, goedgekeurd, moderatorid, moddatum, modtijd) 
                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                   (data[0], data[1], data[4], data[3], data[2], gekeurd, modID,
                    moderatie_datum.strftime("%d/%m/%y"), moderatie_tijd.strftime("%H:%M:%S")))


psswrd = input("Wat is het wachtwoord: ")
database_connection = open_database(psswrd)
moderatorID = 1

with open("txt/stations.txt", "r") as stations_txt:
    stations_read = stations_txt.read()
    stations = stations_read.split("\n")

    stations.remove("")

    with open("txt/bericht.txt", "r") as berichten_txt:
        berichten = berichten_txt.read().split("\n")

        berichten.remove("")

        with open("txt/namen.txt") as namen_txt:
            namen = namen_txt.read().split("\n")

            namen.remove("")

            for station in stations:

                for x in range(5):
                    moderatie_tijd = datetime.now().time()
                    moderatie_datum = datetime.now().date()

                    bericht_invoer = [random.choice(namen),
                                      random.choice(berichten),
                                      station,
                                      moderatie_tijd.strftime("%H:%M:%S"),
                                      moderatie_datum.strftime("%d/%m/%y")]

                    add_database(bericht_invoer, database_connection, moderatorID, True)
                    print(bericht_invoer)
                    time.sleep(1)

database_connection.commit()
database_connection.close()
