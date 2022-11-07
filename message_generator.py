# Created by: Jay Huissen

import datetime
import psycopg2

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

    moderatie_tijd = "14:22:18"
    moderatie_datum = "07/11/22"

    cursor.execute("""INSERT INTO berichten 
                          (naam, bericht, datum, tijd, locatie, goedgekeurd, moderatorid, moddatum, modtijd) 
                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                   (data[0], data[1], data[4], data[3], data[2], gekeurd, modID,
                    moderatie_datum, moderatie_tijd))


database_connection = open_database("Wachtwoord")
moderatorID = 1

with open("stations.txt", "r") as stations_txt:
    stations_read = stations_txt.read()
    stations = stations_read.split("\n")

    stations.remove("")

    with open("berichten.txt", "r") as berichten_txt:
        berichten_read = berichten_txt.read()
        berichten = berichten_read.split("\n")

        berichten.remove("")

        for station in stations:

            for bericht in berichten:
                bericht_invoer = ["Anoniem",
                                  bericht,
                                  station,
                                  "14:22:18",
                                  "07/11/22"]

                add_database(bericht_invoer, database_connection, moderatorID, True)

database_connection.commit()
database_connection.close()
