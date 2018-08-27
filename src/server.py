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

table = ptable.PokerTable({"sb": 1, "bb": 2})


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
        client.send(bytes("mpn"+str(table.add_player(ptable.Player(200))), "utf8"))
        time.sleep(0.1) # Sleep because mpn and table sometimes send together
        if table.cfg["players_at_table"] == 2:
            table.start()
        broadcast(bytes(str(table),"utf8"))
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    while True:
        msg = client.recv(BUFSIZ)
        if msg.decode("utf8")[0:3] != "lea":
            msg = msg.decode("utf8")
            # print(msg)
            if msg[0].isnumeric():
                perf_action(msg)
                broadcast(bytes(str(table),"utf8"))
        else:
            client.close()
            print("%s:%s has disconnected." % addresses[client])
            del addresses[client]
            table.remove_player(int(msg.decode("utf8")[3]))
            broadcast(bytes(str(table),"utf8"))
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""

    for sock in addresses:
        sock.send(bytes(prefix, "utf8")+msg)


def perf_action(msg):
    """Converts action string into specified action"""
    player_pos = int(msg[0])
    action = msg[1:4]
    
    if action == "fld": # fold
        table.player_folds(player_pos)
    elif action == "chk": # check
        table.player_checks(player_pos)
    elif action == "cal": # call
        table.player_calls(player_pos)
    elif action == "bet": # bet
        bet = int(msg[4:])
        table.add_player_bet(player_pos, bet)
    elif action == "muk": # muck
        table.player_mucks(player_pos)
    elif action == "sho": # show
        table.player_shows(player_pos)
    

if __name__ == '__main__':
    main()