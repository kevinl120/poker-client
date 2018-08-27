"""Server for Poker Table application"""
import ptable
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

import time


addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

table = ptable.PokerTable({"sb": 0.01, "bb": 0.02})


def main():
    SERVER.listen(6)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        client.send(bytes("mpn"+str(table.add_player(ptable.Player(2))), "utf8"))
        time.sleep(0.1) # Sleep because mpn and table sometimes send together
        if table.cfg["players_at_table"] > 1:
            table.start()
        broadcast(bytes(str(table),"utf8"))
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg)
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del addresses[client]
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""

    for sock in addresses:
        sock.send(bytes(prefix, "utf8")+msg)


if __name__ == '__main__':
    main()