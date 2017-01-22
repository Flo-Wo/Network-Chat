"""!/usr/bin/python
-*- coding: UTF-8 -*-
Date: 14.01.2017
"""
import socket
import os

# Eingabe der IP-Adresse, entweder lokal Ethernet Verbindungen oder über eine Eingabe
eingabe = input("Verbindung zu einem Rechner im lokalen Netzwerk aufbauen (ja/nein): ")

if eingabe == "ja":
    print("Liste aller über Ethernet verbunden Geräte:\n\n")
    rechner = os.popen("arp -a").readlines()
    for i in range(0, len(rechner)):                # braucht nicht -1, range immer < als Angabe ist
        nummer = str(i) + ": "                      # Nummer vor Listenobjekt
        print(nummer + rechner[i])
    index = input("Wähle deine Ziel-IP aus (Nummer, oder 'nicht in der Liste'): ")
    try:
        index = int(index)
        rechnerneu = rechner[index].split(" ")          # String --> Liste
        rechnerwert = rechnerneu[1]                     # Index der IP in der Liste
        rechner1 = rechnerwert.replace("(", "")
        ip = rechner1.replace(")", "")
        print("Verbindung zum Server wird aufgebaut...\n")# Entfernen der Klammern--> IP
        # print(ip)
    except ValueError:                                  #Wenn es nicht in der Liste ist
        if index == "nicht in der Liste":
            ip = input("IP-Adresse des Zielservers: ")
            print("Verbindung zum Server wird aufgebaut...\n")
        else:
            print("Ungültie Eingabe.")
elif eingabe == "nein":
    ip = input("IP-Adresse des Zielservers: ")
    print("Verbindung zum Server wird aufgebaut...\n")
else:
    print("Ungültige Eingabe.")

# Aufbau des Sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbindung mit dem Server
s.connect((ip, 50000))
name = str(input("Dein Name: ")) + ": "

# Abbruchbedingung
quitClient = False

try:
    while quitClient == False:
        nachricht = input("Nachricht: ")
        if nachricht == "quit()":                     # Abbruch der Kommunikation-->finally
            quitClient = True
            break
        nachricht = name + nachricht + "\n"
        s.send(nachricht.encode())
        antwort = s.recv(1024)
        print(antwort.decode())
finally:                                               # Trennen der Verbindung
    s.close()
    print("""\
\n
-------------------------------
Verbindung zum Server getrennt.
-------------------------------
""")
