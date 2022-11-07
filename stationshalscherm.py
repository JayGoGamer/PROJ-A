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
root.attributes("-fullscreen", True)


def open_database(password):
    connection = psycopg2.connect(database="nsBerichten",
                                  host="127.0.0.1",
                                  user="postgres",
                                  password=password,
                                  port="5432")

    return connection


def stations_keuze(station):
    pagina = Toplevel(root)

    pagina.attributes("-fullscreen", True)
    pagina.title(station)

    frame = Frame(pagina)
    frame.place(relx=0.1, rely=0.1, anchor=S)
    berichten_frame = Frame(pagina)
    berichten_frame.place(relx=0, rely=0.5, anchor=W)
    weer_frame = Frame(pagina)
    weer_frame.place(relx=1, rely=0.5, anchor=E)

    text_blok_raw = Image.open("images/textBlok.png")
    lift_raw = Image.open("images/img_lift.png")
    img_lift = ImageTk.PhotoImage(lift_raw)
    ovfiets_raw = Image.open("images/img_ovfiets.png")
    img_ovfiets = ImageTk.PhotoImage(ovfiets_raw)
    pr_raw = Image.open("images/img_pr.png")
    img_pr = ImageTk.PhotoImage(pr_raw)
    toilet_raw = Image.open("images/img_toilet.png")
    img_toilet = ImageTk.PhotoImage(toilet_raw)

    sluiten = Button(frame, text="Ga terug", command=pagina.destroy, width=20, font=("Arial", 15))
    sluiten.pack()

    connection = open_database(psswrd)
    cursor = connection.cursor()

    cursor.execute(
        """SELECT ov_bike, elevator, toilet, park_and_ride FROM station_service 
        WHERE station_city = %s""",
        (station,))
    faciliteiten = cursor.fetchall()

    cursor.execute(
        """SELECT bericht, naam, datum, tijd FROM berichten 
        WHERE locatie = %s AND goedgekeurd = True 
        ORDER BY datum, tijd DESC""",
        (station,))
    berichten = cursor.fetchmany(5)

    for bericht in berichten:
        if len(bericht[0]) > (3 + len(bericht[1]) + len(str(bericht[3])) + len(str(bericht[2]))):
            message_length = len(bericht[0])
        else:
            message_length = len(bericht[1]) + len(str(bericht[3])) + len(str(bericht[2])) + 3

        resized_text_blok = text_blok_raw.resize(((message_length * 12), 100))
        text_blok = ImageTk.PhotoImage(resized_text_blok)
        label = Label(berichten_frame, text=(bericht[0] + "\n" + bericht[1] + ", " +
                                             str(bericht[3]) + " " + str(bericht[2])),
                      image=text_blok, compound="center", font=("Arial", 15))
        label.image = text_blok
        label.pack()

    for faciliteit in faciliteiten:
        count = 0
        for fac in faciliteit:
            count += 1
            if fac is True:
                match count:
                    case 1:
                        label = Label(weer_frame, text="fiets", image=img_ovfiets, compound="center")
                        print(fac)
                    case 2:
                        label = Label(weer_frame, text="", image=img_lift, compound="center")
                        print(fac)
                    case 3:
                        label = Label(weer_frame, text="", image=img_toilet, compound="center")
                        print(fac)
                    case 4:
                        label = Label(weer_frame, text="", image=img_pr, compound="center")
                        print(fac)
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
