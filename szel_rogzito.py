def go_szel():
    """ez a függvény arra szolgál hogy a gonak a széle is meg legyen jelölve"""
    szinlist = []
    coordlist = []
    #az első ciklusban az fölsö és az alsó széleket hozza létre
    for sor in range(0, 21):
        if sor == 0 or sor == 20:
            for oszlop in range(1, 20):
                coord = [sor, oszlop]
                coordlist.append(coord)
                szinlist.append("s")
    #a másodikban pedi a két oldalt az az jobb és bal oldatl
    for sor in range(1, 20):
        for oszlop in range(0, 21):
            if 1 > oszlop or 19 < oszlop:
                coord = [sor, oszlop]
                coordlist.append(coord)
                szinlist.append("s")
    # vissza tér azokkal a koordinátákkal amik a Goban a szélét jelentik
    return coordlist, szinlist

