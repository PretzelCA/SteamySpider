import threading
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import SteamySpider
import multilist
import webbrowser
import json
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

appVersion = "2018.10.30-1751"

class Application(Frame):
    def __init__(self,master=None):
        root = Tk()
        Frame.__init__(self,master)

        #gives program icon and title
        root.wm_title("Steamy Spider " + appVersion)

        #gui is divided into 3 parts, top middle and bottom
        topframe = Frame(root)
        midframe = Frame(root)
        botframe = Frame(root)

        #allows program to expand when you resize it
        Grid.columnconfigure(root,0,weight=1)
        Grid.rowconfigure(root,1,weight=1)
        Grid.columnconfigure(midframe,0,weight=1)
        Grid.rowconfigure(midframe,0,weight=1)

        #makes both the top and bottom set of buttons equal in spacing
        for i in range(5):
            topframe.columnconfigure(i, weight=1)
            botframe.columnconfigure(i, weight=1)

        #creates the graph used in the middle(called from multilist.py)
        self.graph = multilist.McListBox(midframe)
        self.graph.container.grid(row=0,column=0,sticky=N+S+E+W)

        
        self.SchemaUpdate = BooleanVar()
        self.reset = BooleanVar()
        self.genuine = BooleanVar()
        self.buds = BooleanVar()
        self.bills = BooleanVar()
        self.unusual = BooleanVar()
        self.stranges = BooleanVar()
        self.maxs = BooleanVar()
        self.bmoc = BooleanVar()
        self.salvage = BooleanVar()
        self.traded = BooleanVar()
        self.online = BooleanVar()        
        self.offline = BooleanVar()
        self.f2p = BooleanVar()
        self.untradable = BooleanVar()

        self.entryid = StringVar()
        self.apikey = StringVar()
        self.bpurl = StringVar()

        self.maxhours = IntVar()
        self.minhours = IntVar()
        self.minrecenthours=IntVar()
        self.maxrecenthours=IntVar()
        self.onlinedays = IntVar()
        self.thread=IntVar()

        self.clicked = False
        self.minhours.set(0)
        self.maxhours.set(500)
        self.minrecenthours.set(0)
        self.maxrecenthours.set(500)
        self.onlinedays.set(31)
        self.thread.set(25)
        self.bpurl.set("http://backpack.tf/profiles/")

        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.SchemaUpdate.set(config['SchemaUpdate']) 
                self.reset.set(config['reset']) 
                self.genuine.set(config['genuine'])
                self.buds.set(config['buds'])
                self.bills.set(config['bills'])
                self.unusual.set(config['unusual'])
                self.stranges.set(config['stranges']) 
                self.maxs.set(config['maxs'])
                self.bmoc.set(config['bmoc'])
                self.salvage.set(config['salvage']) 
                self.traded.set(config['traded']) 
                self.online.set(config['online'])
                self.offline.set(config['offline'])
                self.f2p.set(config['f2p'])
                self.untradable.set(config['untradable'])
                self.apikey.set(config['apikey'])
                self.maxhours.set(config['maxhours'])
                self.minhours.set(config['minhours'])
                self.minrecenthours.set(config['minrecenthours'])
                self.maxrecenthours.set(config['maxrecenthours'])
                self.onlinedays.set(config['onlinedays'])
                self.thread.set(config['thread'])
        except:
            pass

        self.box = Entry(topframe, textvariable=self.entryid, fg = "gray")
        self.box.bind("<Button-1>", self.callback)
        self.box.insert(0, "Enter steamid")
        self.box.grid(row=0, column=0, columnspan =3, pady = 5, padx = (5,0))

        self.b = Button(topframe, text="START", command=self.start)
        self.b.grid(row=1, column=0, padx = (5,2), pady = (0,5))
        self.cl = Button(topframe, text="CLEAR", command=self.clear).grid(row=1, column=1, padx = (0,2), pady = (0,5))
        self.he = Button(topframe, text="HELP", command=self.help).grid(row=1, column=2, pady = (0,5))

        Checkbutton(topframe, text = "Reload item schema", variable = self.SchemaUpdate).grid(row=0, column=4, sticky = W, padx = 5)
        Checkbutton(topframe, text = "Start with fresh id", variable = self.reset).grid(row=1, column=4, sticky = W, padx = 5)

        c = Button(topframe, text="Steam", command=self.steam).grid(row=0, column=5, padx = 5, pady = (5,0))
        d = Button(topframe, text="GotoBP", command=self.backpack).grid(row=0, column=6, pady = (5,0))
        option = OptionMenu(topframe, self.bpurl, "http://backpack.tf/profiles/", "www.tf2items.com/profiles/", "www.tf2b.com/tf2/")
        option.config(width = 22)
        option.grid(row=0, column=7, columnspan =2, padx = 5, pady = (5,0))
        
        Label(topframe, text="Threads:").grid(row=1, column=5, pady = 5)
        Entry(topframe,textvariable=self.thread,width=5).grid(row=1, column=6)

        e = Button(topframe, text="API key", command=self.api).grid(row=1, column=7, padx = 5, pady = (0,5), sticky = W)

        self.lbl = Label(topframe, text="0/0 found")
        self.lbl.grid(row=1, column=8, padx = (0,25)) 

        Label(botframe, text="Worked on by PretzelCA | Originally created by Akenne | Version: "+appVersion, font=("Times New Roman", 8)).grid(row=3, column=0, sticky = W)

        Label(botframe, text="Total Hours:").grid(row = 0, column = 4, sticky = W)
        Entry(botframe,textvariable=self.minhours, width = 4).grid(row = 0, column = 5, sticky = E)
        Label(botframe, text=" to ").grid(row = 0, column = 6)
        Entry(botframe,textvariable=self.maxhours, width = 4).grid(row = 0, column = 7, padx = (0,10), sticky = W)

        Label(botframe, text = "Recent Hours:").grid(row = 1, column = 4, sticky = W)
        Entry(botframe, textvariable = self.minrecenthours, width = 4).grid(row=1, column=5, sticky = E)
        Label(botframe, text=" to ").grid(row = 1, column = 6)
        Entry(botframe, textvariable = self.maxrecenthours, width = 4).grid(row=1, column=7, padx = (0,10))

        Checkbutton(botframe, text = "Hide traded", variable = self.traded).grid(row=0, column=3, sticky = W)
        Checkbutton(botframe, text = "Hide f2p", variable = self.f2p).grid(row=1, column=3, sticky = W)
        Checkbutton(botframe, text = "Hide untradable", variable = self.untradable).grid(row=2, column=3, sticky = W)
        Checkbutton(botframe, text = "Hide offline", variable = self.offline).grid(row=3, column=3, sticky = W)

        Checkbutton(botframe, text = "Last online (days):", variable = self.online).grid(row=2, column=4, sticky = W)
        Entry(botframe, textvariable = self.onlinedays, width = 4).grid(row=2, column=5, sticky = E)

        Checkbutton(botframe, text = "Earbuds", variable = self.buds).grid(row=0, column=0, sticky = W)
        Checkbutton(botframe, text = "Bill's", variable = self.bills).grid(row=1, column=0, sticky = W)
        Checkbutton(botframe, text = "Max's items", variable = self.maxs).grid(row=2, column=0, sticky = W)

        Checkbutton(botframe, text = "Genuines", variable = self.genuine).grid(row=0, column=2, sticky = W)
        Checkbutton(botframe, text = "Unusuals", variable = self.unusual).grid(row=1, column=2, sticky = W)
        Checkbutton(botframe, text = "Stranges", variable = self.stranges).grid(row=2, column=2, sticky = W)

        Checkbutton(botframe, text = "BMOCs", variable = self.bmoc).grid(row=0, column=1, sticky = W)
        Checkbutton(botframe, text = "Salvaged", variable = self.salvage).grid(row=1, column=1, sticky = W)

        if len(str(self.apikey.get())) < 4:
            self.api()

        topframe.grid(row =0, column = 0, sticky=E+W)
        midframe.grid(row =1, column = 0, sticky=N+S+E+W)
        botframe.grid(row =2, column = 0, sticky=E+W)

        self.graph.tree.bind("<Double-1>", self.OnDoubleClick)

        def handler():
            self.config = {'SchemaUpdate': self.SchemaUpdate.get(), 'reset': self.reset.get(), 'genuine': self.genuine.get(), 'buds': self.buds.get(), 'bills': self.bills.get(), 'unusual': self.unusual.get()
            , 'stranges': self.stranges.get(), 'maxs': self.maxs.get(), 'bmoc': self.bmoc.get(), 'salvage': self.salvage.get(), 'online': self.online.get(), 'offline': self.offline.get(), 'traded': self.traded.get(), 'f2p': self.f2p.get(), 'untradable': self.untradable.get()
            , 'apikey': self.apikey.get(), 'maxhours': self.maxhours.get(), 'minhours': self.minhours.get(),  'minrecenthours': self.minrecenthours.get(), 'onlinedays': self.onlinedays.get(), 'maxrecenthours': self.maxrecenthours.get(), 'thread':self.thread.get()}     
            with open('config.json', 'w') as f:
                json.dump(self.config, f)
            root.quit()

        root.protocol("WM_DELETE_WINDOW", handler)

        root.mainloop()

    def OnDoubleClick(self, event):
        try:
            webbrowser.get("windows-default").open("https://steamidfinder.com/lookup/" + str(self.graph.tree.item(self.graph.tree.selection())["values"][0]))
        except:
            self.popup_error("You must select a found user first")

    def updateGUI(self):
        fcount = str(SteamySpider.fcount)
        count = str(SteamySpider.count)
        msg = fcount + "/" + count + " found"
        self.lbl["text"] = msg

    def start(self):
        t1 = threading.Thread(target = self.threads)
        t1.daemon = True
        t1.start()
        SteamySpider.run = True
        self.b.configure(text = "STOP", command=self.stop)

    def stop(self):
        SteamySpider.run = False
        self.b.configure(text = "START", command=self.start)

    def threads(self):
        if self.entryid.get() == "Enter steamid":
            self.box.delete(0, END)
            self.box.config(fg = "black")
            self.clicked = True
        SteamySpider.API = self.apikey.get()
        SteamySpider.start(self.SchemaUpdate.get(), self.reset.get(), self.entryid.get())
        SteamySpider.go(self.thread.get(), self, self.genuine.get(), self.buds.get(), self.bills.get(), self.unusual.get(), 
            self.maxs.get(), self.bmoc.get(), self.salvage.get(), self.maxhours.get(), self.traded.get(), self.f2p.get(), 
            self.untradable.get(), self.minrecenthours.get(), self.minhours.get(), self.maxrecenthours.get(), 
            self.online.get(), self.onlinedays.get(), self.offline.get())

    def callback(self, event):
        if (self.clicked == False):
            self.box.delete(0, END)
            self.box.config(fg = "black")
            self.clicked = True

    def steam(self): 
        try:
            webbrowser.get("windows-default").open("https://steamidfinder.com/lookup/" + str(self.graph.tree.item(self.graph.tree.selection())["values"][0]))
        except:
            self.popup_error("You must select a found user first")

    def backpack(self): 
        try:
            webbrowser.get("windows-default").open(self.bpurl.get() + str(self.graph.tree.item(self.graph.tree.selection())["values"][0]))
        except:
            self.popup_error("You must select a found user first")

    def clear(self):
        for i in self.graph.tree.get_children():
            self.graph.tree.delete(i)

    def popup_error(self, error):
        top = Toplevel()
        top.title("Error")
        msg = Label(top, text=error)
        msg.pack()
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()

    def popup_warn(self, warn):
        top = Toplevel()
        top.title("Error")
        msg = Label(top, text=warn)
        msg.pack()
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()

    def help(self):
        def show_hand_cursor(event):
            event.widget.configure(cursor="center_ptr")

        def show_arrow_cursor(event):
            event.widget.configure(cursor="")

        def click(event):
            webbrowser.get("windows-default").open("www.steamcommunity.com/dev/apikey")

        top = Toplevel()
        top.title("Help")
        T = Text(top, height=20, width=100)
        T.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        T.tag_configure('big', font=('Verdana', 20, 'bold'))
        T.insert(END,'How to use\n', 'big')
        T.insert(END, "Start off by getting your API key, it can be found here\n")
        T.tag_config("a", foreground="blue", underline=1)
        T.tag_bind("a", "<Enter>", show_hand_cursor)
        T.tag_bind("a", "<Leave>", show_arrow_cursor)
        T.tag_bind("a", "<Button-1>", click)
        T.config(cursor="arrow")
        T.insert(END, "link\n", "a")
        T.insert(END, "Input when program starts, or click the API key button\nEnter a steam id(after http://steamcommunity.com/id/ or http://steamcommunity.com/profiles/)\nPush start\n")
        T.insert(END, "After you get an ID, use https://steamidfinder.com/ or another site to get a working link to see their profile.\n")
        T.insert(END, "Settings\n", 'big')
        T.insert(END, "Clear - clears the log of found users\nReload item schema - forces item schema to update (do it if tf2 adds new items)\n")
        T.insert(END, "Start with fresh id - if unchecked, program will attempt to use saved data, \n                        otherwise it will start fresh with the id in the entry box\n")
        T.insert(END, "Threads - the amount of users being checked at the same time (depends on computer speed)\n")
        T.insert(END, "Steam - highlight a found user and click to open their steam profile\n")
        T.insert(END, "GotoBP - highlight a found user and click to open their backpack\n\n\n")
        T.insert(END, "Special thanks to Akenne who orginally made this program 4 years\n")
        T.pack()

    def api(self):
        def link():
            webbrowser.get("windows-default").open("www.steamcommunity.com/dev/apikey")

        top = Toplevel()
        top.title("Enter Steam API key")
        entry = Entry(top, textvariable=self.apikey,width=36)
        entry.grid(row=0, column=0, columnspan =2, padx = 15, pady = 5)
        save = Button(top, text="Save", command=top.destroy)
        help = Button(top, text="Help", command=link)
        save.grid(row=1, column=0, sticky = E, padx = (0,5))
        help.grid(row=1, column=1, sticky = W, padx = (5,0))