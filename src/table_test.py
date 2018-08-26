import ptable

def main():
    table = ptable.PokerTable({"sb": 0.01, "bb": 0.02})
    for x in range(3):
        player = ptable.Player(x)
        table.add_player(player)
    table.start()
    print(table)

    # another_table = eval("ptable."+tblstr)

if __name__ == '__main__':
    main()