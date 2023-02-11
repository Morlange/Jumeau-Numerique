from tkinter import Button, Canvas, Tk, Label, PhotoImage, CENTER, LAST
from functools import partial
from opcua import Client
from opcua import Node
from product import produit, machine
from PIL import Image, ImageTk
from tkinter import ttk


LogoAM = "Logo_AM.png"

#Initialisation du protocole OPC/UA

#url = "opc.tcp://10.10.53.128:4880"
def main():
    global LogoAM
    url = "opc.tcp://127.0.0.1:4880"
    client = Client(url)
    client.connect()
    print("Client connected")
    


    Etats = client.get_node("ns = 2; i = 2")
    NbPiecesMachines = client.get_node("ns = 2; i = 3")
    NbPiecesStock = client.get_node("ns = 2; i = 4")
    Chang = client.get_node("ns = 2; i = 6")
    Piece_finie = client.get_node("ns = 2; i = 8")
    Nb_Machines = client.get_node("ns = 2; i = 9")
    Nom_des_machines = client.get_node("ns = 2; i = 10")
    Demandechgtetat = client.get_node("ns = 2; i = 11")
    Tps_cycle_node = client.get_node("ns = 2; i = 12")
    Tps_cycle_moy_node = client.get_node("ns = 2; i = 13")
    Lead_Time_node = client.get_node("ns = 2; i = 14")
    Lead_Time_moy_node = client.get_node("ns = 2; i = 15")
    Deb = client.get_node("ns = 2; i = 5")
    Stop_serv = client.get_node("ns = 2; i = 16")

    #Initialisation de la fenêtre Tkinter
    fen_etat=Tk()
    fen_etat.geometry("1500x1500")
    fen_etat.config(bg="#333333")
    fen_etat.title("Etat des machines")

    #Initialisation des différentes variables 
    nb_machine=Nb_Machines.get_value()
    list_etat=Etats.get_value()
    list_x=[200*(i+1) for i in range(nb_machine)]
    list_y=[150]*nb_machine
    bouton_urgence = [0 for i in range(nb_machine)]
    bouton_suivant = [0 for i in range(nb_machine*2)]
    Label_position_machine = [0 for i in range(nb_machine)]
    Label_position_transport = [0 for i in range(nb_machine-1)]
    Label_temps_cycle =[0 for i in range (nb_machine)]
    Label_temps_cycle_moy =[0 for i in range (nb_machine)]
    Label_Lead_Time = 0
    nom_machine= Nom_des_machines.get_value()

    Nb_piece_machine = NbPiecesMachines.get_value()
    Nb_piece_stockage = NbPiecesStock.get_value()
    Pieces_dans_les_machines = [[]]*nb_machine
    Pieces_dans_les_stockages = [[]]*(nb_machine-1)
    Nouvelle_piece_finie = 0
    Nb_pieces_finies = Piece_finie.get_value()
    epsi = 0.001
    Pieces_finies = []
    img = [ImageTk.PhotoImage(Image.open("StockVide.png").resize((50,50)))]
    Images = []
    piece_max = 30
    Loval=[None]*nb_machine
    Demande_chgt_etat = Demandechgtetat.get_value()
    Tps_cycle,Tc_moy,Lead_Time,Lead_Time_moy = Tps_cycle_node.get_value(),Tps_cycle_moy_node.get_value(), Lead_Time_node.get_value(), Lead_Time_moy_node.get_value()
    Ancien_nb_P_finie = 0
    Nb_seq = Deb.get_value()
    print(Nb_seq)

    #Initialisation d'une list d'image
    for i in range(1,5):
        img += [ImageTk.PhotoImage(Image.open("Stock"+str(i)+".png").resize((50,50)))]


    #Initialisation du canvas Tkinter
    canv = Canvas(fen_etat, highlightthickness = 0, bg="#333333", height=1500, width=1500)
    canv.place(x=1,y=1)




    def Simpletoggle(k):
        """Changement bouton ON/OFF de chaque machine"""
        if bouton_urgence[k].config('text')[-1] == "ON":
            bouton_urgence[k].config(text = "OFF", fg='white', bg = 'salmon')
            
        else:
            bouton_urgence[k].config(text = "ON", fg='white', bg = 'olivedrab')
        Demande_chgt_etat[k] = 1
        Demandechgtetat.set_value(Demande_chgt_etat)
        Demande_chgt_etat[k] = 0
        print("Je demande le changement !")
        return None


    def Etat_stockage(k,pmax):
        """Permet de renvoyer une information sur le stockage/transport des pièces entre 
        la machine k et k+1. 
        Renvoie un int entre 0 et 4 inclus image du stock par rapport au stock maxi 
        4 = Stock Maxi, par exemple : la capacité de l'AVG"""
        global piece_max
        if Nb_piece_stockage[k] == 0:
            return 0
        return int((Nb_piece_stockage[k]/pmax*100)//33)+1

    def Update_image_stock(k,pmax):
        """Permet de mettre à jour les images des images des stock/transports"""
        canv.itemconfig(Images[k], image = img[Etat_stockage(k,pmax)])

    def Demande_ajout_OF(Nb_seq):
        print("Hello... On peut start !!!")
        Deb.set_value(Nb_seq + 1)


    #Création d'un bouton pour lancer des OF
    Bouton_debut_OF = Button(fen_etat,text="Lancement 1 OF",bd=1,font=('Times new roman', 12), fg='#dcdcaa', bg = '#1e1e1e',command=partial(Demande_ajout_OF,Nb_seq), width= 14)
    Bouton_debut_OF.place(x = 10, y = 10)

    #Création des machines
    for i in range(nb_machine):
        canv.create_text(list_x[i],list_y[i],text=nom_machine[i], fill = "#dcdcaa")
        bouton_urgence[i] = Button(fen_etat, text="ON",bd=1,font=('Times new roman', 12),fg='white', bg = 'olivedrab', command=partial(Simpletoggle,i), width = 4)
        bouton_urgence[i].place(x=list_x[i] - 2*9 ,y=list_y[i]-40)

    """
    #Création des bouton relatifs au machines E/S
    for i in range (nb_machine):
        if i != 0:
            bouton=Button(fen_etat,text=" Entrée machine ",bd=1,font=('Times new roman', 12), fg='#dcdcaa', bg = '#1e1e1e',command=partial(entree_machine,i), width= 14)
            bouton.place(x=list_x[i] - 9*7 ,y=list_y[i]+70)
        if i != nb_machine-1:
            bouton=Button(fen_etat,text=" Sortie machine ",bd=1,font=('Times new roman', 12), fg='#dcdcaa', bg = '#1e1e1e',command=partial(sortie_machine,i), width= 14)
            bouton.place(x=list_x[i] - 9*7 ,y=list_y[i]+105)
    bouton_suivant[0]=Button(fen_etat,text=" Nouvelle pièce ",bd=1,font=('Times new roman', 12), fg='#dcdcaa', bg = '#1e1e1e',command=nouvelle_piece, width= 14)
    bouton_suivant[0].place(x=list_x[0] - 9*7 ,y=list_y[nb_machine-1]+70)
    bouton_suivant[-1]=Button(fen_etat,text=" Pièce finie ",bd=1,font=('Times new roman', 12), fg='#dcdcaa', bg = '#1e1e1e',command=fin_piece, width= 14)
    bouton_suivant[-1].place(x=list_x[nb_machine-1] - 9*7,y=list_y[nb_machine-1]+105)
    """

    #Création des labels pour le nombre de pièces dans les machines
    for i in range (nb_machine):
        Label_position_machine[i]=Label(fen_etat,text=Nb_piece_machine[i],bd=0,font=('Times new roman', 12),fg='#dcdcaa', bg='#333333')
        Label_position_machine[i].place(x=list_x[i]- 4.5,y=list_y[i]+20)


    #Création des labels pour afficher le nombre de pièces dans les stockages/transports
    for i in range (nb_machine-1):
        Label_position_transport[i]=Label(fen_etat,text="NON",bd=0,font=('Times new roman', 12),fg='#dcdcaa', bg='#333333')
        Label_position_transport[i].place(x=(list_x[i+1]+list_x[i])/2,y=(list_y[i]+list_y[i+1])/2+20)
        Images += [canv.create_image((list_x[i+1]+list_x[i])/2, (list_y[i]+list_y[i+1])/2+100, image = img[0])]


    #Création des labels pour afficher les temps de cycles mesurés et moyens 
    #La moyenne est prise sur les pièces déjà finies
    #Les Labels s'actualisent à chaque fois qu'une pièce se termine
    print("Ah...")
    for i in range (nb_machine):
        Label_temps_cycle[i]=Label(fen_etat,text= "Temps de cycle {0} : {1} secondes".format(nom_machine[i],Tps_cycle[i]),bd=0,font=('Times new roman', 12),fg='#dcdcaa', bg = '#1e1e1e')
        Label_temps_cycle[i].place(x=20,y=940-45*(1+i))
        Label_temps_cycle_moy[i]=Label(fen_etat,text= "Temps de cycle moyen {0} : {1} secondes".format(nom_machine[i],Tc_moy[i]),bd=0,font=('Times new roman', 12),fg='#dcdcaa', bg = '#1e1e1e')
        Label_temps_cycle_moy[i].place(x=500,y=940-45*(1+i))
    Label_Lead_Time=Label(fen_etat,text='Lead Time ',bd=0,font=('Times new roman', 12),fg='#dcdcaa', bg = '#1e1e1e')
    Label_Lead_Time.place(x=20,y=940)
    Label_Lead_Time_moy=Label(fen_etat,text='Lead Time moyen',bd=0,font=('Times new roman', 12),fg='#dcdcaa', bg = '#1e1e1e')
    Label_Lead_Time_moy.place(x=500,y=940)


    #Création d'une flèche d'une machine vers la machine suivante
    for i in range (nb_machine-1):
        canv.create_line(list_x[i]+40,list_y[i],list_x[i+1]-40,list_y[i+1], arrow= LAST, fill="#dcdcaa")



    #Initialisation des cercles, liés à l'état des machines
    #Processing = orange, Au repos = gris
    for i in range (nb_machine): 
        if list_etat[i]==1:
            a=canv.create_oval(list_x[i]+15,list_y[i]+40,list_x[i]+35,list_y[i]+20, offset= "100,0", fill="orange", outline="#1e1e1e")
        else :  
            a=canv.create_oval(list_x[i]+15,list_y[i]+40,list_x[i]+35,list_y[i]+20,fill="grey", outline="#1e1e1e")
        Loval[i] = a



    #Boucle principal du programme
    while True:
        
        #Récupération des variable depuis le serveur via le protocole OPC/UA
        Nb_piece_machine = NbPiecesMachines.get_value()
        Nb_piece_stockage = NbPiecesStock.get_value()
        Etats_M = Etats.get_value()
        Nb_pieces_finies = Piece_finie.get_value()
        Tps_cycle,Tc_moy,Lead_Time,Lead_Time_moy = Tps_cycle_node.get_value(),Tps_cycle_moy_node.get_value(), Lead_Time_node.get_value(), Lead_Time_moy_node.get_value()
        Nb_seq = Deb.get_value()
        Stop = Stop_serv.get_value()

        
        #Actualisation du nombre de pièces par machine et du nombre de pièces par stock
        for i in range(nb_machine):
            Label_position_machine[i].configure(text = Nb_piece_machine[i])
        for i in range(len(Nb_piece_stockage)):
            Label_position_transport[i].configure(text = Nb_piece_stockage[i])
            canv.itemconfig(Images[i], image = img[Etat_stockage(i,piece_max)])
        

        #Actualisation des états des machines
        for i in range(len(Loval)) :
            if Etats_M[i] == 1 and Nb_piece_machine[i] > 0:
                canv.itemconfigure(Loval[i],fill = "orange")
            else:
                canv.itemconfigure(Loval[i],fill = "grey")
        


        #Si une pièce se termine : Actualisation des temps de cycle et temps de cyle moyen
        if Nb_pieces_finies > Ancien_nb_P_finie:
            for i in range(nb_machine):
                Label_temps_cycle_moy[i].configure(text = "Temps de cycle moyen {0} : {1} secondes".format(nom_machine[i], Tc_moy[i]))
                if Tps_cycle[i] > Tc_moy[i] + epsi :
                    Label_temps_cycle[i].configure(text = "Temps de cycle {0} : {1} secondes".format(nom_machine[i],Tps_cycle[i]), bg = 'salmon') #Changer la couleur pour un peu plus foncé
                else :
                    Label_temps_cycle[i].configure(text = "Temps de cycle {0} : {1} secondes".format(nom_machine[i],Tps_cycle[i]), bg = 'olivedrab')
            if Lead_Time > Lead_Time_moy + epsi:
                Label_Lead_Time.configure(text = "Lead Time = {0} secondes".format(Lead_Time), bg = 'salmon')
            else:
                Label_Lead_Time.configure(text = "Lead Time = {0} secondes".format(Lead_Time), bg = 'olivedrab')
            Label_Lead_Time_moy.configure(text = "Lead Time moyen = {0} secondes".format(Lead_Time_moy))
            Ancien_nb_P_finie = Nb_pieces_finies
        
        
        if Stop:
            client.disconnect()
            fen_etat.destroy()
            return "Travail terminé"
            
        #Actualisation de la fenêtre
        fen_etat.update()
    
try:
    print(main())
except ConnectionRefusedError :
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

