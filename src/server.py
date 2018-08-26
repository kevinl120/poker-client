import ptable

def main():
    table = ptable.PokerTable(0.01, 0.02)
    for x in range(7):
        player = ptable.Player(x)
        table.add_player(player)
    table.start()
    print(table)
    # t1.start()
    # p1 = ptable.Player(100)
    # print(p1)

if __name__ == '__main__':
    main()