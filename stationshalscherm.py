# Stationshalscherm
#
# Created by Jay Huissen
# Created on 12-10-2022
#
# [description here]

from tkinter import *
import psycopg2

root = Tk()
root.geometry("1920x1080")


def open_database(password):
    connection = psycopg2.connect(database="nsBerichten",
                                  host="127.0.0.1",
                                  user="postgres",
                                  password=password,
                                  port="5432")

    return connection


def stations_keuze(station):
    pagina = Toplevel(root)

    pagina.title(station)
    pagina.geometry("1920x1080")

    sluiten = Button(pagina, text="Ga terug", command=pagina.destroy, width=20, font=("Arial", 15))
    sluiten.pack()

    connection = open_database(psswrd)
    cursor = connection.cursor()

    cursor.execute("SELECT ov_bike, elevator, toilet, park_and_ride FROM station_service WHERE station_city = %s", (station, ))
    faciliteiten = cursor.fetchall()

    cursor.execute("SELECT bericht, naam, datum, tijd FROM bericht WHERE locatie = %s AND goedgekeurd = True ORDER BY datum, tijd DESC", (station, ))
    berichten = cursor.fetchmany(5)

    bericht1 = Label(pagina, text="")
    bericht1.pack()
    bericht2 = Label(pagina, text="")
    bericht2.pack()
    bericht3 = Label(pagina, text="")
    bericht3.pack()
    bericht4 = Label(pagina, text="")
    bericht4.pack()
    bericht5 = Label(pagina, text="")
    bericht5.pack()

    match len(berichten):
        case 1:
            bericht1.config(text=berichten[0][0])
        case 2:
            bericht1.config(text=berichten[0][0])
            bericht2.config(text=berichten[1][0])
        case 3:
            bericht1.config(text=berichten[0][0])
            bericht2.config(text=berichten[1][0])
            bericht3.config(text=berichten[2][0])
        case 4:
            bericht1.config(text=berichten[0][0])
            bericht2.config(text=berichten[1][0])
            bericht3.config(text=berichten[2][0])
            bericht4.config(text=berichten[3][0])
        case 5:
            bericht1.config(text=berichten[0][0])
            bericht2.config(text=berichten[1][0])
            bericht3.config(text=berichten[2][0])
            bericht4.config(text=berichten[3][0])
            bericht5.config(text=berichten[4][0])
        case _:
            bericht1.config(text="Er zijn geen berichten")


def show():
    stations_keuze(clicked.get())


psswrd = input("Geef het wachtwoord van de database op: ")

options = []

with open("stations.txt", "r") as file:
    read_file = file.read()
    steden = read_file.split("\n")

    steden.remove("")

    for stad in steden:
        options.append(stad)

clicked = StringVar()

clicked.set("Utrecht")

drop = OptionMenu(root, clicked, *options)
drop.config(width=20, height=2, font=("Arial", 15))
drop.pack()

button = Button(root, text="Selecteer station", command=show, width=20, font=("Arial", 15))
button.pack()

label = Label(text=" ")
label.pack()

root.mainloop()
