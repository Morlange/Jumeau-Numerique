from tkinter import Entry,Label,Tk,Button

fen = Tk()
fen.title("Ajout d'un evenement")

label_Nom = Label(fen, text="Nom de l'événement")
label_Description = Label(fen, text="Description de l'événement")
label_couleur = Label(fen, text="Couleur d'affichage de l'évenemnt")
label_date_deb = Label(fen, text="Date début inclus (format: AAAA-MM-DD)")
label_date_fin = Label(fen, text="Date fin inclus (format: AAAA-MM-DD)")
label_temps = Label(fen, text="Type de durée")

entry_Nom = Entry(fen)
entry_Description = Entry(fen)
entry_couleur = Entry(fen)
entry_date_deb = Entry(fen)
entry_date_fin = Entry(fen)

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

with open("Planning","w") as file:
    file.write



fen.mainloop()
