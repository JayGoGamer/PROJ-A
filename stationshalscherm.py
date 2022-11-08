# Stationshalscherm
#
# Created by Jay Huissen
# Created on 12-10-2022
#
# [description here]

from tkinter import *
import psycopg2
from PIL import Image, ImageTk
import requests
import urllib

root = Tk()
root.attributes("-fullscreen", True)

bg = ImageTk.PhotoImage(Image.open("images/background.jpg").resize((2016, 1512)))
background = Label(root, image=bg)
background.place(relx=-0.01, rely=-0.2, anchor=NW)


def open_database(password):
    connection = psycopg2.connect(database="nsBerichten",
                                  host="127.0.0.1",
                                  user="postgres",
                                  password=password,
                                  port="5432")

    return connection


def weer_voorspelling(stad, master):
    with open("txt/api.txt", "r") as api_key_raw:
        api_key = api_key_raw.read()
    url = "https://api.openweathermap.org/data/2.5/weather?lang=nl&q=" + stad + \
          "&appid=" + api_key + "&units=metric"

    weer_json = requests.get(url).json()

    temperatuur = weer_json["main"]["temp"]
    weer_icon = weer_json["weather"][0]["icon"]

    link = "http://openweathermap.org/img/wn/" + weer_icon + "@4x.png"

    urllib.request.urlretrieve(link, "images/icon.png")

    weer_plaatje = ImageTk.PhotoImage(Image.open("images/icon.png"))
    label = Label(master, image=weer_plaatje, compound="center", background="#FFFFFF")
    label.Image = weer_plaatje
    label.pack()

    temp = str(round(temperatuur, 1)) + "°C"

    label = Label(master, text=temp, background="#FFFFFF", font=("Arial", 20))
    label.pack()


def berichten_functie(master, stad):
    berichten_frame = Frame(master)
    berichten_frame.place(relx=0, rely=1, anchor=SW)
    berichten_frame.configure(background="#ffffff")

    connection = open_database(psswrd)
    cursor = connection.cursor()

    text_blok_raw = Image.open("images/textBlok.png")

    cursor.execute(
        """SELECT bericht, naam, datum, tijd FROM berichten 
        WHERE locatie = %s AND goedgekeurd = True 
        ORDER BY datum, tijd DESC""",
        (stad,))
    berichten = cursor.fetchmany(5)

    for bericht in berichten:
        if len(bericht[0]) > (3 + len(bericht[1]) + len(str(bericht[3])) + len(str(bericht[2]))):
            message_length = len(bericht[0])
        else:
            message_length = len(bericht[1]) + len(str(bericht[3])) + len(str(bericht[2])) + 3

        foto_length = message_length * 12

        while foto_length > 1300:
            foto_length = foto_length - 20

        resized_text_blok = text_blok_raw.resize((foto_length, 100))
        text_blok = ImageTk.PhotoImage(resized_text_blok)
        label = Label(berichten_frame, text=(bericht[0] + "\n" + bericht[1] + ", " +
                                    str(bericht[3]) + " " + str(bericht[2])),
                      image=text_blok, compound="center", font=("Arial", 15))
        label.image = text_blok
        label.configure(background="#ffffff")
        label.pack()

    connection.close()


def stations_keuze(station):
    pagina = Toplevel(root)

    pagina.attributes("-fullscreen", True)
    pagina.configure(background="#ffffff")
    pagina.title(station)

    titel = Label(pagina, text=station, background="#00387b", foreground="#FFFFFF", font=("Arial", 50))
    titel.place(relx=0.5, rely=0.01, anchor=N)

    frame = Frame(pagina)
    frame.place(relx=0.1, rely=0.1, anchor=S)
    frame.configure(background="#ffffff")

    faciliteit_frame = Frame(pagina)
    faciliteit_frame.place(relx=1, rely=1, anchor=SE)
    faciliteit_frame.configure(background="#ffffff")

    weer_frame = Frame(pagina)
    weer_frame.place(relx=1, rely=0, anchor=NE)
    weer_frame.configure(background="#FFFFFF")

    weer_voorspelling(station, weer_frame)

    ovfiets_raw = Image.open("images/img_ovfiets.png")
    lift_raw = Image.open("images/img_lift.png")
    pr_raw = Image.open("images/img_pr.png")
    toilet_raw = Image.open("images/img_toilet.png")

    Button(frame, text="Ga terug", command=pagina.destroy, width=20, font=("Arial", 15)).pack()

    connection = open_database(psswrd)
    cursor = connection.cursor()

    cursor.execute(
        """SELECT ov_bike, elevator, toilet, park_and_ride FROM station_service 
        WHERE station_city = %s""",
        (station,))
    faciliteiten = cursor.fetchall()

    for faciliteit in faciliteiten:
        count = 0
        label = Label(faciliteit_frame, text="Faciliteiten op dit station: ", font=("Arial", 15), background="#FFFFFF")
        label.pack()
        for fac in faciliteit:
            count += 1
            if fac is True:
                match count:
                    case 1:
                        img_ovfiets = ImageTk.PhotoImage(ovfiets_raw)
                        label = Label(faciliteit_frame, image=img_ovfiets, compound="center")
                        label.Image = img_ovfiets
                    case 2:
                        img_lift = ImageTk.PhotoImage(lift_raw)
                        label = Label(faciliteit_frame, image=img_lift, compound="center")
                        label.Image = img_lift
                    case 3:
                        img_toilet = ImageTk.PhotoImage(toilet_raw)
                        label = Label(faciliteit_frame, image=img_toilet, compound="center")
                        label.Image = img_toilet
                    case 4:
                        img_pr = ImageTk.PhotoImage(pr_raw)
                        label = Label(faciliteit_frame, image=img_pr, compound="center")
                        label.Image = img_pr

                label.configure(background="#ffffff")
                label.pack()

    connection.close()

    berichten_functie(pagina, station)


def show():
    stations_keuze(clicked.get())


psswrd = input("Geef het wachtwoord van de database op: ")

options = []

with open("txt/stations.txt", "r") as file:
    read_file = file.read()
    steden = read_file.split("\n")

    steden.remove("")

    for stad in steden:
        options.append(stad)

clicked = StringVar()

clicked.set("Utrecht")

drop = OptionMenu(root, clicked, *options)
drop.config(width=20, height=2, font=("Arial", 15))
drop.place(relx=0.01, rely=0.01, anchor=NW)

button = Button(root, text="Selecteer station", command=show, width=20, font=("Arial", 15))
button.place(relx=0.02, rely=0.08, anchor=NW)

root.mainloop()
