# Stationshalscherm
#
# Created by Jay Huissen
# Created on 12-10-2022
#
# [description here]

from tkinter import *
import psycopg2
from PIL import Image, ImageTk

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

    text_blok_raw = Image.open("textBlok.png")
    resized_text_blok = text_blok_raw.resize((300, 300))
    text_blok = ImageTk.PhotoImage(resized_text_blok)


    sluiten = Button(pagina, text="Ga terug", command=pagina.destroy, width=20, font=("Arial", 15))
    sluiten.pack()

    connection = open_database(psswrd)
    cursor = connection.cursor()

    cursor.execute("SELECT ov_bike, elevator, toilet, park_and_ride FROM station_service WHERE station_city = %s",
                   (station,))
    faciliteiten = cursor.fetchall()

    cursor.execute(
        "SELECT bericht, naam, datum, tijd FROM berichten WHERE locatie = %s AND goedgekeurd = True ORDER BY datum, tijd DESC",
        (station,))
    berichten = cursor.fetchmany(5)



    for bericht in berichten:
        label = Label(pagina, text=bericht[0], image=text_blok, compound="center")
        label.image = text_blok
        label.pack()


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

root.mainloop()
