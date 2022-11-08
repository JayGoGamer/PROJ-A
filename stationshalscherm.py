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
import json

root = Tk()
root.attributes("-fullscreen", True)
# Maak een window aan en zet deze op fullscreen

bg = ImageTk.PhotoImage(Image.open("images/background.jpg").resize((2016, 1512)))
background = Label(root, image=bg)
background.place(relx=-0.01, rely=-0.2, anchor=NW)

# Geef de hoofdpagina een achtergrond en zet deze deels opzij om hem goed te laten passen


def open_database(password):
    connection = psycopg2.connect(database="nsBerichten",
                                  host="127.0.0.1",
                                  user="postgres",
                                  password=password,
                                  port="5432")

    return connection

    # Open de database en return de connectie


def weer_voorspelling(stad, master):
    with open("txt/api.txt", "r") as api_key_raw:
        api_key = api_key_raw.read()
    url = "https://api.openweathermap.org/data/2.5/weather?lang=nl&q=" + stad + \
          "&appid=" + api_key + "&units=metric"

    # Open de OpenWeatherAPI

    weer_json = requests.get(url).json()
    # Zet de weergegevens van de API in een JSON

    temperatuur = weer_json["main"]["temp"]                 # Pak de temperatuur uit de API
    temperatuur_max = weer_json["main"]["temp_max"]         # Pak de maximale temperatuur uit de API
    temperatuur_min = weer_json["main"]["temp_min"]         # Pak de minimale temperatuur uit de API
    weer_icon = weer_json["weather"][0]["icon"]             # Pak de URL-code van de passende icoon uit de API

    link = "http://openweathermap.org/img/wn/" + weer_icon + "@4x.png"

    urllib.request.urlretrieve(link, "images/icon.png")
    # Vraag het icoon op vanaf de site

    weer_plaatje = ImageTk.PhotoImage(Image.open("images/icon.png"))
    label = Label(master, image=weer_plaatje, compound="center", background="#FFFFFF")
    label.Image = weer_plaatje
    label.pack()

    # Open en plaats het plaatje van de weersoort op de pagina

    temp = str(round(temperatuur, 1)) + "°C"
    temp_max = "Max: " + str(round(temperatuur_max, 1)) + "°C"
    temp_min = "Min: " + str(round(temperatuur_min, 1)) + "°C"
    # Zet de temperatuur als een string met 1 getal achter de comma voor de maximale, minimale en momentele temperatuur

    label = Label(master, text=temp, background="#FFFFFF", font=("Arial", 20))
    label.pack()
    # Zet de temperatuur in een label en display deze op de pagina

    label = Label(master, text=temp_max, background="#FFFFFF", font=("Arial", 20))
    label.pack()
    # Zet de temperatuur in een label en display deze op de pagina

    label = Label(master, text=temp_min, background="#FFFFFF", font=("Arial", 20))
    label.pack()
    # Zet de temperatuur in een label en display deze op de pagina


def berichten_functie(master, stad):
    berichten_frame = Frame(master)
    berichten_frame.place(relx=0, rely=1, anchor=SW)
    berichten_frame.configure(background="#ffffff")

    # Maak een frame aan voor alle berichten en zet deze links neer

    connection = open_database(psswrd)
    cursor = connection.cursor()

    # Open de database en maak een cursor aan

    text_blok_raw = Image.open("images/textBlok.png")

    # Open de foto voor text blokken

    cursor.execute(
        """SELECT bericht, naam, datum, tijd FROM berichten 
        WHERE locatie = %s AND goedgekeurd = True 
        ORDER BY datum, tijd DESC""",
        (stad,))
    berichten = cursor.fetchmany(5)

    # Haal de data voor in de berichten uit de database, met maximaal 5 berichten

    for bericht in berichten:
        if len(bericht[0]) > (3 + len(bericht[1]) + len(str(bericht[3])) + len(str(bericht[2]))):
            message_length = len(bericht[0])
        else:
            message_length = len(bericht[1]) + len(str(bericht[3])) + len(str(bericht[2])) + 3

        foto_length = message_length * 12

        # Zet de breedte van de textwolk op de grootte van het bericht

        while foto_length > 1300:
            foto_length = foto_length - 20

        # Laat de textwolk niet te groot worden

        resized_text_blok = text_blok_raw.resize((foto_length, 100))
        text_blok = ImageTk.PhotoImage(resized_text_blok)
        label = Label(berichten_frame, text=(bericht[0] + "\n" + bericht[1] + ", " +
                                    str(bericht[3]) + " " + str(bericht[2])),
                      image=text_blok, compound="center", font=("Arial", 15))
        label.image = text_blok
        label.configure(background="#ffffff")
        label.pack()

        # Maak de label voor de textwolkjes en de informatie

    connection.close()

    # Sluit de database


def stations_keuze():
    station = clicked.get()

    pagina = Toplevel(root)

    pagina.attributes("-fullscreen", True)
    pagina.configure(background="#ffffff")
    pagina.title(station)

    # Maak een nieuwe pagina voor het station

    titel = Label(pagina, text=station, background="#00387b", foreground="#FFFFFF", font=("Arial", 50))
    titel.place(relx=0.5, rely=0.01, anchor=N)

    # Maak een titel in het midden van de pagina waar de stations naam staat

    frame = Frame(pagina)
    frame.place(relx=0.1, rely=0.1, anchor=S)
    frame.configure(background="#ffffff")

    # Maak een frame voor de hele pagina

    faciliteit_frame = Frame(pagina)
    faciliteit_frame.place(relx=1, rely=1, anchor=SE)
    faciliteit_frame.configure(background="#ffffff")

    # Maak een frame voor de faciliteiten die rechts onderin worden geplaatst

    weer_frame = Frame(pagina)
    weer_frame.place(relx=1, rely=0, anchor=NE)
    weer_frame.configure(background="#FFFFFF")

    # Maak een frame voor het weer die rechts bovenin geplaatst word

    weer_voorspelling(station, weer_frame)

    # Run de functie om de weer informatie op te halen van de API

    ovfiets_raw = Image.open("images/img_ovfiets.png")
    lift_raw = Image.open("images/img_lift.png")
    pr_raw = Image.open("images/img_pr.png")
    toilet_raw = Image.open("images/img_toilet.png")

    # Aanroepen van de foto's die gebruikt worden

    Button(frame, text="Ga terug", command=pagina.destroy, width=20, font=("Arial", 15)).pack()

    # Maak een knop aan die je terug stuurt naar de hoofdpagina

    connection = open_database(psswrd)
    cursor = connection.cursor()

    # Open de connectie naar de database en maak een cursor aan

    cursor.execute(
        """SELECT ov_bike, elevator, toilet, park_and_ride FROM station_service 
        WHERE station_city = %s""",
        (station,))
    faciliteiten = cursor.fetchall()

    # Haal de data voor de faciliteiten van het geselecteerde station op

    for faciliteit in faciliteiten:
        count = 0
        label = Label(faciliteit_frame, text="Faciliteiten op dit station: ", font=("Arial", 15), background="#FFFFFF")
        label.pack()

        # Maak een label aan om duidelijk te maken waar de plaatjes voor zijn

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

        # Met een match-case kijk ik welke faciliteiten op het station aanwezig zijn
        # en laat die als plaatjes zien op de pagina

    connection.close()

    # Sluit de verbinding

    berichten_functie(pagina, station)

    # Run de functie om de berichten op de pagina te krijgen


psswrd = input("Geef het wachtwoord van de database op: ")

# Vraag het wachtwoord van de database op

options = []

# Maak een list aan voor alle mogelijke station keuzes

with open("txt/stations.txt", "r") as file:
    read_file = file.read()
    steden = read_file.split("\n")

    steden.remove("")

    for stad in steden:
        options.append(stad)

    # Split de steden en zet ze in de list voor keuzes van stations

clicked = StringVar()

# Maak een variabele clicked aan die de waarde heeft van de dropdown keuze

clicked.set("Utrecht")

# Zet de standaard als Utrecht

drop = OptionMenu(root, clicked, *options)
drop.config(width=20, height=2, font=("Arial", 15))
drop.place(relx=0.01, rely=0.01, anchor=NW)

# Maak de dropdown aan en zet hem op de goeie plek neer

button = Button(root, text="Selecteer station", command=stations_keuze, width=20, font=("Arial", 15))
button.place(relx=0.02, rely=0.08, anchor=NW)

# Maak een knop aan die het station uitkiest als deze wordt ingedrukt

root.mainloop()

# Loop de pagina
