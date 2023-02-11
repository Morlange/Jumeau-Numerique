import time
from opcua import Server
from opcua import Node
from random import randint,random,choice
import datetime
from product import produit, machine


#Création du serveur pour le protocole OPC UA
serveur = Server()

#url = "opc.tcp://10.10.53.128:4880"
url = "opc.tcp://127.0.0.1:4880"

serveur.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"
addspace = serveur.register_namespace(name)
root_node = serveur.get_server_node()

Param = root_node.add_object(addspace, "Paramètres")

#Définition des variables
Nb_seq = 0
prec_time = time.time()
Tech = 0.1
Nb_Machines = 4
Nom_machines = ["Four", "Coulée","Usinage","Assemblage","Métrologie"]
Nb_Stock = Nb_Machines-1
Temps_cycle_idel = [3,2,4,2]+[2]*(Nb_Machines-4)
Temps_transport = [5]*(Nb_Machines-1)
Taille_Kanban = 10
Nb_OF = 30
Nb_piece_finies = 0
Nouvelles_pieces_finies = 0
epsi_M = 0.1
epsi_T = 0.1
OF_en_cours = False

Timer_machine = [0]*Nb_Machines
Timer_Stock = [0]*Nb_Stock
Etats_T = [1]*(Nb_Machines-1)
Etats_M = [1]*Nb_Machines
Machines = [0]*Nb_Machines
Nb_piece_Stock = [0]*Nb_Stock
Nb_piece_Machine = [0]*Nb_Machines
Pieces_dans_les_stockages = [[] for k in range(Nb_Machines-1)]
Pieces_dans_les_machines = [[] for i in range(Nb_Machines)]

List_stock_a_update = [0]*(Nb_Machines-1)

Switch_Etat = [0]*Nb_Machines
Values = [[[0]*Nb_Machines,0]]
Pieces_finies = []
Lead_Time_moy = 0
TC_moy = [0]*Nb_Machines
Tps_cycle = [0]*Nb_Machines
Lead_Time = [0]
OF_fait = 0

#Espaces de créations des différentes fonctions

def entree_machines(k):
    """Fonction pour une pièce qui entre dans la machine k
    La pièce à déplacer est automatiquement prise (celle qui a attendu le plus longtemps)
     et ajoutée dans la machine.
     Si l'état de la machine est sur OFF alors il n'est pas possible 
    de lancer la fabrication de cette pièce.
    """
    if Nb_piece_Stock[k-1] > 0:
        if Machines[k].En_fonctionnement:
            Piece = Pieces_dans_les_stockages[k-1][0]
            Machines[k].ajout_piece(Piece)
            Nb_piece_Stock[k-1] -= 1
            Pieces_dans_les_stockages[k-1].pop(Pieces_dans_les_stockages[k-1].index(Piece))
            Pieces_dans_les_machines[k] += [Piece]
            List_stock_a_update[k-1] = 1
        else :
            print("La machine ne fonctionne pas !!! Err:01")

def sortie_machines(k):
    """Fonction pour faire sortir une pièce de la machine k
    La pièce à déplacer est automatiquement prise (celle qui a attendu le plus longtemps)
     et retirée dans la machine.
     Si l'état de la machine est sur OFF alors il n'est pas possible 
    de lancer la fabrication de cette pièce.
    """
    if Machines[k].nb_piece > 0 :
        if Machines[k].En_fonctionnement :
            Piece = Machines[k].fin_piece()[0]
            Pieces_dans_les_machines[k].pop(Pieces_dans_les_machines[k].index(Piece))
            Piece.sortie_machine(k)
            Nb_piece_Stock[k] += 1
            Pieces_dans_les_stockages[k] += [Piece]
            List_stock_a_update[k] = 1
        else :
            print("La machine ne fonctionne pas !!! Err:02")

def nouvelle_piece():
    """Fonction pour creer et ajouter une pièce dans la première machine.
    Si l'état de la machine est sur OFF alors il n'est pas possible 
    de lancer la fabrication de cette pièce.
    """
    global Pieces_dans_les_machines
    Pieces_dans_les_machines[0] += [produit(nb_machines=Nb_Machines)]
    if Machines[0].En_fonctionnement:
        Machines[0].ajout_piece(Pieces_dans_les_machines[0][-1])
    else:
        print("La machine ne fonctionne pas !!! Err:03")

def fin_pieces():
    """Fonction pour faire sortir une pièce de la boucle qui entre dans la machine k
    La pièce à déplacer est automatiquement prise (celle qui a attendu le plus longtemps)
     et ajoutée dans la machine.
     Si l'état de la machine est sur OFF alors il n'est pas possible 
    de lancer la fabrication de cette pièce.
    """
    global Nouvelles_pieces_finies,Values,Nb_piece_finies, Pieces_finies
    
    if Machines[-1].En_fonctionnement:
        Piece, Etat_fonctionnement = Machines[-1].fin_piece()
        Values += [Pieces_dans_les_machines[-1].pop(0).fin_process()]
        Pieces_finies += [Piece]
        Nouvelles_pieces_finies += 1
        Nb_piece_finies += 1
    else :
        print("La machine ne fonctionne pas !!! Err:04")

def ChangementEtat(k):
    """Changement bouton ON/OFF de chaque machine"""
    if Machines[k].En_fonctionnement:
        Etats_M[k] = 0
        Machines[k].On_Off()
    else:
        Etats_M[k] = 1
        Machines[k].On_Off()
    
    return None
    

#Variables du serveur

Etats = Param.add_variable(addspace, "Etats des machines", Etats_M)
NbPiecesMachines = Param.add_variable(addspace, "Nombres de pièces par machine", Nb_piece_Machine)
NbPiecesStock = Param.add_variable(addspace, "Nombres de pièces par transport", Nb_piece_Stock)
Deb = Param.add_variable(addspace, "Nombre de séquence", Nb_seq)
Chang = Param.add_variable(addspace, "Chgmt", 0)
OF_Running = Param.add_variable(addspace, "OF en cours", OF_en_cours)
Piece_finies = Param.add_variable(addspace, "Pièces finies", 0)
Nombre_de_Machines = Param.add_variable(addspace, "Nombre de machine", Nb_Machines)
Nom_des_machines = Param.add_variable(addspace, "Nom des machines", Nom_machines)
Demande_chgt_etat = Param.add_variable(addspace, "Demande de changement d'état (arrêt) des machines", Switch_Etat)
Tps_cycle_node = Param.add_variable(addspace, "Valeurs de temps de cycle", Tps_cycle)
Tps_cycle_moy_node = Param.add_variable(addspace, "Valeurs de temps de cycle moyen", TC_moy)
Lead_Time_node = Param.add_variable(addspace, "Valeurs de lead time (temps de traversée)", Lead_Time[-1])
Lead_Time_moy_node = Param.add_variable(addspace, "Valeurs de lead time moyen", Lead_Time_moy)
Stop_serv = Param.add_variable(addspace, "Pour stopper le serveur", 0)


#Autorisation de modification de certaines variables

Etats.set_writable()
Deb.set_writable()
Chang.set_writable()
OF_Running.set_writable()
NbPiecesMachines.set_writable()
NbPiecesStock.set_writable()
Piece_finies.set_writable()
Demande_chgt_etat.set_writable()
Tps_cycle_node.set_writable()
Tps_cycle_moy_node.set_writable()
Lead_Time_node.set_writable()
Lead_Time_moy_node.set_writable()
Stop_serv.set_writable()

#Lancement du serveur
serveur.start()
print("Serveur start at url : {}".format(url))

#Initialisation des machines
for i in range(Nb_Machines):
    Machines[i] = machine(Nom_machines[i])
    Nb_piece_Machine[i] = Machines[i].nb_piece

NbPiecesMachines.set_value(Nb_piece_Machine)


#Boucle principale du serveur
while True:
    #Récupération de certaines variables
    Nb_piece_Machine = [Machines[i].nb_piece for i in range(Nb_Machines)]
    Switch_Etat = Demande_chgt_etat.get_value()
    Nb_seq = Deb.get_value()
    Stop = Stop_serv.get_value()

    #Changement des états des machines si besoin
    if Switch_Etat != [0,0,0,0]:
        print("Changement !!!")
        for i in range(len(Switch_Etat)):
            if Switch_Etat[i]:
                ChangementEtat(i)
        Demande_chgt_etat.set_value([0,0,0,0])

    #Mouvement des pièces
    if Nb_seq >= 1:
        #Si on est en train de fabriquer
        if OF_en_cours - Nb_seq < 0 and Nb_piece_Machine[0] == 0 and OF_fait < Nb_seq:
            Nb_piece_Machine[0] += Nb_OF
            for i in range(Nb_OF):
                nouvelle_piece()
            OF_en_cours += 1
        #On regarde ce qu'il se passe pour chaque machine
        for i in range(Nb_Machines):
            #Si il est temps de déplacer la pièce alors on déplace la pièce
            #if time.time()-(Timer_machine[i]+choice([-1,1])*epsi_M*random()) >= Temps_cycle_idel[i] and Timer_machine[i] != 0 and Etats_M[i]:
            if time.time()-(Timer_machine[i]) >= Temps_cycle_idel[i] and Timer_machine[i] != 0 and Etats_M[i]:
                Nb_piece_Machine[i] -= 1
                Timer_machine[i] = 0
                if i < Nb_Machines-1:
                    sortie_machines(i)
                else :
                    fin_pieces()
                    Lead_Time = Values[-1][1]
                    Lead_Time_moy = round(sum([Values[k][1] for k in range(1,len(Values))])/(len(Values)-1), 3)
            
                    for l in range(Nb_Machines):
                        TC_moy[l]  = round(sum([Values[k][0][l] for k in range(1,len(Values))])/(len(Values)-1), 3)
                        Tps_cycle[l] = round(Values[-1][0][l],3) 
            #Si des pièces sont en attente d'être process et qu'il n'y a pas de pièces alors on relance des pièces
            if Nb_piece_Machine[i] >= 1 and Timer_machine[i] == 0 and Etats_M:
                Pieces_dans_les_machines[i][0].timer_machine(i)
                Timer_machine[i] = time.time()
        #Pour chaque stock, on regarde si les pièces sont prêtes à être déplacées et si oui, on les déplace
        for i in range(Nb_Machines-1):
            if Nb_piece_Stock[i] >= Taille_Kanban:
                #if time.time()-(Timer_Stock[i]+choice([-1,1])*epsi_T*random()) >= Temps_transport[i] and Timer_Stock[i] != 0 and Etats_M[i]:
                if time.time()-(Timer_Stock[i]) >= Temps_transport[i] and Timer_Stock[i] != 0 and Etats_M[i]:
                    Timer_Stock[i] = 0
                    for k in range(Taille_Kanban):
                        entree_machines(i+1)
                elif Timer_Stock[i] == 0:
                    Timer_Stock[i] = time.time()
        #Lorsqu'on a lancé toutes les pièces alors on a finit
        if Nouvelles_pieces_finies >= Nb_OF:
            Nouvelles_pieces_finies -= Nb_OF
            OF_en_cours -= 1
            OF_fait += 1
        
        #On enregistre les différentes variables sur le serveur
        NbPiecesMachines.set_value(Nb_piece_Machine)
        NbPiecesStock.set_value(Nb_piece_Stock)
        Etats.set_value(Etats_M)
        Deb.set_value(Nb_seq)
        OF_Running.set_value(OF_en_cours)
        Piece_finies.set_value(Nb_piece_finies)
        Tps_cycle_node.set_value(Tps_cycle)
        Tps_cycle_moy_node.set_value(TC_moy)
        Lead_Time_node.set_value(Lead_Time)
        Lead_Time_moy_node.set_value(Lead_Time_moy)

        #On peut eteindre le serveur si on lui demande
    if Stop:
        time.sleep(2)
        serveur.stop()
        print("Serveur déconnecté")
        break


    
                




    

    
    
    
