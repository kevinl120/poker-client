"""Script for Poker client"""
from ptable import PokerTable, Player
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from treys import Card


img_references = set()


def main():
    global root, bet_entry # better way of doing this?

    root = tk.Tk()
    bet_entry = tk.StringVar()
    root.geometry("1002x743")
    root.title("Poker Table")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    connect_to_server()

    root.mainloop()


### SOCKETS ###
def connect_to_server():
    global HOST, PORT, BUFSIZ, client_socket, receive_thread

    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()


def receive():
    """Handles receiving of messages."""
    global my_player_num, table
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
            if msg[0:3] == "mpn":
                my_player_num = int(msg[3])
            elif msg == "new":
                img_references.clear()
            elif msg[0:3] == "Pok":
                table = eval(msg)
                draw(root, table)
        except OSError:  # Possibly client has left the chat.
            break


# def send(event=None):  # event is passed by binders.
#     """Handles sending of messages."""
#     msg = my_msg.get()
#     my_msg.set("")  # Clears input field.
#     client_socket.send(bytes(msg, "utf8"))
#     if msg == "{quit}":
#         client_socket.close()
#         root.quit()

def send(msg):
    """Handles sending of messages."""
    client_socket.send(bytes(msg, "utf8"))



def on_closing(event=None):
    """This function is to be called when the window is closed."""
    client_socket.send(bytes("lea"+str(my_player_num), "utf8"))
    client_socket.close()
    root.quit()


### TKINTER ###

def fold_callback():
    send(str(my_player_num)+"fld")

def check_callback():
    send(str(my_player_num)+"chk")

def call_callback():
    send(str(my_player_num)+"cal")

def bet_callback(event=None):
    if bet_is_valid():
        send(str(my_player_num)+"bet"+bet_entry.get())

def bet_is_valid(event=None):
    cur_player = table.cfg["players"][table.cfg["current_turn"]]
    return int(bet_entry.get()) >= cur_player.possible_actions[2][0] and int(bet_entry.get()) <= cur_player.possible_actions[2][1]

def show_callback():
    send(str(my_player_num)+"sho")

def muck_callback():
    send(str(my_player_num)+"muk")

def draw(window, table):
    # Draw background
    background_image = tk.PhotoImage(file="./resources/table.png")
    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0)
    background_label.image = background_image
    img_references.add(background_image)

    # Hard-coded hole card coords
    card_coords = [[442, 531], [70, 400], [70, 164], [442, 33], [814, 164], [814, 400]]
    # Hard-coded player label coordinates
    label_coords = [[419, 575], [47, 444], [47, 208], [419, 77], [791, 208], [791, 444]]
    # Hard-coded bet coordinates
    bet_coords = [[460, 465], [220, 391], [220, 226], [461, 163], [700, 226], [700, 391]]
    # Hard-coded button coordinates
    button_coords = [[582, 525], [220, 470], [175, 261], [380, 106], [762, 170], [790, 357]]

    # Draw players and hole cards
    players = table.cfg["players"]
    for x in range(len(players)):
        # Start from my player and draw clockwise
        player_iter = (x+my_player_num)%len(players)

        if players[player_iter] is None:
            # If no player at this position, skip it
            continue
        elif not players[player_iter].hole_cards is None:
            # Draw hole cards
            cards_canvas = tk.Canvas(window, width=119, height=86, bd=0, highlightthickness=0)
            cards_canvas.place(x=card_coords[x][0], y=card_coords[x][1])
            if x == 0 or players[player_iter].show_cards:
                card0_img = tk.PhotoImage(file="./resources/cards-png/"+Card.int_to_str(players[player_iter].hole_cards[0])+".png")
                card1_img = tk.PhotoImage(file="./resources/cards-png/"+Card.int_to_str(players[player_iter].hole_cards[1])+".png")
            else:
                card0_img = tk.PhotoImage(file="./resources/cards-png/back.png")
                card1_img = tk.PhotoImage(file="./resources/cards-png/back.png")
            cards_canvas.create_image(0, 0, image=card0_img, anchor=tk.NW)
            cards_canvas.create_image(59, 0, image=card1_img, anchor=tk.NW)
            img_references.add(card0_img)
            img_references.add(card1_img)

            # Draw bets (if the player(s) bet)
            if not players[player_iter].current_bet == 0:
                bet_canvas = tk.Canvas(window, width=80, height=44, bg="#4A90E2", highlightthickness=0)
                bet_canvas.place(x=bet_coords[x][0], y=bet_coords[x][1])
                bet_canvas.create_text(40, 21, text=players[player_iter].current_bet, font=("Arial", "16"), fill="white")

        # Draw player labels
        player_label_canvas = tk.Canvas(window, width=164, height=44, bd=0, highlightthickness=0)
        player_label_canvas.place(x=label_coords[x][0], y=label_coords[x][1])
        if table.cfg["current_turn"] == player_iter:
            player_label_img = tk.PhotoImage(file="./resources/current_player_label.png")
        else: 
            player_label_img = tk.PhotoImage(file="./resources/player_label.png")
        player_label_canvas.create_image(0, 0, image=player_label_img, anchor=tk.NW)
        player_label_canvas.create_text(23, 21, text=str(player_iter), font=("Arial", "16"), fill="white")
        player_label_canvas.create_text(92, 21, text=players[player_iter].stack, font=("Arial", "16"), fill="white")
        img_references.add(player_label_img)

    # Draw dealer button
    if not table.cfg["button_pos"] is None:
        button_img = tk.PhotoImage(file="./resources/dealer_button.png")
        button_label = tk.Label(window, image=button_img, padx=0, pady=0, bd=0, highlightthickness=0)
        adjusted_button_pos = (table.cfg["button_pos"] + len(players) - my_player_num) % len(players)
        button_label.place(x=button_coords[adjusted_button_pos][0], y=button_coords[adjusted_button_pos][1])
        img_references.add(button_img)

    # Draw community cards
    c_card_coords = [336, 403, 470, 538, 605] # x-coords only. y-coords are all same
    c_card_y_coord = 282
    for x, card in enumerate(table.cfg["board"]):
        c_card_img = tk.PhotoImage(file="./resources/cards-png/"+Card.int_to_str(card)+".png")
        c_card_label = tk.Label(window, image=c_card_img, padx=0, pady=0, bd=0, highlightthickness=0)
        c_card_label.place(x=c_card_coords[x], y=c_card_y_coord)
        img_references.add(c_card_img)
    
    # Draw buttons if it is your turn
    if table.cfg["current_turn"] == my_player_num:
        # Hard-coded button coords
        button_coords = [22, 158, 294]
        button_y_coord = 678
        if len(table.cfg["players"][my_player_num].possible_actions) == 3:
            if table.cfg["players"][my_player_num].possible_actions[1] == "check":
                # Actions are fold/check/bet
                check_button_img = tk.PhotoImage(file="./resources/check_button.png")
                check_button = tk.Button(window, image=check_button_img, command=check_callback, bd=0, highlightthickness=0)
                check_button.place(x=button_coords[1], y=button_y_coord)
                img_references.add(check_button_img)
                bet_button_img = tk.PhotoImage(file="./resources/bet_button.png")
                bet_button = tk.Button(window, image=bet_button_img, command=bet_callback, bd=0, highlightthickness=0)
                bet_button.place(x=button_coords[2], y=button_y_coord)
                img_references.add(bet_button_img)
            else:
                # Actions are fold/call/raise
                call_button_img = tk.PhotoImage(file="./resources/call_button.png")
                call_button = tk.Button(window, image=call_button_img, command=call_callback, bd=0, highlightthickness=0)
                call_button.place(x=button_coords[1], y=button_y_coord)
                img_references.add(call_button_img)
                raise_button_img = tk.PhotoImage(file="./resources/raise_button.png")
                raise_button = tk.Button(window, image=raise_button_img, command=bet_callback, bd=0, highlightthickness=0)
                raise_button.place(x=button_coords[2], y=button_y_coord)
                img_references.add(raise_button_img)

            # Draw bet amount entry field
            entry_field = tk.Entry(window, textvariable=bet_entry, validate="focusin", validatecommand="bet_is_valid")
            entry_field.bind("<Return>", bet_callback)
            entry_field.place(x=600, y=685)

            fold_button_img = tk.PhotoImage(file="./resources/fold_button.png")
            fold_button = tk.Button(window, image=fold_button_img, command=fold_callback, bd=0, highlightthickness=0)
            fold_button.place(x=button_coords[0], y=button_y_coord)
            img_references.add(fold_button_img)
        elif len(table.cfg["players"][my_player_num].possible_actions) == 2:
            # Actions are show or muck
            show_button_img = tk.PhotoImage(file="./resources/show_button.png")
            show_button = tk.Button(window, image=show_button_img, command=show_callback, bd=0, highlightthickness=0)
            show_button.place(x=button_coords[1], y=button_y_coord)
            img_references.add(show_button_img)
            muck_button_img = tk.PhotoImage(file="./resources/muck_button.png")
            muck_button = tk.Button(window, image=muck_button_img, command=muck_callback, bd=0, highlightthickness=0)
            muck_button.place(x=button_coords[0], y=button_y_coord)
            img_references.add(muck_button_img)
            
    # Draw pot
    pot_canvas = tk.Canvas(window, width=100, height=22, bg="#1F922A", bd=0, highlightthickness=0)
    pot_canvas.place(x=500, y=385, anchor=tk.CENTER)
    pot_canvas.create_text(50, 11, text="Pot: "+str(table.cfg["pot"]), font=("Arial", "18"), fill="white")


if __name__ == '__main__':
    main()