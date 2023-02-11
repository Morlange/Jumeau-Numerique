# coding: utf-8

# import bibliothèque
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import xlrd
import xlsxwriter
import subprocess
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle
import time
from opcua import Client

#données pour analyse 
TRS=[23,54,78]
Temps_de_production=[46,6,23]
Nombre_pieces=[12,10,7]
LogoAM = "Logo_AM.png"
Serveur_ON = False
url = "opc.tcp://127.0.0.1:4880"
client = Client(url)

#données OF

document = xlrd.open_workbook('OF.xls')
nb_feuilles = document.nsheets
OF=[]

for i in range (0,nb_feuilles) :
    feuille = document.sheet_by_index(i)
    nom_produit = feuille.name
    nb_colonnes = feuille.ncols
    nb_lignes = feuille.nrows
    n_OF=[]
    nom_OF=[]
    machine_OF=[]
    debut_OF=[]
    caracteristique=[feuille.cell_value(rowx=0,colx=1),feuille.cell_value(rowx=1,colx=1),feuille.cell_value(rowx=2,colx=1) ]
    for i in range (4,nb_lignes):
        n_OF.append(feuille.cell_value(rowx=i, colx=0))
        nom_OF.append(feuille.cell_value(rowx=i, colx=1))
        machine_OF.append(feuille.cell_value(rowx=i, colx=2))
        debut_OF.append(feuille.cell_value(rowx=i, colx=3))
    OF_produit=[nom_produit, n_OF, nom_OF, machine_OF, debut_OF,caracteristique]
    OF.append(OF_produit)
    OF_produit=[]
    
#forme des odres de fabrication : OF=[[nom_produit, n_OF, nom_OF, machine_OF, debut_OF,caracteristique], [nom_produit, n_OF, nom_OF, machine_OF, debut_OF,caracteristique], ...]

nb_produits = len(OF)
liste_produit =[]
for i in range (nb_produits):
    liste_produit.append(OF[i][0])

def ouvrir_analyse ():
    global TRS
    # creation de l'objet fenetre
    fen_analyse= Tk()

    #Titre de la fenetre
    fen_analyse.title('Analyse de production')

    #Taille de la fenetre
    fen_analyse.geometry('1300x630')

    #icone de fenetre
    fen_analyse.iconbitmap(LogoAM)

    #configuration du fond
    fen_analyse.config(background='#333333')
    #Ajout d'un titre 
    label_titre = Label(fen_analyse, text='Analyse de production', height=1,font=('Calibri', 14),fg='#dcdcaa', bg = '#333333') 
    label_titre.grid(row=0,column=0, padx=500, pady=10)

    #Frame TRS
    frame_TRS = tkinter.LabelFrame(fen_analyse, text='TRS', font =('Calibri', 12), fg='#dcdcaa', bg = '#333333', labelanchor='nw')
    frame_TRS.grid(row=1,column=0,padx=50, pady=10)
    Label(frame_TRS, text='Fonderie',fg='#dcdcaa', bg = '#333333').grid(row=1, column=0, padx=10, pady=20)
    Label(frame_TRS, text='Usinage',fg='#dcdcaa', bg = '#333333').grid(row=1, column=1, padx=10, pady=20)
    Label(frame_TRS, text='Assemblage',fg='#dcdcaa', bg = '#333333').grid(row=1, column=2, padx=10, pady=20)

    Label(frame_TRS, text=TRS[0], fg='#dcdcaa', bg = '#333333').grid(row=2, column=0, padx=10, pady=20)
    Label(frame_TRS, text=TRS[1], fg='#dcdcaa', bg = '#333333').grid(row=2, column=1, padx=10, pady=20)
    Label(frame_TRS, text=TRS[2], fg='#dcdcaa', bg = '#333333').grid(row=2, column=2, padx=10, pady=20)

    #Affichage des graphes des TRS

    TRSgraph=[]

    for TRSzone in TRS :
        a=TRSzone%10
        if a==1 or a==2 or a==3 : 
            TRSzone=int((TRSzone/10)%10)*10
        elif a==4 or a==5 :
            TRSzone=int((TRSzone/10)%10)*10+5
        elif a==6 or a==7 or a==8 : 
            TRSzone=int((TRSzone/10)%10)*10+5
        elif a==9 : 
            TRSzone=int((TRSzone/10)%10)*10+10
        
        TRSlist=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
        TRSgraph.append(TRSlist.index(TRSzone)+1)  

    def degree_range(n): 
        start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
        end = np.linspace(0,180,n+1, endpoint=True)[1::]
        mid_points = start + ((end-start)/2.)
        return np.c_[start, end], mid_points


    def rot_text(ang): 
        rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
        return rotation

    def gauge(labels=['LOW','MEDIUM','HIGH','VERY HIGH','EXTREME'], \
            colors='jet_r', arrow=1, title='', fname=False): 
        
        """
        some sanity checks first
        
        """
        
        N = len(labels)
        
        if arrow > N: 
            raise Exception("\n\nThe category ({}) is greated than \
            the length\nof the labels ({})".format(arrow, N))
    
        
        """
        if colors is a string, we assume it's a matplotlib colormap
        and we discretize in N discrete colors 
        """
        
        if isinstance(colors, str):
            cmap = cm.get_cmap(colors, N)
            cmap = cmap(np.arange(N))
            colors = cmap[::-1,:].tolist()
        if isinstance(colors, list): 
            if len(colors) == N:
                colors = colors[::-1]
            else: 
                raise Exception("\n\nnumber of colors {} not equal \
                to number of categories{}\n".format(len(colors), N))

        """
        begins the plotting
        """
        
        fig, ax = plt.subplots()

        ang_range, mid_points = degree_range(N)

        labels = labels[::-1]
        
        """
        plots the sectors and the arcs
        """
        patches = []
        for ang, c in zip(ang_range, colors): 
            # sectors
            patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
            # arcs
            patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))
        
        [ax.add_patch(p) for p in patches]

        
        """
        set the labels (e.g. 'LOW','MEDIUM',...)
        """

        for mid, lab in zip(mid_points, labels): 

            ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
                horizontalalignment='center', verticalalignment='center', fontsize=14, \
                fontweight='bold', rotation = rot_text(mid))

        """
        set the bottom banner and the title
        """
        r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
        ax.add_patch(r)
        
        ax.text(0, -0.05, title, horizontalalignment='center', \
            verticalalignment='center', fontsize=22, fontweight='bold')

        """
        plots the arrow now
        """
        
        pos = mid_points[abs(arrow - N)]
        
        ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                    width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
        
        ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
        ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

        """
        removes frame and ticks, and makes axis equal and tight
        """
        
        ax.set_frame_on(False)
        ax.axes.set_xticks([])
        ax.axes.set_yticks([])
        ax.axis('equal')
        plt.tight_layout()
        if fname:
            fig.savefig(fname, dpi=200)


    fonderie=gauge(labels=['0',' ','10',' ','20',' ','30',' ','40',' ','50',' ','60',' ','70',' ','80',' ','90',' ','100'], \
        colors=['#ED1C24','#ED1C24','#ED1C24','#ED1C24','#ED1C24','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00',
                '#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#007A00','#007A00','#007A00','#007A00',
                '#007A00'], arrow=TRSgraph[0], title='TRS fonderie')
    plt.savefig('TRS_fonderie.png', transparent = True) 
    im_fonderie=PhotoImage(file='TRS_fonderie.png')

    usinage=gauge(labels=['0',' ','10',' ','20',' ','30',' ','40',' ','50',' ','60',' ','70',' ','80',' ','90',' ','100'], \
        colors=['#ED1C24','#ED1C24','#ED1C24','#ED1C24','#ED1C24','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00',
                '#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#007A00','#007A00','#007A00','#007A00',
                '#007A00'], arrow=TRSgraph[1], title='TRS usinage')
    plt.savefig('TRS_usinage.png', transparent = True) 
    im_usinage=PhotoImage(file='TRS_usinage.png')


    assemblage=gauge(labels=['0',' ','10',' ','20',' ','30',' ','40',' ','50',' ','60',' ','70',' ','80',' ','90',' ','100'], \
        colors=['#ED1C24','#ED1C24','#ED1C24','#ED1C24','#ED1C24','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00',
                '#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#007A00','#007A00','#007A00','#007A00',
                '#007A00'], arrow=TRSgraph[2], title='TRS assemblage')
    plt.savefig('TRS_assemblage.png', transparent = True) 
    im_assemblage=PhotoImage(file='TRS_assemblage.png')

    im_fonderie.grid(row=7,column=4,padx=50, pady=10)
    im_usinage.grid(row=8,column=4,padx=50, pady=10)
    im_assemblage.grid(row=9,column=4,padx=50, pady=10)
    
    #Frame Temps de production
    frame_temps_de_production = tkinter.LabelFrame(fen_analyse, text='Temps de production', font =('Calibri', 12), fg='#dcdcaa', bg = '#333333', labelanchor='nw')
    frame_temps_de_production.grid(row=4,column=0,padx=50, pady=10)
    Label(frame_temps_de_production, text='Fonderie', fg='#dcdcaa', bg = '#333333').grid(row=4, column=0, padx=10, pady=20)
    Label(frame_temps_de_production, text='Usinage', fg='#dcdcaa', bg = '#333333').grid(row=4, column=1, padx=10, pady=20)
    Label(frame_temps_de_production, text='Assemblage', fg='#dcdcaa', bg = '#333333').grid(row=4, column=2, padx=10, pady=20)

    Label(frame_temps_de_production, text=Temps_de_production[0], fg='#dcdcaa', bg = '#333333').grid(row=5, column=0, padx=10, pady=20)
    Label(frame_temps_de_production, text=Temps_de_production[1], fg='#dcdcaa', bg = '#333333').grid(row=5, column=1, padx=10, pady=20)
    Label(frame_temps_de_production, text=Temps_de_production[2], fg='#dcdcaa', bg = '#333333').grid(row=5, column=2, padx=10, pady=20)

    #Frame nombre de pièces 
    frame_nb_pieces = tkinter.LabelFrame(fen_analyse, text='Nombre de pièces produites', font =('Calibri', 12), fg='#dcdcaa', bg = '#333333', labelanchor='nw')
    frame_nb_pieces.grid(row=7,column=0,padx=50, pady=10)
    Label(frame_nb_pieces, text='Fonderie', fg='#dcdcaa', bg = '#333333').grid(row=7, column=0, padx=10, pady=20)
    Label(frame_nb_pieces, text='Usinage', fg='#dcdcaa', bg = '#333333').grid(row=7, column=1, padx=10, pady=20)
    Label(frame_nb_pieces, text='Assemblage', fg='#dcdcaa', bg = '#333333').grid(row=7, column=2, padx=10, pady=20)

    Label(frame_nb_pieces, text=Nombre_pieces[0], fg='#dcdcaa', bg = '#333333').grid(row=8, column=0, padx=10, pady=20)
    Label(frame_nb_pieces, text=Nombre_pieces[1], fg='#dcdcaa', bg = '#333333').grid(row=8, column=1, padx=10, pady=20)
    Label(frame_nb_pieces, text=Nombre_pieces[2], fg='#dcdcaa', bg = '#333333').grid(row=8, column=2, padx=10, pady=20)

    #Boucle d'affichage
    fen.mainloop()

def ouvrir_OF ():
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
    fen_OF.config(background='#333333')
    #Ajout d'un titre 
    label_titre = Label(fen_OF, text='Ordres de fabrication', height=1,font=('Calibri', 14),fg='#dcdcaa', bg = '#333333') 
    label_titre.grid(row=0,column=1, padx=0, pady=10)

    ################# menu déroulant et tableau ###############

    def action(event):
        # Obtenir l'élément sélectionné
        select = listeCombo.get()

        # Srollbar 
        scrollbar = ttk.Scrollbar( fen_OF, orient=VERTICAL)
        scrollbar.grid(row=2, column=3, sticky=N+S)
        
        #définir le tableau et joindre avec le mouvement de la scrollbar 
        tableau = ttk.Treeview(fen_OF, fg='#dcdcaa', bg = '#333333',columns=('n° OF', 'nom OF', 'machine', 'début'),show='headings',yscrollcommand = scrollbar.set)
        scrollbar.config(command = tableau.yview )
        
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
                     tableau.insert('', tkinter.END, values=valeur)
                 
        #afficher 
        tableau['show'] = 'headings'
        tableau.grid(row=2, column=1, padx=10, pady=(0,10))

        
        #Frame Caractéristiques produits 
        frame_caracteristique = tkinter.LabelFrame(fen_OF, text='Caractéristiques du produit', font =('Calibri', 12), fg='#dcdcaa', bg = '#1e1e1e', labelanchor='nw')
        frame_caracteristique.grid(row=7,column=1,padx=50, pady=10)
        Label(frame_caracteristique, text='Coût :',fg='#dcdcaa', bg = '#333333').grid(row=3, column=0, padx=10, pady=20)
        Label(frame_caracteristique, text='Résistance :',fg='#dcdcaa', bg = '#333333').grid(row=4, column=0, padx=10, pady=20)
        Label(frame_caracteristique, text='Temps de cycle moyen :',fg='#dcdcaa', bg = '#333333').grid(row=5, column=0, padx=10, pady=20)

        Label(frame_caracteristique, text=caracteristique_produit[0], fg='#dcdcaa', bg = '#333333').grid(row=3, column=2, padx=10, pady=20)
        Label(frame_caracteristique, text=caracteristique_produit[1], fg='#dcdcaa', bg = '#333333').grid(row=4, column=2, padx=10, pady=20)
        Label(frame_caracteristique, text=caracteristique_produit[2], fg='#dcdcaa', bg = '#333333').grid(row=5, column=2, padx=10, pady=20)

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
        fen_nouveau_produit.config(background='#333333')
        


        #Saisie nouveau produit

        frame_nouv = tkinter.LabelFrame(fen_nouveau_produit, text='Nouveau produit', font =('Calibri', 12), fg='#dcdcaa', bg = '#333333', labelanchor='nw')
        frame_nouv.grid(row=1,column=0,padx=50, pady=10)
    
        Label(frame_nouv, text='Nom du produit :',fg='#dcdcaa', bg = '#333333').grid(row=3, column=0, padx=10, pady=20)
        entree_nom_prod= Entry(frame_nouv)
        entree_nom_prod.grid(row=3, column=1, padx=10, pady=20)
        
        
        Label(frame_nouv, text='Coût (€):',fg='#dcdcaa', bg = '#333333').grid(row=4, column=0, padx=10, pady=20)
        entree_cout = Entry(frame_nouv)
        entree_cout.grid(row=4, column=1, padx=10, pady=20)
        
        
        Label(frame_nouv, text='Résistance (MPa):',fg='#dcdcaa', bg = '#333333').grid(row=5, column=0, padx=10, pady=20)
        entree_resistance= tkinter.Entry(frame_nouv)
        entree_resistance.grid(row=5, column=1, padx=10, pady=20)
        
        
        Label(frame_nouv, text='Temps moyen de fabrication :',fg='#dcdcaa', bg = '#333333').grid(row=6, column=0, padx=10, pady=20)
        entree_temps_fab= Entry(frame_nouv)
        entree_temps_fab.grid(row=6, column=1, padx=10, pady=20)
        
        
        
        bouton_ajouter = tkinter.Button (fen_nouveau_produit, text = 'Ajouter le produit',bd=1,font=('Calibri', 12), fg='#dcdcaa', bg = '#1e1e1e',command=ajouter())
        bouton_ajouter.grid(row=1, column=2, padx=40, pady=100)

        

    
    

    # Ajout d'un produit
    bouton = tkinter.Button (fen_OF, text = 'Ajouter un produit', bd=1, fg='#dcdcaa', bg = '#1e1e1e',command=ouvrir_fen_nouveau_produit)
    bouton.grid(row=1, column=4, padx=0, pady=10)
    
    # Selectionner produit 
    label_choix = Label(fen_OF, text='Choisissez un produit:',fg='#dcdcaa', bg = '#333333')
    label_choix.grid(row=1, column=0, padx=0, pady=10)
    
    #Création de la Combobox
    listeCombo = ttk.Combobox(fen_OF, values=liste_produit)
     
    #Choisir l'élément qui s'affiche par défaut
    listeCombo.grid(row=1, column=1,padx=0,pady=10)

    listeCombo.bind("<<ComboboxSelected>>", action)   
    

    #Boucle d'affichage
    fen.mainloop()


def ouvrir_etat ():
    
    if Serveur_ON:
        subprocess.Popen("python3 Interface_machines.py")
    else :
        # creation de l'objet fenetre
        fen_Error_co= Tk()

        #Titre de la fenetre
        fen_Error_co.title('Erreur de connection')

        #Taille de la fenetre
        fen_Error_co.geometry('300x200')

        #icone de fenetre
        fen_Error_co.iconbitmap(LogoAM)

        #configuration du fond
        fen_Error_co.config(background='#333333')
        #Ajout d'un titre 
        label_titre = Label(fen_Error_co, text='Erreur de connection \nVeuillez lancer le serveur en premier', height=2,font=('Calibri', 14),fg='#dcdcaa', bg = '#333333') 
        label_titre.grid(row=0,column=0, padx=10, pady=75)

        fen_Error_co.mainloop()

def lancer_serveur():

    global Serveur_ON
    if not Serveur_ON:
        subprocess.Popen("python3 Serveur.py")
        time.sleep(2)
        client.connect()
        print("Interface connectée")
        Serveur_ON = True
        label_etat_serv.configure(text="Etat du serveur : Connecté")
        fen.update()

def stop_serveur():
#On restart le programme pour espérer arrêter le serveur
    global Serveur_ON
    if Serveur_ON :
        Stop = client.get_node("ns = 2; i = 16")
        Stop.set_value(1)
        client.disconnect()
        Serveur_ON = False
        label_etat_serv.configure(text="Etat du serveur : Déconnecté")
        fen.update()

def quitter():
    if Serveur_ON :
        stop_serveur()
    fen.destroy()
    
    
#Creation de l'objet fenetre
fen= Tk()

#Titre de la fenetre
fen.title('Gestion de production')

#Taille de la fenetre
fen.geometry('1300x630')

#icone de fenetre
fen.iconbitmap(LogoAM)

#configuration du fond
fen.config(background='#333333')

#Menu
mon_menu=Menu(fen)
fen.config(menu=mon_menu)

#Les 4 principaux onglets
mon_menu.add_command(label='Etat',command=ouvrir_etat)
mon_menu.add_command(label='OF',command=ouvrir_OF)
mon_menu.add_command(label='Analyse',command=ouvrir_analyse)

# boutons fenetre
bouton_etat = tkinter.Button (fen, text = 'Etat des machines',bd=1, font=('Calibri', 12),fg='#dcdcaa', bg = '#1e1e1e',command=ouvrir_etat)
bouton_etat.grid(row=1, column=0, padx=40, pady=100)

bouton_OF = tkinter.Button (fen, text = 'Ordres de fabrication',bd=1,font=('Calibri', 12), fg='#dcdcaa', bg = '#1e1e1e',command=ouvrir_OF)
bouton_OF.grid(row=1, column=1, padx=40, pady=100)

bouton_analyse = tkinter.Button (fen, text = 'Analyse de production',bd=1,font=('Calibri', 12), fg='#dcdcaa', bg = '#1e1e1e',command=ouvrir_analyse)
bouton_analyse.grid(row=1, column=2, padx=40, pady=100)

bouton_start_server = tkinter.Button (fen, text = 'Lancer le serveur',bd=1,font=('Calibri', 12), fg='#dcdcaa', bg = '#1e1e1e',command=lancer_serveur)
bouton_start_server.grid(row=2, column=1, padx=40, pady=100)


bouton_serv = tkinter.Button (fen, text = 'Stopper le serveur',bd=1,font=('Calibri', 12), fg='#dcdcaa', bg = '#1e1e1e',command=stop_serveur)
bouton_serv.grid(row=2, column=2, padx=40, pady=100)

label_etat_serv = Label(fen, text='Etat du serveur : Déconnecté', height=2,font=('Calibri', 14),fg='#dcdcaa', bg = '#333333')
label_etat_serv.grid(row=2, column=0, padx=40, pady=100)

bouton_quitter = tkinter.Button (fen, text = 'Quitter',bd=1,font=('Calibri', 12), fg='#dcdcaa', bg = '#1e1e1e',command=quitter)
bouton_quitter.grid(row=3, column=0, padx=40, pady=40)


#Boucle d'affichage
fen.mainloop()



# ajouter un bouton "ajouter un ordre de fabrication" : voir le bug 
#modifier le produit

