from PIL import Image, ImageTk
from tkinter import Label, Tk, Canvas, NW
from tkinter import ttk
from tkinter.messagebox import showinfo
from data import LogoAM, color_bg1, color_bg, color_fg, Gammes,liste_zone,liste_machines
from opcua import Client


imageflux_RDC=Image.open("Flux_RDC.png")
imageflux_1er=Image.open("Flux_1er.png")

def main():
    '''sert à se connecter au serveur'''
    global LogoAM
    url = "opc.tcp://127.0.0.1:4880"
    client = Client(url)
    client.connect()
    print("Client connected")

    NbPiecesMachines = client.get_node("ns = 2; i = 3")
    Gammes_actuelles = client.get_node("ns = 2; i = 17")
    Demande_chgt_gamme = client.get_node("ns = 2; i = 18")


    def afficher_flux ():
        '''fonction créant la fenêtre'''
        # creation de l'objet fenetre
        fen_flux= Tk()

        #Titre de la fenetre
        fen_flux.title('Analyse de production')

        #Taille de la fenetre
        fen_flux.geometry('1300x630')

        #icone de fenetre
        fen_flux.iconbitmap('logo-AM.ico')

        #configuration du fond
        fen_flux.config(background=color_bg1)
        
        #titre de la fenêtre
        label_titre = Label(fen_flux, text='Analyse de production', height=1,font=('Calibri', 14),fg=color_fg, bg=color_bg1) 
        label_titre.grid(row=0,column=1)


        label_Flux = Label(fen_flux, text='Flux', font =('Calibri', 12), fg=color_fg, bg=color_bg1)
        Label(label_Flux, text='Flux').grid(row=1, column=0)

        #def afficher_Image(fen,row,column,name,size):
        """
        size = (100,150)
        img = ImageTk.PhotoImage(Image.open("flux.png").resize((50,50)))
        canv = Canvas(frame_TRS, highlightthickness = 0, bg="#333333", height=size[0], width=size[1])
        canv.grid(row=0, column=0)
        canv.create_image(0,0, image = img)"""

        #Importation de l'image de fond
        #image = ImageTk.PhotoImage(Image.open("flux.png"))
        imaged=Canvas(fen_flux,bg=color_bg, width=585,height=400)
        image1 = ImageTk.PhotoImage(imageflux_RDC)
        image2 = ImageTk.PhotoImage(imageflux_1er)
        logo1 = imaged.create_image(0,0, anchor = NW, image = image1)
        imaged.grid(row=1,column=1)
        imageg=Canvas(fen_flux,bg=color_bg, width=576,height=400)
        logo2 = imageg.create_image(0,0, anchor = NW, image = image2)
        imageg.grid(row=1,column=0)
        # TempLabel2 = Label(fen_flux, image=image2)
        # TempLabel2.grid(row=1,column=2,padx=20,pady=20) 
        # TempLabel1 = Label(fen_flux, image=image1)
        # TempLabel1.grid(row=1,column=1,padx=20,pady=20) 
        
        #Création de la Combobox
        liste_gammes = [Gammes[k].nom_produit for k in range(len(Gammes))]
            
        #Choisir l'élément qui s'affiche par défaut
        

        """affichage des flux en fonction de la pièce choisie"""
        select = Gammes_actuelles.get_value()

        #affichage= NbPiecesMachines.get_value()
        
        

        Liste_lieux=["Composite","Usinage","Forge","Metrologie","Assemblage","Bois","Fonderie"]
        #coordonnées des machines sur l'image (référentiel fenêtre)
        coordonnées_zones=[[500,65],[310,65],[477,325],[130,65],[210,65],[400,65],[380,140]]
        Nb_Pieces_Machine = NbPiecesMachines.get_value()
        Machines=Gammes[liste_gammes.index(select)].liste_ordre_machine
        Liste_nombre_piece=[0]*(len(Liste_lieux))
        for k in range (len(Nb_Pieces_Machine)):
            ind=liste_machines.index(Machines[k])
            print(liste_zone[ind])
            if liste_zone[ind]== "Composite":
                Liste_nombre_piece[0]+=Nb_Pieces_Machine[k]
            if liste_zone[ind]== "Usinage":
                Liste_nombre_piece[1]+=Nb_Pieces_Machine[k]
            if liste_zone[ind]== "Forge":
                Liste_nombre_piece[2]+=Nb_Pieces_Machine[k]
            if liste_zone[ind]== "Metrologie":
                Liste_nombre_piece[3]+=Nb_Pieces_Machine[k]
            if liste_zone[ind]== "Assemblage":
                Liste_nombre_piece[4]+=Nb_Pieces_Machine[k]
            if liste_zone[ind]== "Bois":
                Liste_nombre_piece[5]+=Nb_Pieces_Machine[k]
            if liste_zone[ind]== "Fonderie":
                Liste_nombre_piece[6]+=Nb_Pieces_Machine[k]


        label_nbpiece = [0 for  k in range(7)]
        
        #création de l'affichage
        for i in range (len(Liste_nombre_piece)):
            label_nbpiece[i] = imageg.create_text(coordonnées_zones[i][0],coordonnées_zones[i][1],text=Liste_nombre_piece[i], fill = 'black' ,font=("Calibri",14))
            #canv.create_text(list_x[i],list_y[i],text=nom_machine[i], fill = "#dcdcaa")
            
        def trait (coord0,coord1):
            x0,y0=coord0
            x1,y1=coord1
            decalage=6
            if x0>x1:
                x0=x0-decalage
                x1=x1+decalage
            elif x0<x1:
                x0=x0+decalage
                x1=x1-decalage                
            if y0>y1:
                y0=y0-decalage
                y1=y1+decalage
            elif y0<y1:
                y0=y0+decalage
                y1=y1-decalage

            imageg.create_line(x0, y0, x1, y1, width=2)

        # trait(coordonnées_zones[1],coordonnées_zones[2])
        # trait(coordonnées_zones[1],coordonnées_zones[6])
        # trait(coordonnées_zones[3],coordonnées_zones[4])
        # trait(coordonnées_zones[4],coordonnées_zones[1])
    
        fen_flux.mainloop()



    

    afficher_flux()
if __name__ == "__main__":
    main()