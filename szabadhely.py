import szel_rogzito

class Szabad:
    """ebben a class ban állapitom meg hogy nem e egy lehetettlen lépést akkar e teni az emberünk"""
    def __init__(self, coordlist, szinlist,szin,coord):
        # itt meg hívom a szél létre hozzo fügvényt amit aztán alkalmazni is fogok ( azért hogy a gép is pontosan tudja hogy a szélét nézi)
        szelek = szel_rogzito.go_szel()
        coord_list = szelek[0]
        szin_list = szelek[1]
        self.coordlist = coordlist[:]
        self.szinlist = szinlist[:]
        for j, coordJ in enumerate(coord_list):
            #itt adom hozzá a szélleknek a koordinátáit a coordináta listámhoz
            self.coordlist.append(coordJ)
            self.szinlist.append(szin_list[j])
        # globálisá teszem a tehendö kö szinét
        self.szin_bealitas(szin)
        self.szin = szin
        self.coord = coord
        self.osszesTalaltbarat = []

    def szin_bealitas(self,szin):
        """ebben a fügvénben változtatom meg a szinek helyzetét az akutuális kéréshez"""
        if szin == "b":
            self.szin = "b"
            self.enemyszin = "w"
        else:
            self.szin = "w"
            self.enemyszin = "b"

    def Coord_bealitas(self, coordlist, szinlist, coord):
        """itt  állitom be a koordinátákat nyolc írányba"""
        SzinCoord = []
        SCoordY = coord[0]  # itt állitom be a kezö jelenlegi coordinátákat
        SCoordX = coord[1]
        # ebben a listában állitom be a coordinátákat amik a jelenlegi koordináta körül helyezkedik el
        coord_list = [[SCoordY+1,SCoordX], [SCoordY,SCoordX+1], [SCoordY-1,SCoordX], [SCoordY,SCoordX-1]]
        # itt töltöm ki a SzinCoordináta nevezetü lisámat a megfelelö szinekel a coordniátákhoz
        for coordI in coord_list:
            if coordI in coordlist:
                for j, coordJ in enumerate(coordlist):
                    if coordI == coordJ:
                        SzinCoord.append(szinlist[j])
                        break
            else:  # idde akkor jutt be ha az adott koordinátához nem tartozik szin(fekete vagy fehér)és "n" jelölöm
                SzinCoord.append("n")
        # itt vissza tér a körbe lévö koordináttákkal és hozzájuk tartozo színel
        return coord_list, SzinCoord

    def ko_elet_ellenorzo(self, ellenseg, szin, coordlist, szinlist):
            """ebbe a függvényben értékellem ki hogy az adot kö ( ami a rakando mellet van) meg éle"""
            # rögzitem a jellelegi coordintákat
            coord = ellenseg
            beallitott = self.Coord_bealitas(coordlist, szinlist, coord)  # egy definicio ahol a litáknak a koordinátáját meg változtatom a SCoord-náták szerint
            coord_list = beallitott[0]
            SzinCoord = beallitott[1]
            self.szin_bealitas(szin)
            # le tisztázom a nemVizsgált listámat
            self.nemVizsgalt = []
            self.eredmeny = []
            if coord not in self.osszesTalaltbarat:
                self.osszesTalaltbarat = []
                self.osszesTalaltbarat.append(coord)
            for h, szine in enumerate(SzinCoord):
                if self.szin == szine:
                    """itt a talált barátokat hozzá adom két listához egyikben az összeset tárolom
                        a másikban meg azokat amiket még nem vizsgáltam meg"""
                    self.osszesTalaltbarat.append(coord_list[h])
                    self.nemVizsgalt.append(coord_list[h])

            while self.nemVizsgalt != []:
                """itt a nem vizsgáltakat vizsgálom meg"""
                coord = self.nemVizsgalt[0]
                # a koordinátákat rögzitem hogy tudjak dolgozni vel
                beallitott = self.Coord_bealitas(coordlist, szinlist,coord)
                # egy definicio ahol a litáknak a koordinátáját meg változtatom a SCoord-náták szerint
                coord_list = beallitott[0]
                SzinCoord = beallitott[1]
                for h in range(4):
                    if self.szin == SzinCoord[h] and coord_list[h] not in self.osszesTalaltbarat:
                        """itt a talált barátokat hozzá adom két listához egyikben az összeset tárolom
                            a másikban meg azokat amiket még nem vizsgáltam meg"""
                        self.osszesTalaltbarat.append(coord_list[h])
                        self.nemVizsgalt.append(coord_list[h])
                # itt törlöm azt a amit már megvizsgáltam
                del (self.nemVizsgalt[0])

            if self.nemVizsgalt == []:
                """ha nincsen több nemvizsgált akkor itt nézem meg a csoportnak az életét havan nem történik semi
                        ha nincsen akkor vissza tér a coordináták"""
                self.nemVizsgalt[:] = self.osszesTalaltbarat
                self.CsoportElet = 0
                terulet = []
                while self.nemVizsgalt != []:
                    coord = self.nemVizsgalt[0]
                    # egy definicio ahol a litáknak a koordinátáját meg változtatom a SCoord-náták szerint
                    beallitott = self.Coord_bealitas(coordlist, szinlist,coord)
                    coord_list = beallitott[0]
                    SzinCoord = beallitott[1]
                    w = 0
                    while w < len(SzinCoord):
                        if SzinCoord[w] == 'n' and coord_list[w] not in terulet:
                            """itt ellen örzöm a hogy vana élete a csoportnak és ha a szélénél van-e"""
                            self.CsoportElet += 1
                            terulet.append(coord_list[w])
                        w += 1
                    del (self.nemVizsgalt[0])

                if self.CsoportElet == 1 and self.nemVizsgalt == []:
                    # ide akkor jut be a nincsn a csoportnak élete és vissza tér ha nem kell többet vizsigálnia
                    return True
                elif self.nemVizsgalt == []:
                    return False

    def indito(self):
        """ebben aa függvénben kezdi el az ellenörzést """
        #rögzitem (copy) a eredeti szint ami majd jól fog jöni az ellenörzéskór
        self.szin_sz = self.szin[:]
        self.enemyszin_sz = self.enemyszin[:]
        #rögzitem (copy) a listákat amiket késöbb akkor pontosan ugyan igy használni
        self.coordlist_sz = self.coordlist[:]
        self.szinlist_sz = self.szinlist[:]
        # most meg hívom a coord ballitást amivel a lerakkando kö körülötti köveket
        beallit = self.Coord_bealitas(self.coordlist, self.szinlist, self.coord)
        coord_list = beallit[0]
        szin_list = beallit[1]
        #létre hozzok listákat amiben tárolni fogom a körülötte lévö kövekte tárolom a következö lépéshez
        coordNezedo = []
        szinNezedo = []
        for i in range(4):
            """ebbe a cikluban csekolom és tárolom a négy koordináttá, amiket késöb fogok meg vizsgálni"""
            if szin_list[i] != "n":
                #itt hozá adom azokat a köveket amiket megézem hogy körülötte van
                coordNezedo.append(coord_list[i])
                szinNezedo.append(szin_list[i])

        if len(coordNezedo) == 4:
            """idde akkor jutt be ha van körülötte kö"""
            ko_elet = 0
            for i, megnezet in enumerate(coordNezedo):
                #print("szin_sz:", self.szin_sz)
                if szinNezedo[i] == self.szin_sz:
                    """idde akkor jut be a program ha a rakando könek azzonos szin van 'mellete' """
                    a = self.ko_elet_ellenorzo(megnezet,self.szin_sz, self.coordlist, self.szinlist)
                    if a == False:
                        ko_elet += 1

                elif szinNezedo[i] == self.enemyszin_sz:
                    """idde akkor jutt be a program ha ellenséges szin van 'mellete' """
                    a = self.ko_elet_ellenorzo(megnezet, self.enemyszin_sz, self.coordlist, self.szinlist)
                    if a == True:
                        ko_elet += 1
            # itt értékelem ki a 4 nél kisseb akkor lelehet rakni azaz van vagy lesz élete
            if ko_elet > 0:
                return True
            else:
                return False
        else:
            """az akkor történik meg ha nincsen kö körülötte azaz bisztos van élete :)"""
            return True