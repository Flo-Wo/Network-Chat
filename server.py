"""!/usr/bin/python
-*- coding: UTF-8 -*-
Date: 14.01.2017
"""
import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 50000))
s.listen(1)

#Server zeigt IP-Adresse über Systembefehl an
e = input("Eigene IP-Adresse anzeigen? (ja/nein) ")
if e == "ja":
    alleips = os.popen("ifconfig |grep inet").readlines()
    #mal 4 und mal 7?!
    alleips = alleips[4].split(" ")
    print("Deine IP-Adresse lautet: " + alleips[1])
    print("Server startet...\n")
elif e == "nein":
    print("Server startet...")
else:
    print("Ungültige Eingabe.\nServer startet...\n")

#Namenseingabe
name = str(input("Dein Name: ")) + ": "

#Abbruchbedingung
quitServer = False

try:
    while quitServer == False:
        #Verbindungssocket
        komm, addr = s.accept()
        while quitServer == False:
            #Kommunikationssocket
            data = komm.recv(1024)
            print(data.decode())
            nachricht = str(input("Antwort: "))
            #Abbruchanweisung, Client wird benachrichtigt
            if nachricht == "quit()":
                quitServer = True
                nachricht = """\
                \n
-----------------------------------------
Der Server hat die Kommunikation beendet.
-----------------------------------------
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
----------------------------------------------------
Verbindung zum Client getrennt, Server wird beendet.
----------------------------------------------------
""")
