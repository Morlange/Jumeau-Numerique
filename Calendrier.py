from tkinter import Tk, Canvas
from datetime import datetime, timedelta, date

class Calendrier:
    def __init__(self, master = None, rows=5, cols=7, width=400, height=400, bg="white", fg="green", day = 0, month = 0,grid = (0,0)):
        if master == None:
            self.master = Tk()
            self.master.title("Calendrier")
        else:
            self.master = master
        self.rows = rows+2
        self.cols = cols
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg
        self.w = self.width // self.cols
        self.h = self.height // self.rows
        self.canvas = Canvas(self.master, width=self.width, height=self.height, bg=self.bg)
        self.canvas.grid(row=0,column=0)
        self.grid = []
        self.offset_day = -day
        self.offset_month = month            
        self.date_now = (datetime.now() - timedelta(days = self.offset_day)).strftime("%A/%d/%m/%Y")
        self.wday, self.day, self.month, self.years = self.date_now.split("/")
        if not self.offset_month == 0:
            self.date_now = (datetime.now() - timedelta(days = self.offset_day)- timedelta(days = -30*self.offset_month)).strftime("%A/%d/%m/%Y")
            self.wday, self.day, self.month, self.years = self.date_now.split("/")
        self.fdaymonthname, self.fdaymonth, self.month = (date(int(self.years),int(self.month),int(self.day)) - timedelta(days=int(self.day)-1)).strftime("%A/%d/%m").split("/")
        self.dict_wdays = {"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}
        self.dict_wmonth = {"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Août","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre"}
        self.number_fdaymonth = self.dict_wdays[self.fdaymonthname]
        self.cases_jours = [[None for j in range(self.cols)] for i in range(self.rows-2)]
        self.rect_day = [None for i in range(self.cols)]
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<ButtonRelease-1>", self.release_click)
        self.planned_event = lecture_planning("Planning")
        self.CreerGrille()
        
    def CreerGrille(self):
        self.rect_mois = self.canvas.create_rectangle(0,0,4*self.w,int(self.h*0.7), fill=self.bg)
        self.text_mois = self.canvas.create_text((4*self.w)//2,((self.h*0.7))//2,text=self.dict_wmonth[self.month], justify="center")
        self.start_grille = (0,-self.h*1.4)
        self.ajout_event = self.canvas.create_rectangle(self.w*4,0,self.w*5,self.h*0.7,fill=self.bg)
        self.label_ajout_event = self.canvas.create_text(int(self.w*4.5),int(self.h*0.7/2), text="+", justify="center")
        self.rect_mois_prec = self.canvas.create_rectangle(self.w*5,0,self.w*6,self.h*0.7,fill=self.bg)
        self.rect_mois_suiv = self.canvas.create_rectangle(self.w*6,0,self.w*7,self.h*0.7,fill=self.bg)
        self.label_mois_prec = self.canvas.create_text(int(self.w*5.5),int(self.h*0.7/2),fill=self.bg, text="<", justify="center")
        self.label_mois_suiv = self.canvas.create_text(int(self.w*6.5),int(self.h*0.7/2),fill=self.bg, text=">", justify="center")
        for j in range(self.rows):
            D = "LMMJVSD"
            self.rect_day = [self.canvas.create_rectangle(j*self.w,self.h*0.7,(j+1)*self.w,2*(self.h*0.7), fill=self.bg)]
            self.canvas.create_text(j*self.w + self.w//2,self.h * 0.7 + (self.h*0.7)//2,text = D[j], justify="center")
        for i in range(0,self.rows-2):
            row = []
            for j in range(self.cols):
                x1 = j * self.w - self.start_grille[0]
                y1 = i * self.h - self.start_grille[1]
                x2 = x1 + self.w
                y2 = y1 + self.h
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.bg)
                jour,mois,annee = (date(int(self.years),int(self.month),int(self.fdaymonth)) - timedelta(days=self.number_fdaymonth+1) + timedelta(days=self.cols*(i)+(j+1))).strftime("%d/%m/%Y").split('/')
                events = []
                for x in self.planned_event:
                    if date(int(annee),int(mois),int(jour)) >= x[0] and date(int(annee),int(mois),int(jour)) <= x[1]:
                        events.append(x)
                for k in range(len(events)):
                    self.canvas.create_rectangle(x1 ,y1 + int(k*self.h/len(events)),x2,y1 + int((k+1)*self.h/len(events)), fill=events[k][4])
                    #self.canvas.create_text(int((x1 +x2)/2),int(y1 + (2*k+1)*self.h/len(events)/2),text=events[k][2], justify="center")
                text_day = self.canvas.create_text(x1 + self.w//2,y1 + self.h//3,text = jour, justify="center")
                row.append((rect,text_day))
                self.cases_jours[i][j] = [rect,jour,mois,annee]
            self.grid.append(row)
        
        
    def handle_click(self, event):
        x = event.x
        y = event.y
        i = int((y+self.start_grille[1])//self.h)
        j = int((x+self.start_grille[0])//self.w)
        jour,mois,annee = self.cases_jours[i][j][1:]
        date_day = date(int(annee),int(mois),int(jour))
        if i < 0:
            if x <= 3*self.w and y <= self.h*0.7:
                for x in self.cases_jours:
                    for y in x:
                        if y[2] == self.month:
                            self.canvas.itemconfig(y[0],fill  = self.fg)
            elif x >= 5*self.w and x <= 6*self.w and y <= (self.h*0.7):
                self.mois_precedent()
            elif x >= 6*self.w and x <= 7*self.w and y <= self.h*0.7:
                self.mois_prochain()
            
            else:
                for k in range(self.rows-2):
                    if self.cases_jours[k][j][2] == self.month:
                        rect = self.cases_jours[k][j][0]
                        self.canvas.itemconfig(rect,fill  = self.fg)
        else:
            rect = self.cases_jours[i][j][0]
            self.canvas.itemconfig(rect,fill  = self.fg)
            self.ouvrir_jour((jour,mois,annee))
        
        #self.ouvrir_jour((jour,mois,annee))
        #self.mois_prochain()

    def release_click(self, event):
        for x in self.cases_jours:
            for y in x:
                self.canvas.itemconfig(y[0],fill  = self.bg)
    
    def ouvrir_jour(self, date):
        Jour(date[0], date[1], date[2])

    def mois_prochain(self):
        self.canvas.delete()
        NewMois = Calendrier(master = self.master,rows = self.rows-2,cols = self.cols,width = self.width,height = self.height,bg = self.bg,fg = self.fg,day = 0,month = self.offset_month+1)

    def mois_precedent(self):
        self.canvas.delete()
        NewMois = Calendrier(master = self.master,rows = self.rows-2,cols = self.cols,width = self.width,height = self.height,bg = self.bg,fg = self.fg,day = 0,month = self.offset_month-1)
        
    
    

class Jour:

    def __init__(self, day, month, year, width = 200, height = 350, bg = "white"):
        self.fen = Tk()
        self.width = width
        self.height = height
        self.w = self.width//8
        self.h = self.height//7
        self.day = day
        self.month = month
        self.year = year
        self.bg = bg
        self.date = date(int(self.year),int(self.month),int(self.day))
        self.canvas = Canvas(self.fen, width=self.width, height=self.height, bg=self.bg)
        self.wday = self.date.strftime("%A")
        self.canvas.pack()

        self.fen.title("{0}/{1}/{2}".format(self.day,self.month,self.year))
        self.events = lecture_planning_jour("Planning",self.date)
        self.CreerPLanningJour()


    def CreerPLanningJour(self):
        self.rect_vide = self.canvas.create_rectangle(0,0,2*self.w,2*self.h, fill= self.bg)
        self.rect_date = self.canvas.create_rectangle(2*self.w,0,10*self.w,2*self.h, fill= self.bg)
        self.dict_wdays = {"Monday":"Lundi","Tuesday":"Mardi","Wednesday":"Mercredi","Thursday":"Jeudi","Friday":"Vendredi","Saturday":"Samedi","Sunday":"Dimanche"}
        self.dict_wmonth = {"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Août","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre"}
        self.date_str = "{0} {1} \n {2} {3}".format(self.dict_wdays[self.wday],self.day,self.dict_wmonth[self.month],self.year)
        self.label_date = self.canvas.create_text(int(self.w*5),self.h,text = self.date_str, justify="center")
        self.rect_heures = [0 for i in range(5)]
        self.label_horaires = [0 for i in range(5)]
        self.rect_plan = [0 for i in range(5)]
        x1 = 2*self.w
        y1 = self.h
        for i in range(len(self.rect_heures)):
            self.rect_heures[i] = self.canvas.create_rectangle(0, (2+i)*self.h, 2*self.w, (3+i)*self.h, fill=self.bg)
            self.label_horaires[i] = self.canvas.create_text(self.w,int(((5+2*i)/2*self.h)), text = "{}h - {}h".format(8+i*2,10+i*2), justify="center")
            self.rect_plan[i] = self.canvas.create_rectangle(2*self.w, (2+i)*self.h, 8*self.w, (3+i)*self.h, fill=self.bg)
        for k in range(len(self.events)):
            if self.events[k][5] == "temps plein":
                for i in range(len(self.rect_heures)):
                    self.canvas.create_rectangle(x1+(k*6/len(self.events))*self.w,y1*(i+2),x1+((k+1)*6/len(self.events))*self.w,y1*(i+3), fill=self.events[k][4])
                    self.canvas.create_text(x1+((2*k+1)*6/len(self.events)/2)*self.w,y1*(i+2)+self.h/2,text=self.events[k][2])
            if self.events[k][5] == "temps partiel matin":
                for i in range(len(self.rect_heures[:2])):
                    self.canvas.create_rectangle(x1+(k*6/len(self.events))*self.w,y1*(i+2),x1+((k+1)*6/len(self.events))*self.w,y1*(i+3), fill=self.events[k][4])
                    self.canvas.create_text(x1+((2*k+1)*6/len(self.events)/2)*self.w,y1*(i+2)+self.h/2,text=self.events[k][2])
            if self.events[k][5] == "temps partiel aprem":
                for i in range(len(self.rect_heures[3:])):
                    self.canvas.create_rectangle(x1+(k*6/len(self.events))*self.w,y1*(i+5),x1+((k+1)*6/len(self.events))*self.w,y1*(i+6), fill=self.events[k][4])
                    self.canvas.create_text(x1+((2*k+1)*6/len(self.events)/2)*self.w,y1*(i+5)+self.h/2,text=self.events[k][2])
        self.canvas.create_rectangle(self.w*2,self.h*4,self.w*8,self.h*5, fill="gray")


def creer_date(String):
        L = String.split("-")
        L = [int(x) for x in L]
        return date(L[0],L[1],L[2])

def lecture_planning(name):
    planned_event = []
    with open(name,"r") as planned:
        Data = planned.read().split("\n")
        for ligne in Data:
            date_deb,date_fin,Nom,description,couleur,time = ligne.split(";")
            planned_event.append([creer_date(date_deb),creer_date(date_fin),Nom,description,couleur,time])
    planned.close()
    return planned_event

def lecture_planning_jour(name,date):
    planned_event = []
    with open(name,"r") as planned:
        Data = planned.read().split("\n")
        for ligne in Data:
            date_deb,date_fin,Nom,description,couleur,time = ligne.split(";")
            date_deb,date_fin = creer_date(date_deb),creer_date(date_fin)
            if date >= date_deb and date <= date_fin:
                planned_event.append([date_deb,date_fin,Nom,description,couleur,time])
    planned.close()
    return planned_event

# créer la fenêtre principale
root = Tk()
root.title("Grille 7x7 clickable")

# créer la grille
grille = Calendrier(master = root, rows=5, cols=7, width=400, height=350, day=0,month=1)
#grille = Calendrier(master = None, rows=5, cols=7, width=400, height=350, day=32-16)

# démarrer la boucle principale
root.mainloop()