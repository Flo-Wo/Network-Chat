"""!/usr/bin/python
-*- coding: UTF-8 -*-
"""
import socket
import os

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

try:
    while quitRechner1 == False:
        #Verbindungssocket
        komm, addr = s.accept()
        while quitRechner1 == False:
            #Kommunikationssocket
            data = komm.recv(1024)
            print(data.decode())
            nachricht = str(input("Antwort: "))
            #Abbruchanweisung, Komm.partner wird benachrichtigt
            if nachricht == "quit()":
                quitRechner1 = True
                nachricht = """\
                \n
--------------------------------------------------------
Der Kommunikationspartner hat die Kommunikation beendet.
--------------------------------------------------------
                """
                komm.send(nachricht.encode())
                break
            else:
                #Konvertierung, Name dazu
                nachricht = name + nachricht + "\n"
                komm.send(nachricht.encode())
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
