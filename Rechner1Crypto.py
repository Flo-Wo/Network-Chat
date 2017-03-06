"""!/usr/bin/python
-*- coding: UTF-8 -*-
"""
import socket
import os
#Verschlüsselung
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 50000))
s.listen(1)

#Zeigt IP-Adresse über Systembefehl an
e = input("Eigene IP-Adresse anzeigen? (ja/nein) ")
if e == "ja":
    alleips = os.popen("ifconfig |grep inet").readlines()
    alleips = alleips[4].split(" ")
    print("Deine IP-Adresse lautet: " + alleips[1])
    print("Rechner 1 startet...\n")
elif e == "nein":
    print("Rechner 1 startet...")
else:
    print("Ungültige Eingabe.\nRechner 1 startet...\n")

#Namenseingabe
name = str(input("Dein Name: ")) + ": "

#Abbruchbedingung
quitRechner1 = False

#Akzeptieren der Verbindung
komm, addr = s.accept()

#Verschlüsselung
#Schlüsselpaar wird erzeugt
rechner1key = RSA.generate(1024)
#Public key wird extrahiert
rechner1keypublic = rechner1key.publickey()
#Public Key --> String, damit der Partner ihn lesen kann
rechner1key_lesbar = rechner1keypublic.exportKey()

#Seperation des private keys, über PKCS1_OAEP-Verfahren
rechner1keyprivate = PKCS1_OAEP.new(rechner1key)

keyaccept = komm.recv(1024)
publickeyrechner2 = keyaccept.decode()
#--> öffentlicher Schlüssel des Partners liegt nun vor
chiffrerechner2 = PKCS1_OAEP.new(publickeyrechner2)

#Versenden des öffentlichen Schlüssels an den Partner
komm.send(rechner1key_lesbar)


try:
    while quitRechner1 == False:
        #Verbindungssocket
        #siehe oben
        #komm, addr = s.accept()
        while quitRechner1 == False:
            #Kommunikationssocket
            data = komm.recv(1024)
            #Entschlüsseln der empfangenen Nachricht
            print(rechner1keyprivate.decrypt(data.decode())
            nachricht = str(input("Antwort: "))
            #Abbruchanweisung, Partner wird benachrichtigt
            if nachricht == "quit()":
                quitRechner1 = True
                nachricht = """\
                \n
--------------------------------------------------------
Der Kommunikationspartner hat die Kommunikation beendet.
--------------------------------------------------------
                """
                # Verschlüssel der Nachricht
                chiffrat = chiffrerechner2.encrypt(nachricht)
                komm.send(chiffrat.encode())
                break
            else:
                #Konvertierung, Name dazu
                nachricht = name + nachricht + "\n"
                # Verschlüssel der Nachricht
                chiffrat = chiffrerechner2.encrypt(nachricht)
                komm.send(chiffrat.encode())
#Ende der Kommunikation
finally:
    komm.close()
    s.close()
    print("""\
\n
-------------------------------------------------------------
Verbindung zum Partner getrennt, Kommunikation wird beendet.
-------------------------------------------------------------
""")
