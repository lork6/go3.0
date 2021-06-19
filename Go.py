from tkinter import *
from tkinter import messagebox
import winsound, random

class Main(Canvas):
    def __init__(self, master=None):
        """itt indul ell palya kirajzolás"""
        if master != None:
            #felületekre osztom fel a az ablakot
            Canvas.__init__(self,master=master,bg="sandy brown",height=600, width=600)
            #self.pack(side=LEFT)
            self.grid(row=0,padx=5,pady=5)
            self.frame = Frame(master=master)
            #self.frame.pack(side=TOP)
            self.frame.grid(row=0, column=1, padx=5, pady=5, sticky=N)
            self.master = master
            self.magas = 600
            self.szeles = self.magas
            # fügvényeket hívok meg hogy elinduljon helyesen a program
            self.goPalya()
            self.gombok()
            self.gomb_rako()
            self.menu()
            self.nullazo()
            self.master.bind('<Configure>', self.meretezo)

    def menu(self):
        """ebben a fügvényben jelenitem meg a menut"""
        menubar = Menu(self.master)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Új jaték    ctr+n", command=self.uj_jatek)
        menu1.add_separator()
        menu1.add_command(label="Mentés", )
        menu1.add_command(label="Betöltés", )
        menu1.add_separator()
        menu1.add_command(label="beállitások", )
        menu1.add_command(label="Kilépés", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=menu1)
        # helper
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Segítség", command=self.Segitseg_web)
        helpmenu.add_separator()
        helpmenu.add_command(label="Névjegy", command=self.nevjegy)
        menubar.add_cascade(label="Súgó", menu=helpmenu)
        self.master.config(menu=menubar)

    def Segitseg_web(self):
        """ez a függvény meg nyít egy internetes oldalt ahol a felhasználonak
        meg mutatja a játék szabályokat"""
        import webbrowser
        # ez az url cim ami egy weboldara mutat ahol elmagyaraza a go szalyokat
        url = "http://mek.oszk.hu/00100/00136/html/szabaly.htm"
        try:
            # itt meg pobállok egy uj boöngészöt nyittni
            webbrowser.open_new_tab(url)
        except:
            messagebox.showwarning("browser hiba", "Nem sikerült megnyítni a weboldalt")

    def uj_jatek(self,event=None):
        """ebbe a függvénybe akkor jut be a az illető uj játékot akkar kezdeni"""
        m = messagebox.askquestion(title="Uj jaték", message="Biztosan új játékot akkrasz kezdeni?")
        if m == "yes":
            # törlom a régi go táblát
            self.destroy()
            #létre hozzom az ujat
            Canvas.__init__(self, master=self.master, bg="sandy brown", height=600, width=600)
            self.grid(row=0, padx=5, pady=5)
            self.goPalya()
            self.gombok()
            self.kovet()
            self.nullazo()

    def nevjegy(self):
        """itt írom ki a programrol a tulajdonságati a névjegy menu sor allat"""
        ablak = Tk()
        ablak.title("Névjegy")
        ablak.geometry("250x100")
        data = open("config.txt", "r")
        versio = data.read()
        irando = "Program version: "+ versio+ \
                 "\n"+ "Programot készítette: Lévay Lőrinc"+\
                 "\n"+"Python 3.6.0 program nyelvelben készítve"
        Label(ablak,text=irando).grid()

    def nullazo(self):
        """ebben a fügvényben minden értéket béállitok nullára azaz kezdö értékre"""
        # itt adok értékeket a számoláshoz
        self.B_pontszam = 0
        self.B_fogolyszam = 0
        self.W_pontszam = 0
        self.W_fogolyszam = 0
        self.lepesekszam  = 0
        # megjelenittem a kezdö értékeket
        self.B_pontszamText.set(self.B_pontszam)
        self.B_fogolyszam_Text.set(self.B_fogolyszam)
        self.W_pontszamText.set(self.W_pontszam)
        self.W_fogolyszam_Text.set(self.W_fogolyszam)
        self.lepesekszam_Text.set(self.lepesekszam)
        self.Kovetkezo_lepes = self.can.create_oval(30 - 13, 30 - 13, 30 + 13, 30 + 13, fill="black")

        # értékeket adok meg változoknak
        self.koSzin = 0
        self.szin = "White"
        #self.szin = "black"
        self.passzolo_szam = 0
        # listákat hozzok létre amikben a go állást tárolom
        self.Coord_list = []
        self.Szin_list = []
        self.ko_nev_list = []
        self.lista = []
        self.sz_lista = []
        self.sz_fogoly = []
        self.sz_fogoly_szin = []
        self.pontok_nev = []
        self.nev_fogoly = []
        self.sz_fogoly_nev = []

    def gomb_rako(self):
        # itt jelenetödik meg a passz gombok
        Button(self.frame, text="Fekete passz", command=self.fekete_passzolo).grid(row=0, column=0, padx=5, pady=5, sticky=W)  # TODO megcsinálni hogy lehetsen passzolni
        Button(self.frame, text="Fehér passz", command=self.feher_passzolo).grid(row=0, column=1, padx=5, pady=5, sticky=W)

        #fekete box
        feketebox= LabelFrame(self.frame, text="Fekete")
        feketebox.grid(row=1, column=0, padx=5, pady=5)
        # itt a pontszámokat írom ki
        self.B_pontszamText = StringVar()
        Label(feketebox, text="pontszam:").grid(row=0,column=0,padx=5,pady=5)
        B_pontszam_L = Label(feketebox, textvariable = self.B_pontszamText)
        B_pontszam_L.grid(row=0,column=1,padx=5,pady=5)
        # itt a fekete foglyok számát írom ki
        self.B_fogolyszam_Text = StringVar()
        Label(feketebox, text="fogolyok:").grid(row=1,column=0,padx=5,pady=5)
        Label(feketebox, textvariable = self.B_fogolyszam_Text).grid(row=1, column=1, padx=5, pady=5)

        #fehér box van
        feherbox = LabelFrame(self.frame, text="Fehér")
        feherbox.grid(row=1, column=1, padx=5, pady=5)
        #itt a pontszámokat írom ki
        self.W_pontszamText = StringVar()
        Label(feherbox, text="pontszam:").grid(row=0,column=0,padx=5,pady=5)
        Label(feherbox, textvariable=self.W_pontszamText).grid(row=0, column=1, padx=5, pady=5)
        # itt a FEHÉR foglyok számát írom ki
        self.W_fogolyszam_Text = StringVar()
        Label(feherbox, text="fogolyok:").grid(row=1,column=0,padx=5,pady=5)
        Label(feherbox, textvariable=self.W_fogolyszam_Text).grid(row=1, column=1)
        #itt jelenitödik meg a lépések szama kiírás
        Label(self.frame, text = "Lépések száma:").grid(row=2,sticky=W)
        self.lepesekszam_Text = StringVar()
        Label(self.frame, textvariable=self.lepesekszam_Text).grid(row=2, column=0,sticky=E)
        self.lepesekszam = 0
        self.lepesekszam_Text.set(self.lepesekszam)

        self.can = Canvas(self.frame, height=60, width=60)
        self.can.grid(row=2,column=1)
        self.nyertesText = StringVar()
        self.nyertesSzamText = StringVar()
        Label(self.frame, textvariable=self.nyertesText).grid(row=3, column=0, sticky=E)
        Label(self.frame, textvariable=self.nyertesSzamText).grid(row=3, column=1, sticky=W)

    def szabaly_ellenorzo(self, coord, milyenszin):
        coord_lista = self.Coord_list[:]
        szin_lista = self.Szin_list[:]
        coord_lista.append(coord)
        szin_lista.append(milyenszin)
        import szabalytest
        torlendo = szabalytest.Main(szinlist=szin_lista, coordlist=coord_lista, coordY=coord[0],
                                     coordX=coord[1], szin=milyenszin)
        eredmenyek = torlendo.kereso()
        if eredmenyek != []:
            for eredmeny in eredmenyek:
                for i, coordI in enumerate(coord_lista):
                    if eredmeny == coordI:
                        del(coord_lista[i])
                        del(szin_lista[i])
            coord_lista.append(coord)

            if len(coord_lista) == len(self.sz_lista) and len(self.sz_lista) != 0:
                # mert a listák hossza meg egyezik ezért ellenőrzom hogy minden elemük egyelő-e
                egyezes_szama = 0
                for coordI in coord_lista:
                    for szabaly in self.sz_lista:
                        if coordI == szabaly:
                            egyezes_szama += 1
                if egyezes_szama == len(self.sz_lista):
                    return False
                else:
                    return True
            else:
                #azért mert a listák nem egy hoszuak ami boztos hogy nem fog egyezni ezért nem is ellenőrzom hanem False vissza térek
                return True
        else:
            return True

    def kovetkezo_lepes_rajzolo(self):
        """ez rajzolja ki oldalt a kovetkezo ko szinét"""
        if self.szin[0] == "b":
            self.Kovetkezo_lepes = self.can.create_oval(30 - 13, 30 - 13, 30 + 13, 30 + 13, fill="white")
        else:
            self.Kovetkezo_lepes = self.can.create_oval(30 - 13, 30 - 13, 30 + 13, 30 + 13, fill="black")

    def goPalya(self):
        """ez rajzolja  ki a magát a go pályát"""
        i = 0
        c = self.oszto_szamolo()
        a = (c*20)/172
        metol = c
        meddig = (c*20) - c
        while i < 20:
            if i == 1 or i == 19:  # ezek a szélsö vonolak amik egy kicsit vastagabak
                self.create_line(c * i, metol, c * i, meddig, fill='black', width=1.5)
                self.create_line(metol, c * i, meddig, c * i, fill='black', width=1.5)
            if i == 4:  # ez fölsö sor pontolókat rajzolja ki
                x = c * i
                y = c * i
                self.create_oval(x - a, y - a, x + a, y + a, fill='black')
                x1 = c * 10
                x2 = c * 16
                self.create_oval(x1 - a, y - a, x1 + a, y + a, fill='black')
                self.create_oval(x2 - a, y - a, x2 + a, y + a, fill='black')
            if i == 10:  # ez a középső pontokat rajzolja ki
                x = c * 4
                y = c * i
                self.create_oval(x - a, y - a, x + a, y + a, fill='black')
                x1 = c * 10
                x2 = c * 16
                self.create_oval(x1 - a, y - a, x1 + a, y + a, fill='black')
                self.create_oval(x2 - a, y - a, x2 + a, y + a, fill='black')
            if i == 16:  # itt az also pontokat rajzolom ki
                x = c * 4
                y = c * i
                self.create_oval(x - a, y - a, x + a, y + a, fill='black')
                x1 = c * 10
                x2 = c * 16
                self.create_oval(x1 - a, y - a, x1 + a, y + a, fill='black')
                self.create_oval(x2 - a, y - a, x2 + a, y + a, fill='black')
            # itt rajzololm ki y és az x vonalakat
            self.create_line(c * i, metol, c * i, meddig, )
            self.create_line(metol, c * i, meddig, c * i)
            i = i + 1
            self.addtag_all("all")

    def kovet(self):
        """ez felel hogy meg felelö kevet rakjak le és következen """
        if self.koSzin == 0:
            self.szin = "black"
            self.koSzin = 1
            self.rakoSzin = "b"
            self.frendySzin = 'white'

        elif self.koSzin == 1:
            self.szin = "white"
            self.koSzin = 0
            self.rakoSzin = "w"
            self.frendySzin = 'black'

    def coord_csinalo(self, x, y):
        """itt szamolom ki a potos koordinátát a lerakott könek"""
        oszto = self.oszto_szamolo()
        oszto_fele = oszto/2
        self.mutatX = (x)
        self.mutatY = (y)
        self.tablaX = int(self.mutatX / oszto)
        self.tablaY = int(self.mutatY / oszto)

        if self.mutatX % self.meret > oszto_fele:
            self.tablaX += 1
        self.tablaY = int(self.mutatY / oszto)
        if self.mutatY % self.meret > oszto_fele:
            self.tablaY += 1
        return self.tablaX, self.tablaY

    def oszto_szamolo(self):
        size = self.magas
        self.meret = int(size) / 20
        self.koMeret = self.meret / 2
        return self.meret

    def goKoLerak(self, event):
        """ez álapitja meg hogy hova kell raknia követ"""
        # self.palya azt jelenti hogy bele léptek
        self.palya = 1
        self.w = 0
        self.frendyCoord = []
        self.frendly = 0
        self.mentve = 1
        coords = self.coord_csinalo(event.x, event.y)
        oszto = self.oszto_szamolo()
        # rögzitem a coordinátákat
        self.tablaX = coords[0]
        self.tablaY = coords[1]
        coord = [self.tablaY, self.tablaX]
        # importálom a szabad hely függvényt
        import szabadhely
        self.kovet()
        Szabaly = szabadhely.Szabad(self.Coord_list, self.Szin_list, self.rakoSzin[0],coord )
        szabad = Szabaly.indito()
        nem_ellozo = self.szabaly_ellenorzo(coord,self.szin)
        if 0 < self.tablaY < 20 and 0 < self.tablaX < 20 and coord not in self.Coord_list and nem_ellozo and szabad:
            self.ko_lerako()
            self.kovetkezo_lepes_rajzolo()
        else:
            # ez akkor kell amikor nem lehet nem ended le rakni követ és a helyes szin maradjon meg
            self.kovet()

    def ko_leteves_sound(self):
        #itt játszodik le a hang
        winsound.PlaySound('koandwood2.wav', winsound.SND_FILENAME)
    def ko_levetel_sound(self):
        #itt játszodik le a hang
        winsound.PlaySound('levetel.wav', winsound.SND_FILENAME)

    def ko_lerako(self):
        """ez rakja le a követe és jeleniti meg és a visszának memorizálja a lépéseket"""
        # meg hívom a szabályt
        import szabalytest
        Szabaly = szabalytest.Main(self.Szin_list, self.Coord_list, self.tablaY, self.tablaX, self.rakoSzin[0])
        # itt jelenitödik meg a lerakott kö
        self.koNev = self.create_oval(self.tablaX * self.meret - self.koMeret,
                                              self.tablaY * self.meret - self.koMeret,
                                              self.tablaX * self.meret + self.koMeret,
                                              self.tablaY * self.meret + self.koMeret,
                                               fill=self.szin)
        try: # ha már léptek akkor a jelzést eltünteti
            self.delete(self.mostani)
        except:
            pass
        # ez jelöli a legutolso lépést egy kiseb körrel
        self.mostani = self.create_oval(self.tablaX * self.meret - self.koMeret/1.8,
                                        self.tablaY * self.meret - self.koMeret/1.8,
                                        self.tablaX * self.meret + self.koMeret/1.8,
                                        self.tablaY * self.meret + self.koMeret/1.8,
                                        outline=self.frendySzin)
        # bealitom atagad ami méretezés hez kell
        self.addtag_all("all")
        self.sz_lista.clear()
        # hozzá adom a listák hozz az adatokat
        coord = [self.tablaY, self.tablaX]
        self.Coord_list.append(coord)
        self.ko_nev_list.append(self.koNev)
        self.Szin_list.append(self.rakoSzin)
        # szabályt hívok meg
        szabaly = Szabaly.kereso()
        #print(szabaly)
        #itt játsza le a hangot
        if szabaly == []:
            self.ko_leteves_sound()
        else:
            self.ko_levetel_sound()
        self.szabaly_torlo(szabaly)
        # kiírom a lépések számát
        self.lepesekszam += 1
        self.lepesekszam_Text.set(self.lepesekszam)
        # nullázom a psszolo értéket amivel számol hogy kétszer egymás uto lehesen passzolni
        self.passzolo_szam = 0

    def Ko_torlo(self, event=None):
        """ebben a fügvényben törlöm ki azt a követt amire a felhaszálo jobb egér gombal kattint"""
        coords = self.coord_csinalo(event.x, event.y)
        self.tablaX = coords[0]
        self.tablaY = coords[1]
        coord = [self.tablaY, self.tablaX]
        i = 0
        while i < len(self.Coord_list):
            # megnézem coordináta szernit hogy melyiket kell levenem
            if coord == self.Coord_list[i]:
                # aztán leszedem és kiszedem a listákbol is az adataikat
                if coord == self.Coord_list[len(self.Coord_list) - 1]:
                    self.delete(self.mostani)

                self.delete(self.ko_nev_list[i])
                del(self.Coord_list[i])
                del(self.ko_nev_list[i])
                del(self.Szin_list[i])
            i += 1

    def szabaly_torlo(self,torlendo):
        """itt törlöm a szabálytest bol vissza térö koordinátán lévö köveket"""
        if len(torlendo) == 1:
            # ez felügyeli azt hogy nel jöhessen létere ugyan az a helyzet mint az előzö körben
            #self.sz_lista=torlendo[0]
            self.sz_lista=self.Coord_list[:]

        if torlendo != []:
            i = 0
            while i < len(torlendo):
                j = 0
                while j < len(self.Coord_list):
                    if torlendo[i] == self.Coord_list[j]:
                        # törlom a követ a táblárol és a listákbol a tulajdonságait
                        self.delete(self.ko_nev_list[j])
                        del (self.Coord_list[j])
                        del (self.ko_nev_list[j])
                        del (self.Szin_list[j])
                    j += 1
                i += 1
            # megszámolom a levet köveket és kiírom mint fogolyszam
            if self.szin[0] == "b": # fekete
                self.B_fogolyszam+=len(torlendo)
                self.B_fogolyszam_Text.set(self.B_fogolyszam)
            else: # fehér
                self.W_fogolyszam += len(torlendo)
                self.W_fogolyszam_Text.set(self.W_fogolyszam)

    def fekete_passzolo(self):
        """itt töl el hogy  mindkét passzolt e és ha igen akkor vége legyen a játéknak"""
        if self.szin[0] == "w":
            self.passzolo_szam += 1
            self.kovet()
            self.kovetkezo_lepes_rajzolo()
            if self.passzolo_szam == 2:
                self.passz_vege()

    def feher_passzolo(self):
        """itt töl el hogy  mindkét passzolt e és ha igen akkor vége legyen a játéknak"""
        if self.szin[0] == "b":
            self.passzolo_szam += 1
            self.kovet()
            self.kovetkezo_lepes_rajzolo()
            if self.passzolo_szam == 2:
                self.passz_vege()

    def jobbra(self,event):
        if self.McoordX <= 18:
            self.McoordX += 1
            self.cntrol_L()
    def balra(self,event):
        if self.McoordX >= 2:
            self.McoordX -= 1
            self.cntrol_L()
    def fel(self,event):
        if self.McoordY >= 2:
            self.McoordY -= 1
            self.cntrol_L()
    def le(self,event):
        if self.McoordY <= 18:
            self.McoordY += 1
            self.cntrol_L()

    def kaja_restart(self):
        if self.restart == 1:
            self.restart -= 1
            self.delete(self.kaja)
        else:
            kor = self.oszto_szamolo()
            fele = kor / 2
            self.delete(self.kaja)
            self.KcoordX = random.randint(2, 18)
            self.KcoordY = random.randint(2, 18)
            self.kaja = self.create_oval(self.KcoordX * kor - fele, self.KcoordY * kor - fele,
                                         self.KcoordX * kor + fele,
                                         self.KcoordY * kor + fele, fill="black")
            self.kaja_elet = random.randint(13,20)
            self.restart = 1

    def kaja_lepteto(self):
        kor = self.oszto_szamolo()
        fele = kor / 2
        if self.kaja_elet == 0:
            self.kaja_restart()
        else:
            if self.KlepesSzam == 0:
                self.KlepesSzam = random.randint(1, self.kaja_elet-int((self.kaja_elet/2)))
                coord = [self.McoordX, self.McoordY]
                koord = [self.KcoordX, self.KcoordY]
                if coord[0]+coord[1] > koord[0]+koord[1]:
                    self.merre = random.randint(0,1)
                else:
                    self.merre = random.randint(2, 3)

            if self.merre == 0:
                if 1 < self.KcoordX < 19:
                    self.KcoordX -= 1
            if self.merre == 1:
                if 1 < self.KcoordY < 19:
                     self.KcoordY -= 1
            if self.merre == 2:
                if 1 < self.KcoordY < 19:
                    self.KcoordY += 1
            if self.merre == 3:
                if 1 < self.KcoordX < 19:
                    self.KcoordX += 1

            self.coords(self.kaja, self.KcoordX * kor - fele, self.KcoordY * kor - fele,
                        self.KcoordX * kor + fele,
                        self.KcoordY * kor + fele)
            self.kaja_elet -= 1
            self.KlepesSzam -= 1

    def cntrol_L(self):
        kor = self.oszto_szamolo()
        fele = kor / 2
        coord = [self.McoordX, self.McoordY]
        koord = [self.KcoordX,self.KcoordY]

        self.coords(self.pMan, self.McoordX * kor - fele, self.McoordY * kor - fele, self.McoordX * kor + fele,
                    self.McoordY * kor + fele)
        if coord == koord:
            self.W_pontszam += 1
            self.W_pontszamText.set(self.W_pontszam)
            self.kaja_restart()
        elif self.restart == 1:
            self.kaja_lepteto()
        else:
            self.kaja_lepteto()

    def start(self,event):
        self.uj_jatek()
        self.unbind('<Button-1>')
        self.unbind('<Button-3>')
        self.bind('<w>', self.fel)
        self.bind('<s>', self.le)
        self.bind('<a>', self.balra)
        self.bind('<d>', self.jobbra)
        coord = [13, 13]
        koord = [9, 9]
        self.KcoordX = koord[0]
        self.KcoordY = koord[1]
        self.kaja_elet = random.randint(13,20)
        self.McoordX = coord[0]
        self.McoordY = coord[1]
        self.KlepesSzam = random.randint(1, self.kaja_elet)
        self.merre = random.randint(0, 3)
        self.restart = 1
        self.pack_man()

    def pack_man(self):
        kor = self.oszto_szamolo()
        fele = kor/2
        self.pMan = self.create_oval(self.McoordX * kor - fele, self.McoordY * kor - fele, self.McoordX * kor + fele,
                                     self.McoordY * kor + fele, fill="white")
        self.kaja = self.create_oval(self.KcoordX * kor - fele, self.KcoordY * kor - fele, self.KcoordX * kor + fele,
                                     self.KcoordY * kor + fele, fill="black")

    def passz_vege(self):
        """itt írom ki hogy vége van a játéknak mert psszokltak a játékosok"""
        #értesiti a játékosokat hogy a játéknak vége
        messagebox.askokcancel(title="jaték vége", message="A játéknak vége mert mind két fél passzolt")
        self.unbind('<Button-1>')
        self.unbind('<Button-3>')
        self.bind('<Button-1>', self.fogolyEllenorzo)
        # meghívok egy függvényt ami ki értékeli a területekket
        import eredmeny1
        eredmeny = eredmeny1.eredmeny()
        eredmeny2 = eredmeny.indit(self.Coord_list, self.Szin_list)
        fekete_coord = eredmeny2[0]
        feher_coord = eredmeny2[1]
        # itt el ossztom a pintokat szinek szerint
        if fekete_coord != []:
            for fekete in fekete_coord:
                self.pontRako(fekete[0], fekete[1], "black")
                self.B_pontszam += 1
        if feher_coord != []:
            for feher in feher_coord:
                self.pontRako(feher[0], feher[1], "white")
                self.W_pontszam += 1
        self.nyertes_kiiro()
        ablak = Tk()
        ablak.title("Játék vége")
        ablak.geometry("220x100")
        frame = Frame(ablak)
        frame.grid()
        Label(frame, text="Kérem kattintson azokra a kővekre "\
                          +"\n" +"amik foglyok.").grid(row=0, column=0)
        Label(frame, text="Ha vissza szeretné tenni a követ(-eket)"+\
                        "\n" +"akkor kattintson rá mégegyszer").grid(row=1)
        gomb = Button(frame, text="Befejezés", command = ablak.destroy).grid(row=2)

    def fogolyEllenorzo(self, event):
        """ebben a fügvényben a játék végén amire katint azt fogolynak veszem"""
        coords = self.coord_csinalo(event.x, event.y)
        #print("ok")
        y = coords[0]
        x = coords[1]
        coord = [x, y]
        #print("coordlist:", self.Coord_list)
        if coord in self.Coord_list:
            #print("1")
            nemVizsgalt = []
            osszesTalaltbarat = []
            nemVizsgalt.append(coord)
            osszesTalaltbarat.append(coord)
            for i in range(len(self.Coord_list)):
                if coord == self.Coord_list[i]:
                    #print("2")
                    #print(osszesTalaltbarat)
                    szin = self.Szin_list[i]
            
            while nemVizsgalt != []:
                #print("3")
                #print(nemVizsgalt[0])
                a = nemVizsgalt[0]
                bealitott = self.Coord_bealitas(a)
                coord_list = bealitott[0]
                szin_list = bealitott[1]
                ertek = self.korbeNezo(coord_list,szin_list,osszesTalaltbarat, szin)
                if ertek != None:
                    #print("4")
                    for i in range(len(ertek)):
                        if ertek[i] not in osszesTalaltbarat:
                            nemVizsgalt.append(ertek[i])
                            osszesTalaltbarat.append(ertek[i])
                del(nemVizsgalt[0])
            # TODO ellenőrizni hogy helyesen néz e kőrbe (azaz nem talája megmégegyszer azt amit már megtalált)
            fogoly_nev = []
            sz_fogoly = []
            for talaltbarat in osszesTalaltbarat:
                for j, coord in enumerate(self.Coord_list):
                    if talaltbarat == coord:
                        sz_fogoly.append(talaltbarat)
                        if szin == "b":
                            jeloles = self.pontRako(talaltbarat[0],talaltbarat[1],"White",1)
                        elif szin == "w":
                            jeloles = self.pontRako(talaltbarat[0], talaltbarat[1], "black",1)
                        fogoly_nev.append(jeloles)
                        del(self.Coord_list[j])
                        del(self.Szin_list[j])

            self.sz_fogoly.append(sz_fogoly)
            self.sz_fogoly_szin.append(szin)
            self.sz_fogoly_nev.append(fogoly_nev)
            #print(self.sz_fogoly)
            #print(self.sz_fogoly_szin)
            if szin == "b":
                self.W_fogolyszam += len(osszesTalaltbarat)
                self.W_fogolyszam_Text.set(self.W_fogolyszam)
            elif szin == "w":
                self.B_fogolyszam += len(osszesTalaltbarat)
                self.B_fogolyszam_Text.set(self.B_fogolyszam)

        else:
            for i, fogoly in enumerate(self.sz_fogoly):
                if coord in self.sz_fogoly[i]:
                    #print("kk")
                    szinFogoly = self.sz_fogoly_szin[i]
                    for j in range(len(self.sz_fogoly[i])):
                        self.Coord_list.append(self.sz_fogoly[i][j])
                        self.Szin_list.append(szinFogoly)
                    if self.sz_fogoly_szin[i] == "b":
                        self.W_fogolyszam -= 1
                        self.W_fogolyszam_Text.set(self.W_fogolyszam)
                    else:
                        self.B_fogolyszam -= 1
                        self.B_fogolyszam_Text.set(self.B_fogolyszam)
                    #print(self.sz_fogoly[i])
                    del(self.sz_fogoly[i])
                    del(self.sz_fogoly_szin[i])
                    for k in range(len(self.sz_fogoly_nev[i])):
                        self.delete(self.sz_fogoly_nev[i][k])
                    del(self.sz_fogoly_nev[i])

        if self.pontok_nev != []:
            for pont in self.pontok_nev:
                self.delete(pont)
            self.pontok_nev.clear()

        self.B_pontszam = 0
        self.W_pontszam = 0
        import eredmeny1
        eredmeny = eredmeny1.eredmeny()
        eredmeny2 = eredmeny.indit(self.Coord_list, self.Szin_list)
        fekete_coord = eredmeny2[0]
        feher_coord = eredmeny2[1]
        if fekete_coord != []:
            for fekete in fekete_coord:
                self.pontRako(fekete[0], fekete[1], "black")
                self.B_pontszam += 1
        if feher_coord != []:
            for feher in feher_coord:
                self.pontRako(feher[0], feher[1], "white")
                self.W_pontszam += 1

        self.nyertes_kiiro()

    def nyertes_kiiro(self):
        self.B_pontszam += self.B_fogolyszam
        self.W_pontszam += self.W_fogolyszam
        self.B_pontszamText.set(self.B_pontszam)
        self.W_pontszamText.set(self.W_pontszam)

        if self.B_pontszam > self.W_pontszam:
            menyivel = str(self.B_pontszam-self.W_pontszam)
            szoveg = "Fekete Nyert! "
            pontszam = menyivel+ " Ponttal"
        elif self.W_pontszam > self.B_pontszam:
            menyivel = str(self.W_pontszam - self.B_pontszam)
            szoveg = "Fehér Nyert!"
            pontszam = menyivel+" Ponttal"
        else:
            szoveg="Döntettlen"
            pontszam = ""
        self.nyertesText.set(szoveg)
        self.nyertesSzamText.set(pontszam)

    def Coord_bealitas(self, coord):
        """itt  állitom be a koordinátákat nyolc írányba"""
        SzinCoord = []
        SCoordY = coord[0]  # itt állitom be a kezö jelenlegi coordinátákat
        SCoordX = coord[1]
        coord_list = [[SCoordY + 1, SCoordX],
                      [SCoordY, SCoordX + 1], [SCoordY - 1, SCoordX], [SCoordY, SCoordX - 1]]
        # itt töltöm ki a SzinCoordináta nevezetü lisámat a megfelelö szinekel a coordniátákhoz
        for coordI in coord_list:
            if coordI in self.Coord_list:
                for j, coordJ in enumerate(self.Coord_list):
                    if coordI == coordJ:
                        SzinCoord.append(self.Szin_list[j])

            else:  # idde akkor jutt be ha az adott koordinátához nem tartozik szin(fekete vagy fehér)és "n" jelölöm
                if coordI == 1 or coordI == 19:
                    SzinCoord.append("s")
                if coordI == 1 or coordI == 19:
                    SzinCoord.append("s")
                else:
                    SzinCoord.append("n")
        return coord_list, SzinCoord

    def korbeNezo(self, coord_list, szin_list, osszesTalaltbarat, szin):
        """ezt a fügvényt akkor használom amikor barát koveket keresek a zartkeresonek"""
        i = 0
        ertek = []
        while i < len(coord_list):
            if szin == szin_list[i] and coord_list[i] not in osszesTalaltbarat:
                ertek.append(coord_list[i])
            i += 1
        return ertek

    def pontozoRajzolo(self): # ez jelenleg nicsen használva
        frame = Frame()
        frame.grid()
        feketebox = LabelFrame(frame, text="Fekete")
        feketebox.grid(row=1, column=0, padx=5, pady=5)
        # itt a pontszámokat írom ki
        self.B_pontszamText1 = StringVar()
        Label(feketebox, text="pontszam:").grid(row=0, column=0, padx=5, pady=5)
        B_pontszam_L = Label(feketebox, textvariable=self.B_pontszamText1)
        B_pontszam_L.grid(row=0, column=1, padx=5, pady=5)
        self.B_fogolyszam_Text1 = StringVar()
        Label(feketebox, text="fogolyok:").grid(row=1, column=0, padx=5, pady=5)
        Label(feketebox, textvariable=self.B_fogolyszam_Text1).grid(row=1, column=1, padx=5, pady=5)

        # fehér box van
        feherbox = LabelFrame(self.frame, text="Fehér")
        feherbox.grid(row=1, column=1, padx=5, pady=5)
        # itt a pontszámokat írom ki
        self.W_pontszamText1 = StringVar()
        Label(feherbox, text="pontszam:").grid(row=0, column=0, padx=5, pady=5)
        Label(feherbox, textvariable=self.W_pontszamText1).grid(row=0, column=1, padx=5, pady=5)
        # itt a FEHÉR foglyok számát írom ki
        self.W_fogolyszam_Text1 = StringVar()
        Label(feherbox, text="fogolyok:").grid(row=1, column=0, padx=5, pady=5)
        Label(feherbox, textvariable=self.W_fogolyszam_Text1).grid(row=1, column=1)

        self.B_pontszam1 = 0
        self.B_fogolyszam1 = 123
        self.W_pontszam1 = 0
        self.W_fogolyszam1 = 0
        self.lepesekszam1 = 0

        self.B_pontszam1 += self.B_fogolyszam1
        self.B_pontszamText1.set(self.B_pontszam1)
        self.W_pontszam1 += self.W_fogolyszam1
        self.W_pontszamText1.set(self.W_pontszam1)

    def pontRako(self, y, x, szin, mi=None):
        """ebben a függvényben jelenitem meg a kis pontokat amiket kaptam"""
        pontok = self.create_oval(x*self.meret-(self.koMeret/4.28),y*self.meret-(self.koMeret/4.28),x*self.meret+(self.koMeret/4.28),y*self.meret+(self.koMeret/4.28),fill=szin)
        self.addtag_all("all")
        if mi == None:
            self.pontok_nev.append(pontok)
        else:
            return pontok

    def meretezo(self,event=None):
        #ebben a fugvénben meretezodik át a canvas a z ablak méretéhez
        old_magas = self.magas
        old_szelse = self.szeles
        self.szeles = self.master.winfo_width()
        self.magas = self.master.winfo_height()
        if self.szeles > self.magas:
            self.szeles = self.magas-15
            self.magas -= 15
        else:
            self.magas = self.szeles
        self.config(height=self.magas, width=self.szeles)
        self.scale("all", 0, 0, self.magas / float(old_magas), self.szeles / float(old_szelse))

    def gombok(self):
        """ebben a fügvénybe aállitom be a bilenytyüzet paracsait"""
            #self.bind('<Control_L>' + '<s>', self.ment)
            #self.bind('<Control_L>' + '<o>', self.tolt)
        self.bind('<Control_L>' + '<n>', self.uj_jatek)
        self.bind('<Button-1>', self.goKoLerak)
        self.bind('<Button-3>', self.Ko_torlo)
        self.bind('<Control_L>' + '<l>', self.start)
        self.focus_set()
