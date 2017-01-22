"""!/usr/bin/python
-*- coding: UTF-8 -*-
Date: 14.01.2017
"""
import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 50000))
s.listen(1)

e = input("Eigene IP-Adresse anzeigen? (ja/nein) ")
if e == "ja":
    alleips = os.popen("ifconfig |grep inet").readlines()
    alleips = alleips[4].split(" ")
    print("Deine IP-Adresse lautet: " + alleips[1])
    print("Server startet...\n")
elif e == "nein":
    print("Server startet...\n")
else:
    print("Ungültige Eingabe.\nServer startet...\n")

name = str(input("Dein Name: ")) + ": "

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
            if nachricht == "quit()":
                quitServer = True
                nachricht = "\nDer Server hat die Kommunikation beendet.\n"
                komm.send(nachricht.encode())
                break
            else:
                #Konvertierung, Name dazu
                nachricht = name + nachricht + "\n"
                komm.send(nachricht.encode())
finally:
    s.close()
    print("""\
\n
----------------------------------------------------
Verbindung zum Client getrennt, Server wird beendet.
----------------------------------------------------
""")
