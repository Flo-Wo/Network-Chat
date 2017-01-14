"""!/usr/bin/python
-*- coding: UTF-8 -*-
Date: 14.01.2017
"""
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 50000))
s.listen(1)


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
            nachricht = name + str(input("Antwort: ")) + "\n"
            if nachricht == "quit()":
                quitServer = True
                break
            komm.send(nachricht.encode())
finally:
    s.close()
    print("Server wird geschlossen...")
