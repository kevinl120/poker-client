import ptable
import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("1002x743")
    root.title("Poker Table")
    background_image = tk.PhotoImage(file="./resources/table.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0)

    # player label
    player_frame = tk.Frame(root, width=164, height=44)
    player_frame.place(x=419, y=575)
    player_label_img = tk.PhotoImage(file="./resources/player_label.png")
    player_label = tk.Label(player_frame, image=player_label_img, padx=0, pady=0, borderwidth=0, highlightthickness=0)
    player_label.image = player_label_img
    player_label.place(relx=0, rely=1, anchor=tk.SW)

    root.mainloop()

if __name__ == '__main__':
    main()