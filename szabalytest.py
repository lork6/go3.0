class Main:
    def __init__(self, szinlist, coordlist, coordY, coordX, szin):
        """ez a class felel a szabály végre hajtásáras"""
        self.szin_lista = szinlist
        self.coord = coordlist
        self.coordY = coordY
        self.coordX = coordX
        self.Szin = szin

        self.SCoordY = coordY
        self.SCoordX = coordX
        #menetem a szint és a coordinátát
        self.szin_mentes()
        self.Coord = [coordY, coordX]
        #létre hozom a szükséges listákat
        self.nemVizsgalt = []
        self.eredmeny = []
        self.osszesTalaltbarat = []

    def szin_mentes(self):
        if self.Szin[0] == "b":
            self.enemy_szin = "w"
        elif self.Szin[0] == "w":
            self.enemy_szin = "b"

    def Coord_bealitas(self):
        """itt  állitom be a koordinátákat """
        self.SzinCoord = []

        self.coord_list = [[self.SCoordY,self.SCoordX-1], [self.SCoordY+1,self.SCoordX],
                            [self.SCoordY,self.SCoordX+1], [self.SCoordY-1,self.SCoordX]]

        for i in range(0,len(self.coord_list)):
            if self.coord_list[i] in self.coord:
                for j in range(0,len(self.coord)):
                    if self.coord_list[i] == self.coord[j]:
                        self.SzinCoord.append(self.szin_lista[j])
            else:
                self.SzinCoord.append("n")

    def kereso(self):
        """itt keresem meg az ellentétes követés raktározom
            egy listában minta mit lerakot az ember"""
        self.talaltko = 0
        self.keresetKovek = []

        self.SCoordY = self.coordY #meg csinálom hogy lista szerinti coordináta legyen mert azzal dolgozom
        self.SCoordX = self.coordX

        self.Coord_bealitas()

        for q in range(0,4,1):
            """itt keresem meg hogy a lerakot kö melet van-e ellentétes szin"""
            #itt megnézem hogy biztosan neki fusake az ellenörzésnek
            #azaz megnézem hogy egyáltalán benevan-e a listában
            if self.coord_list[q] in self.coord:
                #ebben a for ban megnézem hogy hanyadik is a listában
                for p in range(0,len(self.coord)):
                    # itt ellenörzom hogy hanyadik
                    if self.coord[p] == self.coord_list[q] and self.szin_lista[p] == self.enemy_szin:
                        
                        self.keresetKovek.append(self.coord_list[q])

                        self.talaltko += 1
        i = 0
        if self.keresetKovek != []:
            """ha (igen) találtam akkor itt nézem hogy vanak e "barátai" """

            while i < len(self.keresetKovek):

                a = self.keresetKovek[i]

                """ itt annak a négy oldalát nézem meg hogy nekik vanake társaik"""


                self.SCoordY = a[0]
                self.SCoordX = a[1]

                self.Coord_bealitas() # egy definicio ahol a litáknak a koordinátáját meg változtatom a SCoord-náták szerint
                if a not in self.osszesTalaltbarat:
                    self.osszesTalaltbarat = []
                    self.osszesTalaltbarat.append(a)

                for h in range(0,len(self.SzinCoord),1):
                    if self.enemy_szin == self.SzinCoord[h]:
                        """itt a talált barátokat hozzá adom két listához egyikben az összeset tárolom
                            a másikban meg azokat amiket még nem vizsgáltam meg"""

                        self.osszesTalaltbarat.append(self.coord_list[h])
                        self.nemVizsgalt.append(self.coord_list[h])

                while self.nemVizsgalt != []:
                    """itt a nem vizsgáltakat vizsgálom meg"""
                    a = self.nemVizsgalt[0]
                    # a koordinátákat rögzitem hogy tudjak dolgozni velük
                    self.SCoordY = a[0]
                    self.SCoordX = a[1]

                    self.Coord_bealitas()

                    for h in range(0,4,1):
                        if self.enemy_szin == self.SzinCoord[h] and self.coord_list[h] not in self.osszesTalaltbarat:
                            """itt a talált barátokat hozzá adom két listához egyikben az összeset tárolom
                                a másikban meg azokat amiket még nem vizsgáltam meg"""

                            self.osszesTalaltbarat.append(self.coord_list[h])
                            self.nemVizsgalt.append(self.coord_list[h])
                    # itt törlöm azt a amit már megvizsgáltam
                    del(self.nemVizsgalt[0])

                if self.nemVizsgalt == []:
                    """ha nincsen több nemvizsgált akkor itt nézem meg a csoportnak az életét havan nem történik semi
                            ha nincsen akkor vissza tér a coordináták"""
                    self.nemVizsgalt[:] = self.osszesTalaltbarat
                    self.CsoportElet = 0

                    while self.nemVizsgalt != []:
                        a = self.nemVizsgalt[0]

                        self.SCoordY = a[0]
                        self.SCoordX = a[1]

                        self.Coord_bealitas()
                        w = 0
                        while w < len(self.SzinCoord):
                            if self.SzinCoord[w] == 'n':
                                """itt ellen örzöm a hogy vana élete a csoportnak és ha a szélénél van-e"""
                                self.CsoportElet += 1

                            w += 1

                        # itt ha a talált kö a zéléénv van akkor itt ellenörzöm és vonok le élettet
                        h = self.nemVizsgalt[0]

                        if h[0] == 1 or h[0] == 19:
                            self.CsoportElet -= 1

                        if h[1] == 1 or h[1] == 19:
                            self.CsoportElet -= 1

                        # itt törlöm azt a amit már megvizsgáltam
                        del(self.nemVizsgalt[0])

                    if self.CsoportElet == 0 and self.nemVizsgalt == []:
                        # ide akkor jut be a nincsn a csoportnak élete és vissza tér ha nem kell többet vizsigálnia
                        self.eredmeny = self.eredmeny + self.osszesTalaltbarat

                        if self.talaltko > 1:

                            self.talaltko -= 1
                        else:
                            return self.eredmeny
                    else:
                        if self.talaltko > 1:

                            self.talaltko -= 1
                        else:
                            return self.eredmeny

                i += 1

        return self.eredmeny