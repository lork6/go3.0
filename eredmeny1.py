class eredmeny:
    def indit(self, koordlist, Szin):
        self.talatltak = []
        fekete = []

        coordlist = koordlist[:]
        szinlist = Szin[:]
        for sor in range(0, 21):
            if sor == 0 or sor == 20:
                for oszlop in range(1, 20):
                    coord = [sor,oszlop]
                    coordlist.append(coord)
                    szinlist.append("s")
        for sor in range(1,20):
            for oszlop in range(0, 21):
                if 1 > oszlop or 19 < oszlop:
                    coord = [sor, oszlop]
                    coordlist.append(coord)
                    szinlist.append("s")

        fekete_coord = []
        feher_coord = []
        for sor in range(1, 20):
            for oszlop in range(1, 20):
                coord = [sor, oszlop]
                if coord not in coordlist and coord not in self.talatltak:
                    talalt = self.kereso(coordlist, szinlist, coord)
                    if talalt != None:
                        listcoord = talalt[0]
                        if talalt[1] == "b":
                            for i in range(len(talalt[0])):
                                fekete_coord.append(listcoord[i])
                                self.talatltak.append(listcoord[i])

                        else:
                            for i in range(len(talalt[0])):
                                feher_coord.append(listcoord[i])
                                self.talatltak.append(listcoord[i])
                        koord = talalt[2]
                        for i in range(len(koord)):
                            fekete.append(koord[i])

        return fekete_coord, feher_coord

    def Coord_bealitas(self,coordlist,szinlist,coord):
        """itt  állitom be a koordinátákat nyolc írányba"""
        SzinCoord = []
        SCoordY = coord[0]  # itt állitom be a kezö jelenlegi coordinátákat
        SCoordX = coord[1]
        # beálitom a négy írányt
        coord_list = [[SCoordY+1,SCoordX],
                                [SCoordY,SCoordX+1], [SCoordY-1,SCoordX],[SCoordY,SCoordX-1]]
        # itt töltöm ki a SzinCoordináta nevezetü lisámat a megfelelö szinekel a coordniátákhoz
        for i in range(0, len(coord_list)):
            if coord_list[i] in coordlist:
                for j in range(0, len(coordlist)):
                    if coord_list[i] == coordlist[j]:
                        SzinCoord.append(szinlist[j])
            else:  # idde akkor jutt be ha az adott koordinátához nem tartozik szin(fekete vagy fehér)és "n" jelölöm
                SzinCoord.append("n")

        return coord_list, SzinCoord

    def uresKereso(self, coord, coord_list, szin_list, osszesTalaltbarat):
        """ezt a fügvényt akkor használom amikor üres területet keresek a pontozonak"""
        i = 0
        coorda = []
        talaltSzinek = []
        talaltkoord = []
        while i < len(coord_list):
            if "n" == szin_list[i] and coord_list[i] not in osszesTalaltbarat:
                coorda.append(coord_list[i])
            elif "s" != szin_list[i] and coord_list[i] not in osszesTalaltbarat:
                talaltSzinek.append(szin_list[i])
                talaltkoord.append(coord_list[i])
            i+=1
        return coorda, talaltSzinek, talaltkoord

    def kereso(self,coordlist, szinlist, coord):
        nemVizsgalt = []
        osszesTalaltbarat = []
        talaltSzinek = []
        talaltkoord  =[]
        nemVizsgalt.append(coord)
        osszesTalaltbarat.append(coord)
        while nemVizsgalt != []:
            a = nemVizsgalt[0]
            ertek = self.Coord_bealitas(coordlist, szinlist, a)
            coord_list = ertek[0]
            szin_list = ertek[1]
            pont = self.uresKereso(a, coord_list, szin_list, osszesTalaltbarat)
            coorda = pont[0]
            Szinek = pont[1]
            szinkoord = pont[2]
            if coorda != []:
                for i in range(len(coorda)):
                    osszesTalaltbarat.append(coorda[i])
                    nemVizsgalt.append(coorda[i])

            for j in range(len(Szinek)):
                talaltSzinek.append(Szinek[j])
                talaltkoord.append(szinkoord[j])

            del(nemVizsgalt[0])

        try:
            elso = talaltSzinek[0]
            egyezes = 0
            for i in range(1,len(talaltSzinek)):
                if elso == talaltSzinek[i]:
                    egyezes += 1
                else:
                    break

            if egyezes == len(talaltSzinek)-1:
                return osszesTalaltbarat, elso, talaltkoord
            else:
                for i in range(len(osszesTalaltbarat)):
                    self.talatltak.append(osszesTalaltbarat[i])
        except:
            pass








