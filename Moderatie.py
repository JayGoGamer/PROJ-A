# Moderatie
#
# Created by Jay Huissen
# Created on 12-10-2022
#
# De functie van dit programma is om de berichten die binnen komen te modereren.
# Nadat de berichten gemodereerd zijn worden ze naar de database gestuurd door de code. Daarbij word de datum en tijd
# van het modereren er ook meegestuurd. De naam van de moderator word meegegeven naar de database, hier krijgt het
# zijn eigen nummer waar het aan gelinkt zit via een email adress.

from datetime import datetime
import psycopg2


def berichten():
    with open("txt/berichten.txt", "r") as file:
        read_file = file.read()
        split_file = read_file.split("\n")

        if split_file[0] == "":
            return False

        return True

    # Kijk of er berichten in berichten.txt zijn om te modereren.


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

    # Vraag aan de moderator of ze het bericht goedkeuren of niet.
    # Als de moderator "stop" typt, wordt het programma gestopt


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

    # Vraag aan de moderator of ze de naam goedkeuren of niet.
    # Als de moderator "stop" typt, wordt het programma gestopt


def moderator():
    gegevens = []
    naam = input("Wat is uw naam? ")
    email = input("Wat is uw email? ")

    # Vraag de gegevens van de moderator op. (Naam en email)

    if "@ns.nl" not in email:
        print("Geen geldig email adres, probeer opnieuw")
        moderator()

        # De email moet "@ns.nl" bevatten om een geldig email-adres van een NS-medewerker te zijn

    else:
        gegevens.append(naam)
        gegevens.append(email)
        return gegevens

        # Als de email klopt de gegevens in een list zetten zodat ze makkelijk te vinden zijn


def bestand_split(file_name):
    file = open(file_name, "r").read()

    berichten = file.split("\n")
    berichten.remove("")

    # Open het bestand met alle berichten en split het op de "\n" zodat het in een list komt die makkelijker te
    # splitten is om alle gedeeltes van het bericht te kunnen vinden

    bericht_data = []

    # Maak een nieuwe list voor alle data van het bericht

    for bericht in berichten:
        data = bericht.split(";")
        bericht_data.append(data)

        # Split de berichten in naam, bericht, datum en tijd

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

    # Controleer of het bericht en de naam correct zijn. Als deze beide kloppen, returnt het programma 1,
    # wordt er stop getypt, returnt het programma -1. Als het bericht niet passend is, returnt het programma 0.
    # Als de naam niet passend is, wordt deze veranderd naar "Anoniem"


def open_database(psswrd):
    connection = psycopg2.connect(database="nsBerichten",
                                  host="127.0.0.1",
                                  user="postgres",
                                  password=psswrd,
                                  port="5432")

    return connection

    # Open de database die lokaal op de computer staat en return de connectie


def mod_to_database(gegevens, connection):
    cursor = connection.cursor()

    cursor.execute("SELECT moderator.moderatorid FROM moderator WHERE emailadress = %s", (gegevens[1],))
    moderatieid = cursor.fetchone()

    # Probeer de moderatieID van de moderator met de opgegeven mail te selecteren.

    if moderatieid is None:
        cursor.execute("INSERT INTO moderator (naam, emailadress) VALUES(%s, %s)", (gegevens[0], gegevens[1]))
        return 0

        # Als de moderator zijn email nog niet in de database staat, maak dan een nieuwe aan voor de moderator

    else:
        return moderatieid

        # Als de moderatieID wel al in het systeem staat, return dan die waarde


def pull_modID(connection, gegevens):
    cursor = connection.cursor()

    cursor.execute("SELECT moderator.moderatorid FROM moderator WHERE emailadress = %s", (gegevens[1],))
    moderatieid = cursor.fetchone()

    return moderatieid

    # Vraag de moderatieID op van de database en return deze


def add_database(data, connection, modID, status):
    cursor = connection.cursor()

    if status == 1:
        gekeurd = True
    else:
        gekeurd = False

    # Kijk of het bericht goedgekeurd is voordat het programma verder gaat

    moderatie_tijd = datetime.now().time()      # Haal de tijd van modereren op
    moderatie_datum = datetime.now().date()     # Haal de datum van modereren op

    cursor.execute("""INSERT INTO berichten 
                          (naam, bericht, datum, tijd, locatie, goedgekeurd, moderatorid, moddatum, modtijd) 
                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                   (data[0][0], data[0][1], data[0][4], data[0][3], data[0][2], gekeurd, modID[0],
                    moderatie_datum.strftime("%d/%m/%y"), moderatie_tijd.strftime("%H:%M:%S")))

    # Stuur de data van het bericht door naar de database


def remove_line(data):
    with open("txt/berichten.txt", "w") as file:
        for i in range(1, len(data)):
            for x in range(0, len(data[0])):
                file.write(data[i][x] + ";")
            file.write("\n")

    # Verwijder het gemodereerde bericht uit het txt bestand, omdat er niet een functie voor is,
    # moet de hele txt file opnieuw geschreven worden.


print("\n==================== Moderatie ====================\n")

moderator_gegevens = moderator()    # Vraag de gegevens op
wachtwoord = input("\nWat is het wachtwoord van de database? ")
# Vraag het database-wachtwoord om die te kunnen openen

database_connection = open_database(wachtwoord)     # Open de database met het wachtwoord

print("\nTyp stop op elk moment om het modereren te stoppen")

if mod_to_database(moderator_gegevens, database_connection) != 0:
    moderatorID = pull_modID(database_connection, moderator_gegevens)
else:
    moderatorID = mod_to_database(moderator_gegevens, database_connection)

# Kijk of de moderator al in het systeem staat of niet.
# Als de moderator er nog niet in staat zet die er dan in, anders moet de moderatieID opgehaald worden

database_connection.commit()
database_connection.close()

# Stuur alle al opgegeven data naar de database


database_connection = open_database(wachtwoord)

# Open de database opnieuw


while True:

    if not berichten():
        print("\nEr zijn geen berichten om te modereren")
        database_connection.commit()
        database_connection.close()
        break

        # Stop het programma als er geen berichten meer zijn om te modereren

    bericht = bestand_split("txt/berichten.txt") # Split het bestand

    print("\nHet bericht om te modereren: " + bericht[0][1])
    print("\nDe naam om te modereren: " + bericht[0][0])

    # Laat het bericht en de naam zien die gemodereerd moeten worden

    correct = goedgekeurd(bericht)

    # Run de keuringsfunctie

    if correct == -1:
        print("\nBedankt voor het modereren!")
        print("\n====================================================\n")
        database_connection.commit()
        database_connection.close()
        break

        # Als de moderator wil stoppen, sluit de database en stop het programma.

    else:
        add_database(bericht, database_connection, moderatorID, correct)
        remove_line(bericht)

        # Als het bericht is gekeurd, stuur deze dan naar de database
