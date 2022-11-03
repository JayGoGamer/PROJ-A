# Stationshalscherm
#
# Created by Jay Huissen
# Created on 12-10-2022
#
# [description here]

from tkinter import *
import psycopg2

global bericht4_data
global bericht3_data
global bericht2_data
global bericht1_data
global nieuw_bericht

root = Tk()
root.geometry("1200x600")


def open_database():
    psswrd = input("Geef het wachtwoord van de database op: ")

    connection = psycopg2.connect(database="nsBerichten",
                                  host="127.0.0.1",
                                  user="postgres",
                                  password=psswrd,
                                  port="5432")

    return connection


def stations_keuze(station):
    print(station)


def show(berichten):
    nieuw_bericht = clicked.get()
    stations_keuze(nieuw_bericht)


while True:
    open_database()
    break

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

bericht1 = Label(root, text=" ")
bericht1.pack()

bericht2 = Label(root, text=" ")
bericht2.pack()

bericht3 = Label(root, text=" ")
bericht3.pack()

bericht4 = Label(root, text=" ")
bericht4.pack()

bericht5 = Label(root, text=" ")
bericht5.pack()

root.mainloop()
