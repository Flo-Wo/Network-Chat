"""!/usr/bin/python
-*- coding: UTF-8 -*-
"""
import socket
import os

# Ziel IP, entweder Rechner im lokalen Netzwerk (WLan und Ethernet) oder
# über eine manuelle Eingabe
eingabe = input("Verbindung zu einem Rechner im lokalen Netzwerk aufbauen (ja/nein): ")

if eingabe == "ja":
    print("Liste aller über Ethernet verbunden Geräte:\n\n")
    # Systembefehl, welcher alle Geräte im lokalen Netzwerk anzeigt
    rechner = os.popen("arp -a").readlines()
    for i in range(0, len(rechner)):
        # Nummerierung der Adressen --> Auswahl
        nummer = str(i) + ": "
        print(nummer + rechner[i])
    index = input(
        "Wähle deine Ziel-IP aus (Nummer, oder 'nicht in der Liste'): ")
    # Nutzer wählt Nummer aus --> Konvertierung zu einem Integer möglich
    try:
        index = int(index)
        # String aller Adressen --> Liste
        rechnerneu = rechner[index].split(" ")
        # Index der IP in der Liste
        rechnerwert = rechnerneu[1]
        # Entfernen der Klammern, da IP als Tupel vorliegt --> IP
        rechner1 = rechnerwert.replace("(", "")
        ip = rechner1.replace(")", "")
        print("Verbindung zum Zielrechner wird aufgebaut...\n")
        # print(ip)
    # Eingabe nicht konvertierbar --> "nicht in der Liste"
    except ValueError:
        # Manuelle Eingabe der IP, falls die Ziel-IP nicht in der Liste ist
        if index == "nicht in der Liste":
            ip = input("IP-Adresse des Zielrechners: ")
            print("Verbindung zum Zielrechner wird aufgebaut...\n")
        # Der Nutzer kommt trotzdem noch zur manuellen Eingabe
        else:
            print("Ungültie Eingabe. Manuelle Eingabe der IP-Adresse folgt...")
# Manuelle Eingabe
elif eingabe == "nein":
    ip = input("IP-Adresse des Zielrechers: ")
    print("Verbindung zum Zielrechner wird aufgebaut...\n")
else:
    print("Ungültige Eingabe.")

# Aufbau des Sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbindung mit dem Zielrechner --> Verbindungssocket
s.connect((ip, 50000))
name = str(input("Dein Name: ")) + ": "

# Abbruchbedingung
quitRechner2 = False

# Kommunikationssocket
try:
    while quitRechner2 == False:
        nachricht = input("Nachricht: ")
        # Abbruch der Kommunikation
        if nachricht == "quit()":
            nachricht = """\
            \n
-------------------------------------------
Der Partner hat die Kommunikation beendet.
-------------------------------------------
            """
            s.send(nachricht.encode())
            quitRechner2 = True
            break
        nachricht = name + nachricht + "\n"
        s.send(nachricht.encode())
        antwort = s.recv(1024)
        print(antwort.decode())
# Trennen der Verbindung
finally:
    s.close()
    print("""\
\n
-----------------------------------------------
Verbindung zum Kommunikationspartner getrennt.
-----------------------------------------------
""")
