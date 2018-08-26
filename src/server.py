import ptable

def main():
    print("Hello World")
    table = ptable.PokerTable()
    for x in range(7):
        player = ptable.Player(x)
        table.add_player(player)
        print(table)
    # t1.start()
    # p1 = ptable.Player(100)
    # print(p1)

if __name__ == '__main__':
    main()