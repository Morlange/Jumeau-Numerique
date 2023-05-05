from tkinter import Tk, Label, Canvas, LabelFrame,ttk, VERTICAL, S
from PIL import Image, ImageTk
from fonction import afficher_Image
from data import taille, Images, color_bg1, color_fg, TRS, Gammes
from numpy import c_, linspace, radians, pi, degrees, cos, sin
from matplotlib import cm
from matplotlib.pyplot import subplots, tight_layout, savefig
from matplotlib.patches import Circle, Wedge, Rectangle
import openpyxl as op
from random import randint # a supprimer quand le programme sera fait (sert a avoir des valeurs de TRS)
from opcua import Client

def main():
    global Images
    print("Ouverture Analyse")

    # creation de l'objet fenetre
    fen_analyse= Tk()

    #Titre de la fenetre
    fen_analyse.title('Analyse de production')

    #Taille de la fenetre
    fen_analyse.geometry('1300x630')

    #icone de fenetre
    fen_analyse.iconbitmap('logo-AM.ico')

    #configuration du fond
    fen_analyse.config(background=color_bg1)
    #Ajout d'un titre 
    label_titre = Label(fen_analyse, text='Analyse de production', height=1,fg=color_fg,font=('Calibri', 14),bg=color_bg1) 
    label_titre.grid(row=0,column=1)

    # Selectionner produit 
    #label_choix = Label(fen_analyse, text='Choisissez un produit:',fg=color_fg, bg=color_bg1)
    #label_choix.grid(row=1, column=0, padx=0, pady=10)

    #récupère le nom de tous les produits depuis le fichier data
    liste_nom_gammes = [Gammes[k].nom_produit for k in range(len(Gammes))]

    #Création de la Combobox
    #listeCombo = ttk.Combobox(fen_analyse, values=liste_nom_gammes)

    TRS=[randint (1,100) for i in range (len(liste_nom_gammes))]

    
    # Obtenir le nom du produit dans le serveur
    url = "opc.tcp://127.0.0.1:4880"
    client = Client(url)
    client.connect()
    print("Client connected")

    NbPiecesMachines = client.get_node("ns = 2; i = 3")
    Gammes_actuelles = client.get_node("ns = 2; i = 17")

    #récupère la liste des machines utilisées pour la fabrication du produit choisi 
    liste_nom_machine = Gammes[liste_nom_gammes.index(Gammes_actuelles.get_value())].nom_process

    #fonction qui créée le fichier .png pour l'affichage des TRS
    def creerGraphsTRS(x,name,titre = "Titre du graphique"):
        #x valeur en pourcentage
        TRSgraph=[]
        namefile = name
        #conversion en .png
        if not name[-4:] == ".png":
            namefile += ".png"

        #On affiche le TRS de 5 en 5 donc on mets le TRS à jour en fonction du chiffre des unités 
        # (1, 2, 3 -> 0), (4, 5 -> 5), (6, 7, 8 -> 5), (9->10)
        a=x%10
        if a==1 or a==2 or a==3 : 
            x=int((x/10)%10)*10
        elif a==4 or a==5 :
            x=int((x/10)%10)*10+5
        elif a==6 or a==7 or a==8 : 
            x=int((x/10)%10)*10+5
        elif a==9 : 
            x=int((x/10)%10)*10+10
        
        #on sépart les valeurs du TRS en segments (la valeur affichée n'est pas précise mais correspond à une zone)
        TRSlist=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
        TRSgraph.append(TRSlist.index(x)+1)  

        #divise les 180 degrés en n secteurs
        def degree_range(n): 
            start = linspace(0,180,n+1, endpoint=True)[0:-1]
            end = linspace(0,180,n+1, endpoint=True)[1::]
            mid_points = start + ((end-start)/2.)
            return c_[start, end], mid_points

        #fonction pour écrire le texte en arc de cercle (valeur des TRS)
        def rot_text(ang): 
            rotation = degrees(radians(ang) * pi / pi - radians(90))
            return rotation

        #fonction pour définir la partie visuelle des graphes
        def gauge(labels=['secteur1','secteur2','secteur3', 'secteur4','secteur5'], \
                colors='jet_r', arrow=1, title='', fname=False): 
            
            N = len(labels)

            # début de l'affichage
            fig, ax = subplots()
            ang_range, mid_points = degree_range(N)
            labels = labels[::-1]
            
            #affiche les secteurs et les arcs
            patches = []
            for ang, c in zip(ang_range, colors): 
                # secteurs
                patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
                # arcs
                patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))
            
            [ax.add_patch(p) for p in patches]
            
            #affiche les labels (secteur1, secteur2, ...)
            for mid, lab in zip(mid_points, labels): 

                ax.text(0.35 * cos(radians(mid)), 0.35 * sin(radians(mid)), lab, \
                    horizontalalignment='center', verticalalignment='center', fontsize=14, \
                    fontweight='bold', rotation = rot_text(mid))

            #affiche les arrow
            pos = mid_points[abs(arrow - N)]
            
            ax.arrow(0, 0, 0.225 * cos(radians(pos)), 0.225 * sin(radians(pos)), \
                        width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
            
            ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
            ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

            #affiche correctement les axes
            ax.set_frame_on(False)
            ax.axes.set_xticks([])
            ax.axes.set_yticks([])
            ax.axis('equal')
            tight_layout()
            if fname:
                fig.savefig(fname, dpi=200)

        image=gauge(labels=['0',' ','10',' ','20',' ','30',' ','40',' ','50',' ','60',' ','70',' ','80',' ','90',' ','100'], \
            colors=['#ED1C24','#ED1C24','#ED1C24','#ED1C24','#ED1C24','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00',
                    '#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#007A00','#007A00','#007A00','#007A00',
                    '#007A00'], arrow=TRSgraph[0], title=titre)
        
        savefig(namefile, transparent = True)

    
    
    #Frame TRS
    #frame_TRS = LabelFrame(fen_analyse, text='TRS', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    #frame_TRS.grid(row=1,column=0)
    #Label(frame_TRS, text='Fonderie', background=color_bg1, fg=color_fg).grid(row=1, column=0)
    #Label(frame_TRS, text='Usinage', background=color_bg1, fg=color_fg).grid(row=3, column=0)
    #Label(frame_TRS, text='Assemblage', background=color_bg1, fg=color_fg).grid(row=5, column=0)


    #Choisir l'élément qui s'affiche par défaut
    #listeCombo.grid(row=1, column=1,padx=0,pady=10)

    #listeCombo.bind("<<ComboboxSelected>>", action)

    #PROGRAMME EN COURS POUR CREER ET AFFICHER LES IMAGES TRS DE TOUTES LES MACHINES (à adapter)
    k=len(liste_nom_machine)
    TRS1=[randint(0,100) for i in range (k)] # liste aléatoire pour l'instant

    liste_pour_TRS = [TRS1,liste_nom_machine] #TRS1 est une liste à remplacer par la vraie liste des TRS
    N = len(liste_pour_TRS[0])
    frame_TRS = LabelFrame(fen_analyse, text='TRS', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    frame_TRS.grid(row=1,column=0)
    frame_temps_de_production = LabelFrame(fen_analyse, text='Temps de production', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    frame_temps_de_production.grid(row=1,column=1)
    frame_nb_pieces = LabelFrame(fen_analyse, text='Nombre de pièces produites', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    frame_nb_pieces.grid(row=1,column=3)
    k=0
    j=1
    Nombre_pieces = NbPiecesMachines.get_value()
    for i in range (N) : 
       creerGraphsTRS(liste_pour_TRS[0][i],liste_pour_TRS[1][i], liste_pour_TRS[1][i])
       Images += afficher_Image(frame_TRS,j,k, liste_pour_TRS[1][i]+".png",taille,Images)

       Label(frame_TRS, text=liste_pour_TRS[1][i], background=color_bg1, fg=color_fg).grid(row=j+1, column=k)
       Label(frame_temps_de_production, text=liste_pour_TRS[1][i], background=color_bg1, fg=color_fg).grid(row=i, column=0)
       Label(frame_nb_pieces, text=liste_pour_TRS[1][i], bg=color_bg1, fg=color_fg).grid(row=i, column=0)

       Label(frame_temps_de_production, text=Nombre_pieces[i], bg=color_bg1, fg=color_fg).grid(row=i, column=1)
       Label(frame_nb_pieces, text='0', bg=color_bg1, fg=color_fg).grid(row=i, column=1)

       if k==1 : 
           k=0
           j=j+2
       elif k==0 : 
           k=1  


    #creerGraphsTRS(TRS[0],"TRS_fonderie","TRS fonderie")
    #creerGraphsTRS(TRS[1],"TRS_usinage","TRS usinage")
    #creerGraphsTRS(TRS[2],"TRS_assemblage","TRS assemblage")

    #Images += afficher_Image(frame_TRS,2,0,"TRS_usinage.png",taille,Images)
    #Images += afficher_Image(frame_TRS,4,0,"TRS_fonderie.png",taille,Images)
    #Images += afficher_Image(frame_TRS,6,0,"TRS_assemblage.png",taille,Images)

    """
    Label(frame_TRS, label_usinage, bg=color_bg1).grid(row=2, column=0)
    Label(frame_TRS, label_fonderie, bg=).grid(row=4, column=0)           ###mettre les images 
    Label(frame_TRS, label_assemblage, bg=color_bg1).grid(row=6, column=0)
    """

    #Frame Temps de production
    #frame_temps_de_production = LabelFrame(fen_analyse, text='Temps de production', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    #frame_temps_de_production.grid(row=1,column=1)
    #Label(frame_temps_de_production, text='Fonderie', background=color_bg1, fg=color_fg).grid(row=2, column=0)
    #Label(frame_temps_de_production, text='Usinage', background=color_bg1, fg=color_fg).grid(row=2, column=1)
    #Label(frame_temps_de_production, text='Assemblage', background=color_bg1, fg=color_fg).grid(row=2, column=2)

    #Label(frame_temps_de_production, text='0', bg=color_bg1, fg=color_fg).grid(row=3, column=0)
    #Label(frame_temps_de_production, text='0', bg=color_bg1, fg=color_fg).grid(row=3, column=1)
    #Label(frame_temps_de_production, text='0', bg=color_bg1, fg=color_fg).grid(row=3, column=2)

    #Frame nombre de pièces 
    #frame_nb_pieces = LabelFrame(fen_analyse, text='Nombre de pièces produites', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    #frame_nb_pieces.grid(row=1,column=2)
    #Label(frame_nb_pieces, text='Fonderie', bg=color_bg1, fg=color_fg).grid(row=3, column=0)
    #Label(frame_nb_pieces, text='Usinage', bg=color_bg1, fg=color_fg).grid(row=3, column=1)
    #Label(frame_nb_pieces, text='Assemblage', bg=color_bg1, fg=color_fg).grid(row=3, column=2)

    #Label(frame_nb_pieces, text='0', bg=color_bg1, fg=color_fg).grid(row=4, column=0)
    #Label(frame_nb_pieces, text='0', bg=color_bg1, fg=color_fg).grid(row=4, column=1)
    #Label(frame_nb_pieces, text='0', bg=color_bg1, fg=color_fg).grid(row=4, column=2)

    #Boucle d'affichage
    fen_analyse.mainloop()

if __name__ == "__main__":
    main()