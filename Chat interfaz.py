# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of Slixmpp.

    See the file LICENSE for copying permission.
"""

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




while True:
    # Mostramos el menu
    menu()

    # solicituamos una opción al usuario
    opcionMenu = input("inserta un numero valor >> ")

    if opcionMenu == "1":

        print("------------------------REGRISTE SU CUENTA-------------------------")


        class RegisterBot(slixmpp.ClientXMPP):

            """
            A basic bot that will attempt to register an account
            with an XMPP server.

            NOTE: This follows the very basic registration workflow
                  from XEP-0077. More advanced server registration
                  workflows will need to check for data forms, etc.
            """

            def __init__(self, jid, password):
                slixmpp.ClientXMPP.__init__(self, jid, password)

                # The session_start event will be triggered when
                # the bot establishes its connection with the server
                # and the XML streams are ready for use. We want to
                # listen for this event so that we we can initialize
                # our roster.
                self.add_event_handler("session_start", self.start)

                # The register event provides an Iq result stanza with
                # a registration form from the server. This may include
                # the basic registration fields, a data form, an
                # out-of-band URL, or any combination. For more advanced
                # cases, you will need to examine the fields provided
                # and respond accordingly. Slixmpp provides plugins
                # for data forms and OOB links that will make that easier.
                self.add_event_handler("register", self.register)

            def start(self, event):
                """
                Process the session_start event.

                Typical actions for the session_start event are
                requesting the roster and broadcasting an initial
                presence stanza.

                Arguments:
                    event -- An empty dictionary. The session_start
                             event does not provide any additional
                             data.
                """
                self.send_presence()
                self.get_roster()

                # We're only concerned about registering, so nothing more to do here.
                self.disconnect()

            async def register(self, iq):
                """
                Fill out and submit a registration form.

                The form may be composed of basic registration fields, a data form,
                an out-of-band link, or any combination thereof. Data forms and OOB
                links can be checked for as so:

                if iq.match('iq/register/form'):
                    # do stuff with data form
                    # iq['register']['form']['fields']
                if iq.match('iq/register/oob'):
                    # do stuff with OOB URL
                    # iq['register']['oob']['url']

                To get the list of basic registration fields, you can use:
                    iq['register']['fields']
                """
                resp = self.Iq()
                resp['type'] = 'set'
                resp['register']['username'] = self.boundjid.user
                resp['register']['password'] = self.password

                try:
                    await resp.send()
                    logging.info("Account created for %s!" % self.boundjid)
                except IqError as e:
                    logging.error("Could not register account: %s" %
                                  e.iq['error']['text'])
                    self.disconnect()
                except IqTimeout:
                    logging.error("No response from server.")
                    self.disconnect()


        if __name__ == '__main__':
            # Setup the command line arguments.
            parser = ArgumentParser()

            # Output verbosity options.
            parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                                action="store_const", dest="loglevel",
                                const=logging.ERROR, default=logging.INFO)
            parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                                action="store_const", dest="loglevel",
                                const=logging.DEBUG, default=logging.INFO)

            # JID and password options.
            parser.add_argument("-j", "--jid", dest="jid",
                                help="JID to use")
            parser.add_argument("-p", "--password", dest="password",
                                help="password to use")

            args = parser.parse_args()

            # Setup logging.
            logging.basicConfig(level=args.loglevel,
                                format='%(levelname)-8s %(message)s')

            if args.jid is None:
                args.jid = input("Username: ")
            if args.password is None:
                args.password = input("Password: ")

            # Setup the RegisterBot and register plugins. Note that while plugins may
            # have interdependencies, the order in which you register them does
            # not matter.
            xmpp = RegisterBot(args.jid, args.password)
            xmpp.register_plugin('xep_0030')  # Service Discovery
            xmpp.register_plugin('xep_0004')  # Data forms
            xmpp.register_plugin('xep_0066')  # Out-of-band Data
            xmpp.register_plugin('xep_0077')  # In-band Registration

            # Some servers don't advertise support for inband registration, even
            # though they allow it. If this applies to your server, use:
            xmpp['xep_0077'].force_registration = True

            # Connect to the XMPP server and start processing XMPP stanzas.
            if xmpp.connect():

                xmpp.process(block=True)
                print("registro exitoso!")
            else:
                print("no se pudo establecer conexion")




    elif opcionMenu == "2":
        print("------------------------Incio de Sesion-------------------------")
        while True:
            submenu()
            opcionMenu = input("inserta un numero valor >> ")
            if opcionMenu == "1":
                print("------------------------Presencia-------------------------")


                class PingTest(slixmpp.ClientXMPP):

                    """
                    A simple Slixmpp bot that will send a ping request
                    to a given JID.
                    """

                    def __init__(self, jid, password, pingjid):
                        slixmpp.ClientXMPP.__init__(self, jid, password)
                        if pingjid is None:
                            pingjid = self.boundjid.bare
                        self.pingjid = pingjid

                        # The session_start event will be triggered when
                        # the bot establishes its connection with the server
                        # and the XML streams are ready for use. We want to
                        # listen for this event so that we we can initialize
                        # our roster.
                        self.add_event_handler("session_start", self.start)

                    async def start(self, event):
                        """
                        Process the session_start event.

                        Typical actions for the session_start event are
                        requesting the roster and broadcasting an initial
                        presence stanza.

                        Arguments:
                            event -- An empty dictionary. The session_start
                                     event does not provide any additional
                                     data.
                        """
                        self.send_presence()
                        self.get_roster()

                        try:
                            rtt = await self['xep_0199'].ping(self.pingjid,
                                                            timeout=10)
                            logging.info("Success! RTT: %s", rtt)
                        except IqError as e:
                            logging.info("Error pinging %s: %s",
                                         self.pingjid,
                                         e.iq['error']['condition'])
                        except IqTimeout:
                            logging.info("No response from %s", self.pingjid)
                        finally:
                            self.disconnect()

            if __name__ == '__main__':
                # Setup the command line arguments.
                parser = ArgumentParser()

                # Output verbosity options.
                parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                                    action="store_const", dest="loglevel",
                                    const=logging.ERROR, default=logging.INFO)
                parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                                    action="store_const", dest="loglevel",
                                    const=logging.DEBUG, default=logging.INFO)
                parser.add_argument("-t", "--pingto", help="set jid to ping",
                                    dest="pingjid", default=None)

                # JID and password options.
                parser.add_argument("-j", "--jid", dest="jid",
                                    help="JID to use")
                parser.add_argument("-p", "--password", dest="password",
                                    help="password to use")

                args = parser.parse_args()

                # Setup logging.
                logging.basicConfig(level=args.loglevel,
                                    format='%(levelname)-8s %(message)s')

                if args.jid is None:
                    args.jid = input("Username: ")
                if args.password is None:
                    args.password = input("Password: ")

                # Setup the PingTest and register plugins. Note that while plugins may
                # have interdependencies, the order in which you register them does
                # not matter.
                xmpp = PingTest(args.jid, args.password, args.pingjid)
                xmpp.register_plugin('xep_0030')  # Service Discovery
                xmpp.register_plugin('xep_0004')  # Data Forms
                xmpp.register_plugin('xep_0060')  # PubSub
                xmpp.register_plugin('xep_0199')  # XMPP Ping

                # Connect to the XMPP server and start processing XMPP stanzas.
                if xmpp.connect():

                    xmpp.process(block=True)
                    print("Bienvenido!")
                else:
                    print("no se pudo establecer conexion")

                if opcionMenu == "2":
                    print("------------------------Ingrese Su MENSAJE-------------------------")


                    class SendMsgBot(slixmpp.ClientXMPP):

                        """
                        A basic Slixmpp bot that will log in, send a message,
                        and then log out.
                        """

                        def __init__(self, jid, password, recipient, message):
                            slixmpp.ClientXMPP.__init__(self, jid, password)

                            # The message we wish to send, and the JID that
                            # will receive it.
                            self.recipient = recipient
                            self.msg = message

                            # The session_start event will be triggered when
                            # the bot establishes its connection with the server
                            # and the XML streams are ready for use. We want to
                            # listen for this event so that we we can initialize
                            # our roster.
                            self.add_event_handler("session_start", self.start)

                        def start(self, event):
                            """
                            Process the session_start event.

                            Typical actions for the session_start event are
                            requesting the roster and broadcasting an initial
                            presence stanza.

                            Arguments:
                                event -- An empty dictionary. The session_start
                                         event does not provide any additional
                                         data.
                            """
                            self.send_presence()
                            self.get_roster()

                            self.send_message(mto=self.recipient,
                                              mbody=self.msg,
                                              mtype='chat')

                            self.disconnect()


                    if __name__ == '__main__':
                        # Setup the command line arguments.
                        parser = ArgumentParser(description=SendMsgBot.__doc__)

                        # Output verbosity options.
                        parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                                            action="store_const", dest="loglevel",
                                            const=logging.ERROR, default=logging.INFO)
                        parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                                            action="store_const", dest="loglevel",
                                            const=logging.DEBUG, default=logging.INFO)

                        # JID and password options.
                        parser.add_argument("-j", "--jid", dest="jid",
                                            help="JID to use")
                        parser.add_argument("-p", "--password", dest="password",
                                            help="password to use")
                        parser.add_argument("-t", "--to", dest="to",
                                            help="JID to send the message to")
                        parser.add_argument("-m", "--message", dest="message",
                                            help="message to send")

                        args = parser.parse_args()

                        # Setup logging.
                        logging.basicConfig(level=args.loglevel,
                                            format='%(levelname)-8s %(message)s')

                        if args.jid is None:
                            args.jid = input("Username: ")
                        if args.password is None:
                            args.password = input("Password: ")
                        if args.to is None:
                            args.to = input("Send To: ")
                        if args.message is None:
                            args.message = input("Message: ")

                        # Setup the EchoBot and register plugins. Note that while plugins may
                        # have interdependencies, the order in which you register them does
                        # not matter.
                        xmpp = SendMsgBot(args.jid, args.password, args.to, args.message)
                        xmpp.register_plugin('xep_0030')  # Service Discovery
                        xmpp.register_plugin('xep_0199')  # XMPP Ping

                        # Connect to the XMPP server and start processing XMPP stanzas.
                        if xmpp.connect():

                            xmpp.process(block=True)
                            print("registro exitoso!")
                        else:
                            print("no se pudo establecer conexion")

                elif opcionMenu == "3":
                    print("------------------------Contactos Disponibles-------------------------")


                    class RosterBrowser(slixmpp.ClientXMPP):

                        """
                        A basic script for dumping a client's roster to
                        the command line.
                        """

                        def __init__(self, jid, password):
                            slixmpp.ClientXMPP.__init__(self, jid, password)
                            # The session_start event will be triggered when
                            # the bot establishes its connection with the server
                            # and the XML streams are ready for use. We want to
                            # listen for this event so that we we can initialize
                            # our roster.
                            self.add_event_handler("session_start", self.start)
                            self.add_event_handler("changed_status", self.wait_for_presences)

                            self.received = set()
                            self.presences_received = asyncio.Event()

                        async def start(self, event):
                            """
                            Process the session_start event.

                            Typical actions for the session_start event are
                            requesting the roster and broadcasting an initial
                            presence stanza.

                            Arguments:
                                event -- An empty dictionary. The session_start
                                         event does not provide any additional
                                         data.
                            """
                            future = asyncio.Future()

                            def callback(result):
                                future.set_result(None)

                            try:
                                self.get_roster(callback=callback)
                                await future
                            except IqError as err:
                                print('Error: %s' % err.iq['error']['condition'])
                            except IqTimeout:
                                print('Error: Request timed out')
                            self.send_presence()

                            print('Waiting for presence updates...\n')
                            await asyncio.sleep(10)

                            print('Roster for %s' % self.boundjid.bare)
                            groups = self.client_roster.groups()
                            for group in groups:
                                print('\n%s' % group)
                                print('-' * 72)
                                for jid in groups[group]:
                                    sub = self.client_roster[jid]['subscription']
                                    name = self.client_roster[jid]['name']
                                    if self.client_roster[jid]['name']:
                                        print(' %s (%s) [%s]' % (name, jid, sub))
                                    else:
                                        print(' %s [%s]' % (jid, sub))

                                    connections = self.client_roster.presence(jid)
                                    for res, pres in connections.items():
                                        show = 'available'
                                        if pres['show']:
                                            show = pres['show']
                                        print('   - %s (%s)' % (res, show))
                                        if pres['status']:
                                            print('       %s' % pres['status'])

                            self.disconnect()

                        def wait_for_presences(self, pres):
                            """
                            Track how many roster entries have received presence updates.
                            """
                            self.received.add(pres['from'].bare)
                            if len(self.received) >= len(self.client_roster.keys()):
                                self.presences_received.set()
                            else:
                                self.presences_received.clear()


                    if __name__ == '__main__':
                        # Setup the command line arguments.
                        parser = ArgumentParser()
                        parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                                            action="store_const",
                                            dest="loglevel",
                                            const=logging.ERROR,
                                            default=logging.ERROR)
                        parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                                            action="store_const",
                                            dest="loglevel",
                                            const=logging.DEBUG,
                                            default=logging.ERROR)

                        # JID and password options.
                        parser.add_argument("-j", "--jid", dest="jid",
                                            help="JID to use")
                        parser.add_argument("-p", "--password", dest="password",
                                            help="password to use")

                        args = parser.parse_args()

                        # Setup logging.
                        logging.basicConfig(level=args.loglevel,
                                            format='%(levelname)-8s %(message)s')

                        if args.jid is None:
                            args.jid = input("Username: ")
                        if args.password is None:
                            args.password = input("Password: ")

                        xmpp = RosterBrowser(args.jid, args.password)

                        # Connect to the XMPP server and start processing XMPP stanzas.
                        if xmpp.connect():

                            xmpp.process(block=True)
                            print("registro exitoso!")
                        else:
                            print("no se pudo establecer conexion")

                elif opcionMenu == "4":
                    print("------------------------UNETE A UN GRUPO-------------------------")


                    class MUCBot(slixmpp.ClientXMPP):

                        """
                        A simple Slixmpp bot that will greets those
                        who enter the room, and acknowledge any messages
                        that mentions the bot's nickname.
                        """

                        def __init__(self, jid, password, room, nick):
                            slixmpp.ClientXMPP.__init__(self, jid, password)

                            self.room = room
                            self.nick = nick

                            # The session_start event will be triggered when
                            # the bot establishes its connection with the server
                            # and the XML streams are ready for use. We want to
                            # listen for this event so that we we can initialize
                            # our roster.
                            self.add_event_handler("session_start", self.start)

                            # The groupchat_message event is triggered whenever a message
                            # stanza is received from any chat room. If you also also
                            # register a handler for the 'message' event, MUC messages
                            # will be processed by both handlers.
                            self.add_event_handler("groupchat_message", self.muc_message)

                            # The groupchat_presence event is triggered whenever a
                            # presence stanza is received from any chat room, including
                            # any presences you send yourself. To limit event handling
                            # to a single room, use the events muc::room@server::presence,
                            # muc::room@server::got_online, or muc::room@server::got_offline.
                            self.add_event_handler("muc::%s::got_online" % self.room,
                                                   self.muc_online)

                        def start(self, event):
                            """
                            Process the session_start event.

                            Typical actions for the session_start event are
                            requesting the roster and broadcasting an initial
                            presence stanza.

                            Arguments:
                                event -- An empty dictionary. The session_start
                                         event does not provide any additional
                                         data.
                            """
                            self.get_roster()
                            self.send_presence()
                            self.plugin['xep_0045'].join_muc(self.room,
                                                             self.nick,
                                                             # If a room password is needed, use:
                                                             # password=the_room_password,
                                                             wait=True)

                        def muc_message(self, msg):
                            """
                            Process incoming message stanzas from any chat room. Be aware
                            that if you also have any handlers for the 'message' event,
                            message stanzas may be processed by both handlers, so check
                            the 'type' attribute when using a 'message' event handler.

                            Whenever the bot's nickname is mentioned, respond to
                            the message.

                            IMPORTANT: Always check that a message is not from yourself,
                                       otherwise you will create an infinite loop responding
                                       to your own messages.

                            This handler will reply to messages that mention
                            the bot's nickname.

                            Arguments:
                                msg -- The received message stanza. See the documentation
                                       for stanza objects and the Message stanza to see
                                       how it may be used.
                            """
                            if msg['mucnick'] != self.nick and self.nick in msg['body']:
                                self.send_message(mto=msg['from'].bare,
                                                  mbody="I heard that, %s." % msg['mucnick'],
                                                  mtype='groupchat')

                        def muc_online(self, presence):
                            """
                            Process a presence stanza from a chat room. In this case,
                            presences from users that have just come online are
                            handled by sending a welcome message that includes
                            the user's nickname and role in the room.

                            Arguments:
                                presence -- The received presence stanza. See the
                                            documentation for the Presence stanza
                                            to see how else it may be used.
                            """
                            if presence['muc']['nick'] != self.nick:
                                self.send_message(mto=presence['from'].bare,
                                                  mbody="Hello, %s %s" % (presence['muc']['role'],
                                                                          presence['muc']['nick']),
                                                  mtype='groupchat')


                    if __name__ == '__main__':
                        # Setup the command line arguments.
                        parser = ArgumentParser()

                        # Output verbosity options.
                        parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                                            action="store_const", dest="loglevel",
                                            const=logging.ERROR, default=logging.INFO)
                        parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                                            action="store_const", dest="loglevel",
                                            const=logging.DEBUG, default=logging.INFO)

                        # JID and password options.
                        parser.add_argument("-j", "--jid", dest="jid",
                                            help="JID to use")
                        parser.add_argument("-p", "--password", dest="password",
                                            help="password to use")
                        parser.add_argument("-r", "--room", dest="room",
                                            help="MUC room to join")
                        parser.add_argument("-n", "--nick", dest="nick",
                                            help="MUC nickname")

                        args = parser.parse_args()

                        # Setup logging.
                        logging.basicConfig(level=args.loglevel,
                                            format='%(levelname)-8s %(message)s')

                        if args.jid is None:
                            args.jid = input("Username: ")
                        if args.password is None:
                            args.password = getpass("Password: ")
                        if args.room is None:
                            args.room = input("Ingrese el Grupo: ")
                        if args.nick is None:
                            args.nick = input("nickname: ")

                        # Setup the MUCBot and register plugins. Note that while plugins may
                        # have interdependencies, the order in which you register them does
                        # not matter.
                        xmpp = MUCBot(args.jid, args.password, args.room, args.nick)
                        xmpp.register_plugin('xep_0030')  # Service Discovery
                        xmpp.register_plugin('xep_0045')  # Multi-User Chat
                        xmpp.register_plugin('xep_0199')  # XMPP Ping

                        # Connect to the XMPP server and start processing XMPP stanzas.
                        if xmpp.connect():

                            xmpp.process(block=True)
                            print("registro exitoso!")
                        else:
                            print("no se pudo establecer conexion")

                elif opcionMenu == "5":
                    print("------------------------Editar Cuenta-------------------------")
                    # Setup the command line arguments.
                    parser = ArgumentParser()

                    # Output verbosity options.
                    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                                        action="store_const", dest="loglevel",
                                        const=logging.ERROR, default=logging.INFO)
                    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                                        action="store_const", dest="loglevel",
                                        const=logging.DEBUG, default=logging.INFO)

                    # JID and password options.
                    parser.add_argument("--oldjid", dest="old_jid",
                                        help="JID of the old account")
                    parser.add_argument("--oldpassword", dest="old_password",
                                        help="password of the old account")

                    parser.add_argument("--newjid", dest="new_jid",
                                        help="JID of the old account")
                    parser.add_argument("--newpassword", dest="new_password",
                                        help="password of the old account")

                    args = parser.parse_args()

                    # Setup logging.
                    logging.basicConfig(level=args.loglevel,
                                        format='%(levelname)-8s %(message)s')

                    if args.old_jid is None:
                        args.old_jid = input("Old JID: ")
                    if args.old_password is None:
                        args.old_password = input("Old Password: ")

                    if args.new_jid is None:
                        args.new_jid = input("New JID: ")
                    if args.new_password is None:
                        args.new_password = input("New Password: ")

                    old_xmpp = slixmpp.ClientXMPP(args.old_jid, args.old_password)
                    old_xmpp.ca_certs = "path/to/ca/cert"
                    old_xmpp.ssl_version = ssl.PROTOCOL_SSLv23

                    # If you are connecting to Facebook and wish to use the
                    # X-FACEBOOK-PLATFORM authentication mechanism, you will need
                    # your API key and an access token. Then you'll set:
                    # xmpp.credentials['api_key'] = 'THE_API_KEY'
                    # xmpp.credentials['access_token'] = 'THE_ACCESS_TOKEN'

                    # If you are connecting to MSN, then you will need an
                    # access token, and it does not matter what JID you
                    # specify other than that the domain is 'messenger.live.com',
                    # so '_@messenger.live.com' will work. You can specify
                    # the access token as so:
                    # xmpp.credentials['access_token'] = 'THE_ACCESS_TOKEN'

                    # If you are working with an OpenFire server, you may need
                    # to adjust the SSL version used:
                    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

                    # If you want to verify the SSL certificates offered by a server:
                    # xmpp.ca_certs = "path/to/ca/cert"

                    roster = []


                    def on_session(event):
                        roster.append(old_xmpp.get_roster())
                        old_xmpp.disconnect()


                    old_xmpp.add_event_handler('session_start', on_session)

                    if old_xmpp.connect():
                        old_xmpp.process(block=True)

                    if not roster:
                        print('No roster to migrate')
                        sys.exit()

                    new_xmpp = slixmpp.ClientXMPP(args.new_jid, args.new_password)
                    new_xmpp.ca_certs = "path/to/ca/cert"
                    new_xmpp.ssl_version = ssl.PROTOCOL_SSLv23


                    def on_session2(event):
                        new_xmpp.get_roster()
                        new_xmpp.send_presence()

                        logging.info(roster[0])
                        data = roster[0]['roster']['items']
                        logging.info(data)

                        for jid, item in data.items():
                            if item['subscription'] != 'none':
                                new_xmpp.send_presence(ptype='subscribe', pto=jid)
                            new_xmpp.update_roster(jid,
                                                   name=item['name'],
                                                   groups=item['groups'])
                        new_xmpp.disconnect()


                    new_xmpp.add_event_handler('session_start', on_session2)

                    # Connect to the XMPP server and start processing XMPP stanzas.
                    if xmpp.connect():

                        xmpp.process(block=True)
                        print("registro exitoso!")
                    else:
                        print("no se pudo establecer conexion")

    elif opcionMenu == "3":
        break
    else:
        print("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
