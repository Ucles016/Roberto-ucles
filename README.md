PROYECTO1REDES
#########

library
--------
Slixmpp is an MIT licensed XMPP library for Python 3.5+. It is a fork of
SleekXMPP.

Slixmpp's goals is to only rewrite the core of the library (the low level
socket handling, the timers, the events dispatching) in order to remove all
threads.

Building
--------
Enter the file, PROJECT1RED in the phyton version 3.7 console and run the code.
If you install the slixmpp library to import all plugins.
For the use of the program you will have to run it in pycharm since the use of .py files is more accessible, additionally there will be within the program a menu for what the user would like to do.
In the menu you can display the following options

1. Register:
You can enter the username and password, for the user you will have to place a name or alias in front of @ alumchat.xyz, and then enter your password
2. Ping connectivity:
Here you will only enter your username and password so that users know that you are online, that this happens through a ping.
3. Session and message:
In this part the user has to log in and then send the message, enter his username and password, then he can enter the recipient's address and finally the message.



Documentation and Testing
-------------------------

import logging
import sys
from getpass import getpass
from argparse import ArgumentParser
import ssl
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.asyncio import asyncio
import os

def menu():
    """
    Función que limpia la pantalla y muestra nuevamente el menu
    """
    os.system('cls')  # NOTA para windows tienes que cambiar clear por cls
    print("Selecciona una opción")
    print("\t1 - Registrarse")
    print("\t2 - Iniciar Sesion")

    print("\t3 - salir")


def submenu():
    """
    Función que limpia la pantalla y muestra nuevamente el menu
    """
    os.system('cls')  # NOTA para windows tienes que cambiar clear por cls
    print("Selecciona una opción")
    print("\t1 -  Preciencia")
    print("\t2 - Enviar Mensaje")
    print("\t3 -  Ver Contactos ")
    print("\t4-   Unirse a un grupo")
    print("\t5 - Editar cuenta.. ")

You must select an option from the main menu to be able to execute each chat function.



The Slixmpp plugins
-------------------------
 'xep_0030'  # Service Discovery
 'xep_0004' # Data forms
 'xep_0066'  # Out-of-band Data
 'xep_0077' # In-band Registration
 'xep_0199' #Timeout



PROJECT1RED Credits
---------------
Roberto Carlos Ucles Ortiz 9094-16913
Sergio  Josue Chavez Delgado 9094169223



