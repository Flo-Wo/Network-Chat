"""!/usr/bin/python
-*- coding: UTF-8 -*-
Date: 02.02.2017
"""
import socket
import os
#Verschlüsselung
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Server IP, entweder Rechner im lokalen Netzwerk (WLan und Ethernet) oder
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
        print("Verbindung zum Server wird aufgebaut...\n")
        # print(ip)
    # Eingabe nicht konvertierbar --> "nicht in der Liste"
    except ValueError:
        # Manuelle Eingabe der IP, falls die Ziel-IP nicht in der Liste ist
        if index == "nicht in der Liste":
            ip = input("IP-Adresse des Zielservers: ")
            print("Verbindung zum Server wird aufgebaut...\n")
        # Der Nutzer kommt trotzdem noch zur manuellen Eingabe
        else:
            print("Ungültie Eingabe. Manuelle Eingabe der IP-Adresse folgt...")
# Manuelle Eingabe
elif eingabe == "nein":
    ip = input("IP-Adresse des Zielservers: ")
    print("Verbindung zum Server wird aufgebaut...\n")
else:
    print("Ungültige Eingabe.")

# Aufbau des Sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbindung mit dem Server --> Verbindungssocket
s.connect((ip, 50000))
name = str(input("Dein Name: ")) + ": "


#Verschlüsselung
#Schlüsselpaar wird erzeugt
clientkey = RSA.generate(1024)
#Public key wird extrahiert
clientkeypublic = clientkey.publickey()
#Public Key --> String, damit der Server ihn lesen kann
clientkey_lesbar = clientkeypublic.exportKey()

#Seperation des private keys, über PKCS1_OAEP-Verfahren
clientkeyprivate = PKCS1_OAEP.new(clientkey)

#öffentlicher Schlüssel des Clients muss nun zum Server
keysend = clientkey_lesbar
s.send(keysend.encode())

keyaccept = s.recv(1024)
publickeyserver = keyaccept.decode()
#--> öffentlicher Schlüssel des Servers liegt vor
chiffreserver = PKCS1_OAEP.new(publickeyserver)
#öff. Schlüssel des Servers über Verfahren nutzbar gemacht


# Abbruchbedingung
quitClient = False

# Kommunikationssocket
try:
    while quitClient == False:
        nachricht = input("Nachricht: ")
        # Abbruch der Kommunikation
        if nachricht == "quit()":
            nachricht = """\
            \n
-----------------------------------------
Der Client hat die Kommunikation beendet.
-----------------------------------------
            """
            s.send(nachricht.encode())
            quitClient = True
            break
        nachricht = name + nachricht + "\n"
        chiffrat = chiffreserver.encrypt(nachricht)
        s.send(chiffrat.encode())
        antwort = s.recv(1024)
        print(clientkeyprivate.decrypt(antwort.decode()))
# Trennen der Verbindung
finally:
    s.close()
    print("""\
\n
-------------------------------
Verbindung zum Server getrennt.
-------------------------------
""")
