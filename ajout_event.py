#Ce code permet d'ajouter un événement dans le calendrier


#importation des bibliothèques
from tkinter import Entry,Label,Tk,Button,ttk
from data import color_bg1,color_bg,color_fg

#création de la fenêtre 
fen = Tk()
fen.title("Ajout d'un evenement")
fen.config(background=color_bg1)

liste_time = ["temps plein","temps partiel matin", "temps partiel aprem"]

#création des Labels
label_Nom = Label(fen, text="Nom de l'événement", fg=color_fg, bg=color_bg1)
label_Description = Label(fen, text="Description de l'événement", fg=color_fg, bg=color_bg1)
label_couleur = Label(fen, text="Couleur d'affichage de l'évenemnt", fg=color_fg, bg=color_bg1)
label_date_deb = Label(fen, text="Date début inclus (format: AAAA-MM-DD)", fg=color_fg, bg=color_bg1)
label_date_fin = Label(fen, text="Date fin inclus (format: AAAA-MM-DD)", fg=color_fg, bg=color_bg1)
label_temps = Label(fen, text="Type de durée", fg=color_fg, bg=color_bg1)

#Définition des 5 entrées de la fenêtre (zones où il faut selectionner un parametre)
entry_Nom = Entry(fen)
entry_Description = Entry(fen)
entry_couleur = Entry(fen)
entry_date_deb = Entry(fen)
entry_date_fin = Entry(fen)


#Création d'une liste déroulante
listeTemps = ttk.Combobox(fen, values=liste_time)

#On place les label et les entrées sur la fenêtre
label_Nom.grid(row=0,column=0)
entry_Nom.grid(row=0,column=1)
label_Description.grid(row=1,column=0)
entry_Description.grid(row=1,column=1)
label_couleur.grid(row=2,column=0)
entry_couleur.grid(row=2,column=1)
label_date_deb.grid(row=3,column=0)
entry_date_deb.grid(row=3,column=1)
label_date_fin.grid(row=4,column=0)
entry_date_fin.grid(row=4,column=1)
label_temps.grid(row=5, column=0)
listeTemps.grid(row=5,column=1)


def ajout_evenement():
    '''fonction créant un nouvel evenement'''
    Nom = entry_Nom.get()
    Description = entry_Description.get()
    couleur = entry_couleur.get()
    date_deb = entry_date_deb.get()
    date_fin = entry_date_fin.get()
    time = listeTemps.get()
    with open("Planning","a") as file:
        file.write("\n{};{};{};{};{};{}".format(date_deb,date_fin,Nom,Description,couleur,time))
    Nom = entry_Nom.delete(0,len(Nom))
    Description = entry_Description.delete(0,len(Description))
    couleur = entry_couleur.delete(0,len(couleur))
    date_deb = entry_date_deb.delete(0,len(date_deb))
    date_fin = entry_date_fin.delete(0,len(date_fin))
    

#Création du bouton permettant de valider l'événement
Bouton_ajout = Button(fen, text="Ajout Evenement", fg=color_fg, bg=color_bg, command=ajout_evenement)
Bouton_ajout.grid(row=6,column=1)

fen.mainloop()
