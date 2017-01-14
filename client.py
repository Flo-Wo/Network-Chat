"""!/usr/bin/python
-*- coding: UTF-8 -*-
Date: 14.01.2017
"""
import socket

#Eingabe der IP-Adresse
ip = input("IP-Adresse des Zielservers: ")

#Aufbau des Sockets
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Verbindung mit dem Server
s.connect((ip, 50000))
name = str(input("Dein Name: ")) + ": "

#Abbruchbedingung
quitClient = False

try:
    while quitClient == False:
        nachricht = input("Nachricht: ")
        if nachricht == "quit()":                   #Abbruch der Kommunikation-->finally
            quitClient = True
            break
        nachricht = name + nachricht +"\n"
        s.send(nachricht.encode())
        antwort = s.recv(1024)
        print(antwort.decode())
finally:                                            #Trennen der Verbdingung
    s.close()
    print("""\
\n
-------------------------------
Verbindung zum Server getrennt.
-------------------------------
""")
