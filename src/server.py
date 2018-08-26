import ptable

def main():
    table = ptable.PokerTable()
    # table = ptable.PokerTable({"sb": 0.01, "bb": 0.02})
    for x in range(3):
        player = ptable.Player(x)
        table.add_player(player)
    table.start()
    print(table.__repr__())
    print(table)
    # p1 = ptable.Player(100)
    # print(p1)

    # another_table = eval("ptable."+tblstr)

if __name__ == '__main__':
    main()