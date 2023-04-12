from tkinter import Tk, Label, VERTICAL, N, S, ttk, END, LabelFrame, Button, Entry
import xlsxwriter
from data import LogoAM, nb_produits, liste_produit, OF, color_bg1, color_bg, color_fg


def main():
    ############### fenetre #######################

    # creation de l'objet fenetre
    fen_OF= Tk()

    #Titre de la fenetre
    fen_OF.title('Ordres de fabrication')

    #Taille de la fenetre
    fen_OF.geometry('1300x630')

    #icone de fenetre
    fen_OF.iconbitmap(LogoAM)

    #configuration du fond
    fen_OF.config(background=color_bg1)
    #Ajout d'un titre 
    label_titre = Label(fen_OF, text='Ordres de fabrication', height=1,font=('Calibri', 14),fg=color_fg, bg = color_bg1) 
    label_titre.grid(row=0,column=1, padx=0, pady=10)

    ################# menu déroulant et tableau ###############

    def action(event):
        # Obtenir l'élément sélectionné
        select = listeCombo.get()

        # Srollbar 
        scrollbar = ttk.Scrollbar( fen_OF, orient=VERTICAL)
        scrollbar.grid(row=2, column=3, sticky=N+S)
        
        #définir le tableau et joindre avec le mouvement de la scrollbar 
        tableau = ttk.Treeview(fen_OF,columns=('n° OF', 'nom OF', 'machine', 'début'),show='headings',yscrollcommand = scrollbar.set)
        scrollbar.config(command = tableau.yview )
        
        style = ttk.Style(fen_OF)
        style.theme_use("winnative")  # Charger un thème pour pouvoir accéder aux éléments de style
        style.configure("Treeview", background=color_bg1, foreground="white", fieldbackground=color_bg1)
        style.map("Treeview", background=[("selected", "#0066CC")], foreground=[("selected", "white")])

        #définir chaque colonne 
        tableau.heading ('n° OF', text='n° OF')
        tableau.heading ('nom OF', text='nom OF')
        tableau.heading ('machine', text='machine')
        tableau.heading ('début', text='début')

        #definition de chaque tableau en fonction des produits
        OFs=[]

        for i in range (nb_produits) :
            if str(select)==liste_produit[i] :
                caracteristique_produit=OF[i][5]
                for j in range (len(OF[i][1])):
                    OFs.append((OF[i][1][j], OF[i][2][j], OF[i][3][j], OF[i][4][j]))
        

                for valeur in OFs :
                        tableau.insert('', END, values=valeur)
                    
        #afficher 
        tableau['show'] = 'headings'
        tableau.grid(row=2, column=1, padx=10, pady=(0,10))

        
        #Frame Caractéristiques produits 
        frame_caracteristique = LabelFrame(fen_OF, text='Caractéristiques du produit', font =('Calibri', 12), fg=color_fg, bg = color_bg1, labelanchor='nw')
        frame_caracteristique.grid(row=7,column=1,padx=50, pady=10)
        Label(frame_caracteristique, text='Coût :',fg=color_fg, bg = color_bg1).grid(row=3, column=0, padx=10, pady=20)
        Label(frame_caracteristique, text='Résistance :',fg=color_fg, bg = color_bg1).grid(row=4, column=0, padx=10, pady=20)
        Label(frame_caracteristique, text='Temps de cycle moyen :',fg=color_fg, bg = color_bg1).grid(row=5, column=0, padx=10, pady=20)

        Label(frame_caracteristique, text=caracteristique_produit[0], fg=color_fg, bg = color_bg1).grid(row=3, column=2, padx=10, pady=20)
        Label(frame_caracteristique, text=caracteristique_produit[1], fg=color_fg, bg = color_bg1).grid(row=4, column=2, padx=10, pady=20)
        Label(frame_caracteristique, text=caracteristique_produit[2], fg=color_fg, bg = color_bg1).grid(row=5, column=2, padx=10, pady=20)

    def ouvrir_fen_nouveau_produit():

        def ajouter ():
            nom_prod=entree_nom_prod.get()
            temps_fab=entree_temps_fab.get()
            cout=entree_cout.get()
            print(cout, 'ok')
            resistance=entree_resistance.get()
            print(resistance)
            workbook  = xlsxwriter.Workbook('nouveau_OF4.xlsx')
            worksheet = workbook.add_worksheet('produit1')
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'Coût(€)')
            worksheet.write('B1', cout)
            worksheet.write('A2', 'Resistance (MPa)')
            worksheet.write('B2', resistance)
            worksheet.write('A3', 'Temps cycle moyen (min)')
            worksheet.write('B3', temps_fab)
            worksheet.write('A4', 'N°_OF')
            worksheet.write('B4', 'nom_OF')
            worksheet.write('C4', 'machine_OF')
            worksheet.write('D4', 'debut_OF')
            workbook.close()
        
        
        # creation de l'objet fenetre
        fen_nouveau_produit = Tk()

        #Titre de la fenetre
        fen_nouveau_produit.title('Ajouter un nouveau produit')

        #Taille de la fenetre
        fen_nouveau_produit.geometry('600x300')

        #icone de fenetre
        fen_nouveau_produit.iconbitmap(LogoAM)

        #configuration du fond
        fen_nouveau_produit.config(background=color_bg1)
        


        #Saisie nouveau produit

        frame_nouv = LabelFrame(fen_nouveau_produit, text='Nouveau produit', font =('Calibri', 12), fg=color_fg, bg = color_bg1, labelanchor='nw')
        frame_nouv.grid(row=1,column=0,padx=50, pady=10)

        Label(frame_nouv, text='Nom du produit :',fg=color_fg, bg = color_bg1).grid(row=3, column=0, padx=10, pady=20)
        entree_nom_prod= Entry(frame_nouv)
        entree_nom_prod.grid(row=3, column=1, padx=10, pady=20)
        
        
        Label(frame_nouv, text='Coût (€):',fg=color_fg, bg = color_bg1).grid(row=4, column=0, padx=10, pady=20)
        entree_cout = Entry(frame_nouv)
        entree_cout.grid(row=4, column=1, padx=10, pady=20)
        
        
        Label(frame_nouv, text='Résistance (MPa):',fg=color_fg, bg = color_bg1).grid(row=5, column=0, padx=10, pady=20)
        entree_resistance= Entry(frame_nouv)
        entree_resistance.grid(row=5, column=1, padx=10, pady=20)
        
        
        Label(frame_nouv, text='Temps moyen de fabrication :',fg=color_fg, bg = color_bg1).grid(row=6, column=0, padx=10, pady=20)
        entree_temps_fab= Entry(frame_nouv)
        entree_temps_fab.grid(row=6, column=1, padx=10, pady=20)
        
        
        
        bouton_ajouter = Button(fen_nouveau_produit, text = 'Ajouter le produit',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ajouter())
        bouton_ajouter.grid(row=1, column=2, padx=40, pady=100)

        




    # Ajout d'un produit
    bouton = Button(fen_OF, text = 'Ajouter un produit', bd=1, fg=color_fg, bg = color_bg,command=ouvrir_fen_nouveau_produit)
    bouton.grid(row=1, column=4, padx=0, pady=10)

    # Selectionner produit 
    label_choix = Label(fen_OF, text='Choisissez un produit:',fg=color_fg, bg = color_bg1)
    label_choix.grid(row=1, column=0, padx=0, pady=10)

    #Création de la Combobox
    listeCombo = ttk.Combobox(fen_OF, values=liste_produit)
        
    #Choisir l'élément qui s'affiche par défaut
    listeCombo.grid(row=1, column=1,padx=0,pady=10)

    listeCombo.bind("<<ComboboxSelected>>", action)   


    #Boucle d'affichage
    fen_OF.mainloop()

if __name__ == "__main__":
    main()