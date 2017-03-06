"""!/usr/bin/python
-*- coding: UTF-8 -*-
"""
import socket
import os
#Verschlüsselung
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# IP Rechner 1, entweder Rechner im lokalen Netzwerk (WLan und Ethernet) oder
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
    ip = input("IP-Adresse des Zielrechners: ")
    print("Verbindung zum Zielrechner wird aufgebaut...\n")
else:
    print("Ungültige Eingabe.")

# Aufbau des Sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbindung mit dem Zielrechner --> Verbindungssocket
s.connect((ip, 50000))
name = str(input("Dein Name: ")) + ": "


#Verschlüsselung
#Schlüsselpaar wird erzeugt
rechner2key = RSA.generate(1024)
#Public key wird extrahiert
rechner2keypublic = rechner2key.publickey()
#Public Key --> String, damit der Partner ihn lesen kann
rechner2key_lesbar = rechner2keypublic.exportKey()

#Seperation des private keys, über PKCS1_OAEP-Verfahren
rechner2keyprivate = PKCS1_OAEP.new(rechner2key)

#öffentlicher Schlüssel muss nun zum Partner
keysend = rechner2key_lesbar
s.send(keysend.encode())

keyaccept = s.recv(1024)
publickeyrechner1 = keyaccept.decode()
#--> öffentlicher Schlüssel des Rechner 1 liegt vor
chiffrerechner1 = PKCS1_OAEP.new(publickeyrechner1)
#öff. Schlüssel des Rechner 1 über Verfahren nutzbar gemacht


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
            chiffrat = chiffrerechner1.encrypt(nachricht)
            s.send(chiffrat.encode())
            quitRechner2 = True
            break
        nachricht = name + nachricht + "\n"
        # Verschlüssel der Nachricht
        chiffrat = chiffrerechner1.encrypt(nachricht)
        s.send(chiffrat.encode())
        antwort = s.recv(1024)
        #Entschlüsseln der empfangenen Nachricht
        print(rechner2keyprivate.decrypt(antwort.decode()))
# Trennen der Verbindung
finally:
    s.close()
    print("""\
\n
-----------------------------------------------
Verbindung zum Kommunikationspartner getrennt.
-----------------------------------------------
""")
