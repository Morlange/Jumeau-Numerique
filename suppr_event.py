#Ce code permet d'ajouter un événement dans le calendrier


#importation des bibliothèques
from tkinter import Label,Tk,Button,ttk
from data import color_bg1,color_bg,color_fg

def main():
    #création de la fenêtre 
    
    fen = Tk()
    fen.title("Supression d'un evenement")
    fen.config(background=color_bg1)

    
    with open("Planning","r") as file:
        Data = file.read().split("\n")
        Data = [x.split(";") for x in Data]
        file.close()
    Noms_events,Descriptions_events = [x[2] for x in Data],[x[3] for x in Data]

    print(Noms_events,Descriptions_events)

    
    #création des Labels
    label_Nom = Label(fen, text="Nom de l'événement :", fg=color_fg, bg=color_bg1)
    label_Description = Label(fen, text="Description de l'événement :", fg=color_fg, bg=color_bg1)
    label_Description_event = Label(fen, text="", fg=color_fg, bg=color_bg1)


    #Création d'une liste déroulante
    listeNoms = ttk.Combobox(fen, values=Noms_events)

    #On place les label et les entrées sur la fenêtre
    label_Nom.grid(row=0,column=0)
    listeNoms.grid(row=0,column=1)
    label_Description.grid(row=1,column=0)
    label_Description_event.grid(row=1,column=1)    


    def suppr_evenement():
        '''fonction créant un nouvel evenement'''
        select = listeNoms.get()
        index_event_choisi = Noms_events.index(select)

        with open("Planning","w") as file:
            for i in range(len(Data)):
                if not i == index_event_choisi:
                    date_deb,date_fin,Nom,Description,couleur,time = Data[i]
                    if i == 0 or (index_event_choisi == 0 and i == 1):
                        file.write("{};{};{};{};{};{}".format(date_deb,date_fin,Nom,Description,couleur,time))
                    else:
                        file.write("\n{};{};{};{};{};{}".format(date_deb,date_fin,Nom,Description,couleur,time))
            file.close
        fen.destroy()
        main()
    
    def action(event):
        select = listeNoms.get()
        index_event_choisi = Noms_events.index(select)
        label_Description_event.configure(text=Descriptions_events[index_event_choisi])
    

        

    #Création du bouton permettant de valider l'événement
    Bouton_ajout = Button(fen, text="Supprimer Evenement", fg=color_fg, bg=color_bg, command=suppr_evenement)
    Bouton_ajout.grid(row=6,column=1)

    listeNoms.bind("<<ComboboxSelected>>", action)

    fen.mainloop()
    
if __name__ == "__main__":
    main()