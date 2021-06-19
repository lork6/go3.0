from tkinter import *

def config_read():
    """ez a fügvény olvasa ki a config file bol a verzio számot"""
    #itt kell átirnom a verzio számot
    default = " 3.6.0"
    try:
        # megprobálom megkeresni a config filet és ha megva akkor ki olvasni a verzio számot
        data = open("config.txt", "r")
        if data != None:
            return data.read()
    except:
        # ha nem sikerül meg nyitnom a config filet akkor létre hozok egyet default beálitásal
        data = open("config.txt", "w")
        data.write(default)
        data.close()
        return default

# meg hivom a verzio szám olvasot
cim = config_read()
# létre hozom az ablakot root néven + beálitom a mértét
root = Tk()
root.geometry("850x615")
root.minsize(width=425,height=307)
root.title("Go"+cim)
# itt indul el a program
if __name__ in "__main__":
    import Go
    go = Go.Main(master=root)
    go.mainloop()

