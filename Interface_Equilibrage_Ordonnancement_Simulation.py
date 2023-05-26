## Programme d'equilibrage et d'ordonnancement de ligne de production
#==================================================================================================
#==================================================================================================

##definitions et structures :

#liste des produits : [produit_1,produit2,...]
#Graphe de precedences d'un produit: [[op_principale,op_necessaire_1,op_necessaire_2],[...],...]
#Table des temps operatoires d'un produit : [[nom_operation,temps_de_travail],...]

#==================================================================================================
#==================================================================================================
##imports:
#==================================================================================================
#==================================================================================================
import numpy as np

#==================================================================================================
#==================================================================================================
##functions:
#==================================================================================================
#==================================================================================================

def somme_liste(liste):
    somme = 0
    for i in range(len(liste)):
        somme += liste[i]
    return somme

def appartient_liste(element,liste_):
    for i in range(len(liste_)):
        if liste_[i] == element:
            return True
    return False

def liste_appartient_liste(liste_incluse,liste_globale):
    '''ENTREE : une liste d'elemnts dont on veut verifier qu'ils appartiennent tous à la liste globale
    SORTIE : booleen : Vrai ou Faux'''
    for i in range(len(liste_incluse)):
        if not(appartient_liste(liste_incluse[i],liste_globale)):
            return False
    return True

def Sjk_machine(liste_op_machine,object_product):
    '''ENTREE : liste des operations affectees a la machine, nom du produit
    [op1,op2,...] avec op = ["nom_op",object product]
    SORTIE : Sommes des temps operatoires du produit j a la machine k (Sjk)'''
    somme_temps_op = 0
    for i in range(len(liste_op_machine)):
        if liste_op_machine[i][1] == object_product:
            somme_temps_op += object_product.temps_travail(liste_op_machine[i][0])
    return somme_temps_op

def enleve_doublons(liste):
    liste_elements_rencontres = []
    for i in range(len(liste)):
        if not(appartient_liste(liste[i],liste_elements_rencontres)):
            liste_elements_rencontres.append(liste[i])
    return liste_elements_rencontres



#possibilite d amelioration du temps de calcul : ne pas recalculer a chaque fois la liste des proportions, utiliser celle deja faite au debut de l algo qui l appelle


def Q(solution,liste_produits):
    '''ENTREE : solution : [[operation_1,operation2],[operation3,...],[]] avec [op1,op2] representant la premiere machine, et operation_i = [nom_operation_i,objet_produit];
    [[object produit1,quantite], [object produit2,quantite],...]
    SORTIE : valeur de cout/objectif flotant : charge ponderee de la station goulot
    FONCTION : fonction objectif ou coût pour juger la qualite d une solution fournie'''

    #initialisations :
    liste_charges_machines = []
    J = len(liste_produits)
    nombre_machines = len(solution)

    #calcul des proportions de chaque produits:
    somme = 0
    liste_proportions = []
    for j in range(J):
        somme += liste_produits[j][1]
    for j in range(J):
        liste_proportions.append([liste_produits[j][0],liste_produits[j][1]/somme])

    #calcul des charges ponderees pour chaque machine
    for k in range(nombre_machines):
        charge_k = 0
        for j in range(J):
            produit = liste_proportions[j][0]
            w_jk = liste_proportions[j][1]
            charge_k += w_jk*Sjk_machine(solution[k],produit)
        liste_charges_machines.append(charge_k)
    return max(liste_charges_machines)



#==================================================================================================
#==================================================================================================
##Equilibrage :
#==================================================================================================
#==================================================================================================

#solution initiale :


def solution_initiale(nombre_de_machines,liste_produits):
    '''ENTREE : [[object produit1,quantite], [object produit2,quantite],...]
    SORTIE : [[operation_1,operation2],[operation3,...],[]] avec [op1,op2] representant la premiere machine, et operation_i = [nom_operation_i,objet_produit]'''

    #definition des fonctions utiles

    def tri_groupe(groupe):
        '''ENTREE : groupe (niveau d operations a trier) [[A,produit1],[B,produit2],...]
        SORTIE : groupe triee (avec non destruction de l'entree)'''
        n = len(groupe)
        liste_tri = [] #[[nom_op,produit,nombre_predecesseurs],...]

        #remplissage listes utilisees pour le tri
        liste_op_nom_0 = []
        liste_op_produit_0 = []
        liste_op_nbr_succ_0 = []
        #remplissage des listes
        for i in range(n):
            nom_op = groupe[i][0]
            produit = groupe[i][1]
            liste_succ = produit.return_tous_successeurs(nom_op)
            nombre_succ = len(liste_succ)

            liste_op_nom_0.append(nom_op)
            liste_op_produit_0.append(produit)
            liste_op_nbr_succ_0.append(nombre_succ)

        #tri par nbre decroissant de successeurs sans cas d egalite
        liste_op_nom_1 = []
        liste_op_produit_1 = []
        liste_op_nbr_succ_1 = []
        for i in range(n):
            #indice du max de successeurs
            indice_max = liste_op_nbr_succ_0.index(max(liste_op_nbr_succ_0))
            #remplissage des nouvelles listes triees
            liste_op_nom_1.append(liste_op_nom_0[indice_max])
            liste_op_produit_1.append(liste_op_produit_0[indice_max])
            liste_op_nbr_succ_1.append(liste_op_nbr_succ_0[indice_max])
            #enleve l ancien element des listes non triees
            liste_op_nom_0.pop(indice_max)
            liste_op_produit_0.pop(indice_max)
            liste_op_nbr_succ_0.pop(indice_max)

        #tri des cas d egalite :
        liste_paquets_nom = [[liste_op_nom_1[0]]] #liste qui va contenir les elements de liste avec le même nombre de predecesseurs
        liste_paquets_produit = [[liste_op_produit_1[0]]]
        liste_paquets_temps_op = [[0]]
        liste_paquets_nbr_pred = [[liste_op_nbr_succ_1[0]]]

        #creation des paquets d op de meme nombre de successeurs :
        for i in range(1,n):
            if liste_op_nbr_succ_1[i-1] == liste_op_nbr_succ_1[i-1]:
                liste_paquets_nom[-1].append(liste_op_nom_1[i])
                liste_paquets_produit[-1].append(liste_op_produit_1[i])
                liste_paquets_nbr_pred[-1].append(liste_op_nbr_succ_1[i])
                liste_paquets_temps_op[-1].append(0)
            else:
                liste_paquets_nom.append([liste_op_nom_1[i]])
                liste_paquets_produit.append([liste_op_produit_1[i]])
                liste_paquets_nbr_pred.append([liste_op_nbr_succ_1[i]])
                liste_paquets_temps_op.append([0])

        #ajout des temps operatoires qd plusieurs au sein d un paquet
        nbre_paquets = len(liste_paquets_nom)
        for i in range(nbre_paquets):
            nbre_elements_paquet = len(liste_paquets_nom[i])
            if nbre_elements_paquet >1:
                for j in range(nbre_elements_paquet):
                    produit = liste_paquets_produit[i][j]
                    nom_operation = liste_paquets_nom[i][j]
                    liste_successeurs = produit.return_tous_successeurs(nom_operation)
                    nombre_successeurs = len(liste_successeurs)
                    somme_tp_op_successeurs_i = 0
                    for k in range(nombre_successeurs):
                        somme_tp_op_successeurs_i += produit.temps_travail(liste_successeurs[k])
                    liste_paquets_temps_op[i][j] = somme_tp_op_successeurs_i

        #tri pour chaque paquet par temps operatoire decroissant de tous les successeurs
        nbre_paquets = len(liste_paquets_nom)
        for i in range(nbre_paquets):
            nbre_elements_paquet = len(liste_paquets_nom[i])
            if nbre_elements_paquet >1:
                new_paquet_nom = []
                new_paquet_produit = []
                new_paquet_nbre_pred = []
                new_paquet_temps_op = []
                for j in range(nbre_elements_paquet):
                    #indice du max
                    indice_maxi = liste_paquets_temps_op[i].index(max(liste_paquets_temps_op[i]))
                    #creation des paquets tries
                    new_paquet_nom.append(liste_paquets_nom[i][indice_maxi])
                    new_paquet_produit.append(liste_paquets_produit[i][indice_maxi])
                    new_paquet_temps_op.append(liste_paquets_temps_op[i][indice_maxi])
                    new_paquet_nbre_pred.append(liste_paquets_nbr_pred[i][indice_maxi])
                    #retrait des elements tries
                    liste_paquets_nom[i].pop(indice_maxi)
                    liste_paquets_produit[i].pop(indice_maxi)
                    liste_paquets_nbr_pred[i].pop(indice_maxi)
                    liste_paquets_temps_op[i].pop(indice_maxi)
                #modification dans la liste triee :
                liste_paquets_nom[i] = new_paquet_nom
                liste_paquets_produit[i] = new_paquet_produit
                liste_paquets_nbr_pred[i] = new_paquet_nbre_pred
                liste_paquets_temps_op[i] = new_paquet_temps_op

        #creation de la liste finale a partir de cette liste:
        liste_tri_nom_op = []
        liste_tri_prod = []
        liste_tri_nbre_pred = []

        for i in range(len(liste_paquets_nom)):
            liste_tri_nom_op += liste_paquets_nom[i]
            liste_tri_prod += liste_paquets_produit[i]
            liste_tri_nbre_pred += liste_paquets_nbr_pred[i]

        for i in range(len(liste_tri_nom_op)):
            nom_op = liste_tri_nom_op[i]
            produit = liste_tri_prod[i]
            nombre_predecesseurs = liste_tri_nbre_pred[i]
            liste_tri.append([nom_op,produit])

        return liste_tri


    #calcul des grandeurs utiles :
    m = nombre_de_machines
    J = len(liste_produits) #nombre de types de produits
    n = 0 #nombre d operations totale sur chaque types de produits incremente apres..

    #calcul des proportions de chaque produits:
    somme = 0
    liste_proportions = []
    for j in range(J):
        somme += liste_produits[j][1]
    for j in range(J):
        liste_proportions.append([liste_produits[j][0],liste_produits[j][1]/somme])

    #calul des LB_j (lower bound du produit j) puis du LB :
    LB = 0
    for j in range(J):
        produit = liste_produits[j][0]
        liste_op_j = produit.return_liste_operations() #liste des operations requises pour le produit j
        n_j = produit.nombre_operations_total #nombre d operations requises pour le produit j
        n += n_j # calcul du nombre total d operations pour chacun des produits
        liste_temps_op_j = []
        for k in range(n_j):
            liste_temps_op_j.append(produit.temps_travail(liste_op_j[k]))
            LB_j = max(max(liste_temps_op_j),somme_liste(liste_temps_op_j)/m)
        LB += LB_j * liste_proportions[j][1]

    nombre_de_groupes_max = 0
    liste_groupes_non_regroupes = []
    for j in range(J):
        produit = liste_produits[j][0]
        liste_groupes_j = produit.return_niveaux_predecesseurs() #[[A],[A,B]]

        #ajout information du produit a chaque operation
        for i in range(len(liste_groupes_j)):
            for op in range(len(liste_groupes_j[i])):
                liste_groupes_j[i][op] = [liste_groupes_j[i][op],produit] #[[[A,produit1]],[[A,produit1],[B,produit1]]] = liste_niveaux_produit_1
        liste_groupes_non_regroupes.append(liste_groupes_j) #[liste_niveaux_produit_1,liste...]
        if len(liste_groupes_j) > nombre_de_groupes_max:
            nombre_de_groupes_max = len(liste_groupes_j) #nombre de niveaux max

    #regroupement en [liste_niveaux_1_tous_produits_confondus,liste_niveaux_2...]
    liste_groupes = []
    for g in range(nombre_de_groupes_max):
        liste_groupes.append([])
    for j in range(J):
        for i in range(len(liste_groupes_non_regroupes[j])):
            liste_groupes[i] += liste_groupes_non_regroupes[j][i]

    #[ #niveau1: [[A,produit_1],[B,produit_2],...], #niveau 2 : [...]]

    #tri a l interieur de chacun des groupes
    for g in range(nombre_de_groupes_max):
        liste_groupes[g] = tri_groupe(liste_groupes[g])

    # Attribution aux machines :

    #Hypothèse : on regarde les operations groupe par groupe mais
    #on ne va pas assigner des op de chacun des groupes en recommencant a chaque fois
    #au poste 1 ; Les postes/machines sont remplies au fur et a mesure sans revenir
    #en arriere


    nombre_op_placees = 0
    liste_machine = [] #creation liste des machines qui recevra les operations

    for indice_machine in range(m):
        liste_machine.append([])

    ecart_old = LB #initialisation des ecarts
    ecart_new = 0 #initialisation des ecarts

    k = 0

    liste_op_a_placer = []
    for g in range(len(liste_groupes)):
        for gr in range(len(liste_groupes[g])):
            liste_op_a_placer.append(liste_groupes[g][gr])

    while len(liste_op_a_placer) !=0:
        operation = liste_op_a_placer[0]
        #copie propre de la machine originale pour creer une deuxieme version fictive
        machine_fictive = []
        for elmt_machine in range(len(liste_machine[k])):
            machine_fictive.append(liste_machine[k][elmt_machine])
        machine_fictive.append(operation) #pour test si reduit ou non l ecart
        somme_lb = 0
        for j in range(J):
            produit_lb = liste_proportions[j][0]
            w_lb = liste_proportions[j][1]
            somme_lb += w_lb*Sjk_machine(machine_fictive,produit_lb)

        ecart_new = np.abs(somme_lb-LB)
        if k == m-1 or ecart_new < ecart_old:

            liste_machine[k].append(operation)
            liste_op_a_placer.pop(0)
            ecart_old = ecart_new

        else:
            k += 1
            ecart_old = LB

    return liste_machine


#Tabu_search :
def Tabu_search(initial_solution,liste_produits,tabu_list_size,stopping_criterion,Q):
    '''ENTREE : initial_solution : [[operation_1,operation2],[operation3,...],[]] avec [op1,op2] representant la premiere machine, et operation_i = [nom_operation_i,objet_produit] ;
    tabu_size_list : nombre d operations interdites : memoire des modif precedentes pour eviter les cycles de mutations aleatoires identiques ;
    stopping_criterion : nombre d iterations max sans amelioration de la solution apres des essais successifs;
    liste des produits ;
    Q : fonction objectif/coût d une solution
    SORTIE : [[operation_1,operation2],[operation3,...],[]] avec [op1,op2] representant la premiere machine, et operation_i = [nom_operation_i,objet_produit]'''

    def liste_suppr_liste(liste_pleine,liste_elmts_suppr):
        '''ENTREE : liste_pleine : liste de depart ;
        liste_elmts_suppr = liste des elements qui, si ils sont presents dans la liste de depart, seront supprimes de la liste de depart
        SORTIE : liste_pleine transformée de maniere non destructive'''
        liste_new = []
        for i in range(len(liste_pleine)):
            liste_new.append(liste_pleine[i])
        liste_suppr = []
        for i in range(len(liste_new)):
            if appartient_liste(liste_new[i],liste_elmts_suppr):
                liste_suppr.append(liste_new[i])
        for i in range(len(liste_suppr)):
            liste_new.remove(liste_suppr[i])
        return liste_new


    best_sol = initial_solution
    current_sol = initial_solution
    Q_value_best_sol = 0 #valeur de la fonction objectif de la meilleure solution
    Q_value_current_sol = 0
    m = len(initial_solution) #nombre de machines
    J = len(liste_produits) #nombre de produits
    i = 0
    tabu_list = []

    #proportions de chaque produits :
    somme = 0
    liste_proportions = []
    for j in range(J):
        somme += liste_produits[j][1]
    for j in range(J):
        liste_proportions.append([liste_produits[j][0],liste_produits[j][1]/somme])

    #boucle principale :
    while i < stopping_criterion:
        liste_solutions_S = []
        liste_solutions_Q = []
        liste_solutions_op = []

        for j in range(J):
            # station k on which product j has the longest processing time
            product = liste_produits[j][0]
            liste_Sjk = []
            for machines in range(m):
                liste_Sjk.append(Sjk_machine(current_sol[machines],product))
            indice_machine = liste_Sjk.index(max(liste_Sjk))

            #trouver l'op a deplacer :

            #trouver toutes les operations du produit j sur la machine indice_machine :
            liste_op_machine = current_sol[indice_machine] #liste des op sur la machine k

            liste_op_machine_J = [] #liste des op du produit J sur la machine k
            for op in range(len(liste_op_machine)):
                if liste_op_machine[op][1] == product:
                    liste_op_machine_J.append(liste_op_machine[op])

            #supprimer toutes les operations presentes dans la tabu_list
            liste_op_machine_J_sans_tabu = liste_suppr_liste(liste_op_machine_J,tabu_list)

            #en choisir une restante aleatoirement (prevoir le cas y en a pas d autres)
            if len(liste_op_machine_J_sans_tabu) != 0: #si au moins une op deplacable vis a vis tabu list :
                op_choisie = liste_op_machine_J_sans_tabu[np.random.randint(0,len(liste_op_machine_J_sans_tabu))]

                #trouver le poste sur lequel deplacer :

                indice_poste_deplacement = -1 #initialisation qui permettra de verif qu elle a pu etre deplacee sur un poste

                #verifier si le poste k-1 verifie les contraintes de precedences
                #Autrement dit : verifier que aucune precedence de l op a deplacer se trouve sur k
                nom_op = op_choisie[0]
                liste_predecesseurs = product.return_tous_predecesseurs(nom_op)
                nombre_predecesseurs = len(liste_predecesseurs)
                contraintes_precedences_respectees_k_moins_1 = True
                for pred in range(nombre_predecesseurs):
                    if appartient_liste([liste_predecesseurs[pred],product],liste_op_machine_J):
                        contraintes_precedences_respectees_k_moins_1 = False
                        break

                #verifier si le poste k+1 verifie les contraintes de precedences
                #Autrement dit : verifier que l op a deplacer n est la precedence d aucune op sur k
                nom_op = op_choisie[0]
                contraintes_precedences_respectees_k_plus_1 = True
                liste_preced = []
                for check in range(len(liste_op_machine_J)):
                    liste_preced_local = []
                    op_checked = liste_op_machine_J[check]
                    product_checked = op_checked[1]
                    op_name = op_checked[0]
                    #transformation de la liste pour y rajouter le produit a nouveau:
                    liste_preced = product_checked.return_tous_predecesseurs(op_name)

                liste_preced = enleve_doublons(liste_preced)
                if appartient_liste(nom_op,liste_preced):
                    contraintes_precedences_respectees_k_plus_1 = False


                #determination de indice de changement de poste
                if contraintes_precedences_respectees_k_moins_1 and contraintes_precedences_respectees_k_plus_1 and indice_machine !=0 and indice_machine !=(m-1):

                    #calcul de la somme des Sjk*w_k pour la machine k-1 (charge de k-1)
                    charge_k_moins_1 = 0
                    for prod in range(J):
                        produit = liste_proportions[prod][0]
                        w_jk_moins_1 = liste_proportions[prod][1]
                        charge_k_moins_1 += w_jk_moins_1*Sjk_machine(current_sol[indice_machine-1],produit)

                    # calcul de la somme des Sjk*w_k pour la machine k+1 (charge de k+1)
                    charge_k_plus_1 = 0
                    for prod in range(J):
                        produit = liste_proportions[prod][0]
                        w_jk_plus_1 = liste_proportions[prod][1]
                        charge_k_plus_1 += w_jk_plus_1*Sjk_machine(current_sol[indice_machine+1],produit)

                    #Si la charge de k+1 > charge de k-1:
                    if charge_k_plus_1 > charge_k_moins_1:
                        indice_poste_deplacement = indice_machine - 1
                    else :
                        indice_poste_deplacement = indice_machine + 1

                elif contraintes_precedences_respectees_k_moins_1 and indice_machine !=0:
                    indice_poste_deplacement = indice_machine - 1

                elif contraintes_precedences_respectees_k_plus_1 and indice_machine !=m-1:
                    indice_poste_deplacement = indice_machine + 1

                #Si le deplacement a pu avoir lieu :
                if indice_poste_deplacement != -1:
                    #deplacement de l op i selectionnee random a la machine choisie (k+1 ou k-1)
                    #Attention : faire ça de manière non destructive vis a vis de la current_sol
                    #new_solution = current_sol #attention : faire un copier propre...
                    new_solution = []
                    for level_1 in range(len(current_sol)):
                        new_machine = []
                        for level_2 in range(len(current_sol[level_1])):
                            new_machine.append(current_sol[level_1][level_2])
                        new_solution.append(new_machine)

                    new_solution[indice_machine].remove(op_choisie)
                    new_solution[indice_poste_deplacement].append(op_choisie)

                    #enregistrement de la solution avec la valeur de la fonction objectif (en dehors) dans liste_solutions_S liste_solutions_Q liste_solutions_op
                    objective_value = Q(new_solution,liste_produits) #ajouter les autres paramètres necessaires
                    liste_solutions_S.append(new_solution)
                    liste_solutions_Q.append(objective_value)
                    liste_solutions_op.append(op_choisie)


        #determination de la meilleure solution :

        #trouver l'indice du minimum de liste_solutions_Q : indice de la meilleure solution dans liste_solutions_S[indice]

        if len(liste_solutions_S) != 0: #solutions a proposer
            index_best_sol = liste_solutions_Q.index(min(liste_solutions_Q))
            #Q_value_current_sol = liste_solutions_Q[indice]
            Q_value_current_sol = liste_solutions_Q[index_best_sol]
            #trouver le nom de l op deplacee avec liste_solutions_op[indice]
            op_deplace_current_sol = liste_solutions_op[index_best_sol]
            #Mettre cette op dans la tabu_list avec .append()
            tabu_list.append(op_deplace_current_sol)
            #Si la taille de la tabu list > tabu_list_size :
            if len(tabu_list) > tabu_list_size:
                #Supprimer le premier element de la tabu list (le plus ancien)
                tabu_list.pop(0)
            #Si le Q_value_current_sol < Q_value_best_sol :
            if Q_value_current_sol < Q_value_best_sol:
                Q_value_best_sol = Q_value_current_sol
                best_sol = current_sol
                i = 0 #choix : stopping criterion comme max d essais infructueux SUCCESSIFS et non global
            else:
                i = i+1
        else:
            i = i+1

    return best_sol


def equilibrage(nombre_de_machines,liste_produits):
    '''ENTREE : liste des produits : [[object produit1,quantite], [object produit2,quantite],...];
    nombre de machines/postes
    SORTIE : solution d equilibrage : [[operation_1,operation2],[operation3,...],[]] avec [op1,op2] representant la premiere machine, et operation_i = [nom_operation_i,objet_produit]'''

    #choix de parametres : (cf doc string des fonctions utilisees pour connaitre leur roles)
    tabu_list_size = 10
    stopping_criterion = 5
    Q_function = Q

    #solution initiale par algo heuristique :
    initial_solution = solution_initiale(nombre_de_machines,liste_produits)

    #nouvelle solution par algo metaheuristique :
    solution = Tabu_search(initial_solution,liste_produits,tabu_list_size,stopping_criterion,Q)
    return solution


#==================================================================================================
#==================================================================================================
##Ordonnancement :
#==================================================================================================
#==================================================================================================

#prise en compte du temps de reglage d un produit a un autre, sous forme de matrice :
#ajout d'une operation premiere qui est un reglage et de desinstallation a la fin

def Johnson(matrice):
    '''ENTREE : matrice du problème : np.array([[num_pieceA,num_pieceB,...],[t_machine1_pA,t_machine2_pA],[t_machine1_pB,...],...])
    SORTIE : ordonnancement, C_max'''

    def ordonnancement(matrice):
        '''ENTREE : matrice du problème
        SORTIE : ordonnancement'''

        def condition(liste):
            for i in range(len(liste)):
                if liste[i][1] == True:
                    return True
            return False

        def inverse(liste):
            '''ENTREE : liste
            SORTIE : liste inversee'''
            inverse = []
            n = len(liste)
            for i in range(n):
                inverse.append(liste[n-i-1])
            return inverse

        liste_1 = []
        liste_2 = []
        nbre_pieces = matrice.shape[1]
        liste_pieces = []
        for k in range(nbre_pieces):
            liste_pieces.append([matrice[0][k],True])

        k,l = 1,0
        while condition(liste_pieces):
            #minimum
            mini = np.inf
            for i in range(1,3):
                for j in range(nbre_pieces):
                    if matrice[i][j] < mini and liste_pieces[j][1]:
                        mini = matrice[i][j]
                        k,l = i,j
            if k == 1:
                liste_1.append(liste_pieces[l][0])
            else :
                liste_2.append(liste_pieces[l][0])

            liste_pieces[l][1] = False
        return liste_1 + inverse(liste_2)

    def C_max(matrice,ordre):
        nbre_pieces = len(ordre)
        matrice_travail = np.zeros(matrice.shape)
        k = 0
        for y in range(nbre_pieces):
            for j in range(nbre_pieces):
                if matrice[0][j] == ordre[k]:
                    for i in range(3):
                        matrice_travail[i][k] = matrice[i][j]

            k += 1

        c = 0
        tpsM1 = 0
        tpsM2 = 0
        for piece in range(0,nbre_pieces):
            if (matrice_travail[1][piece] + tpsM1) < tpsM2:
                tpsM1 += matrice_travail[1][piece]
                tpsM2 += matrice_travail[2][piece]
            else:
                tpsM1 += matrice_travail[1][piece]
                tpsM2 = tpsM1 + matrice_travail[2][piece]
            c = max(tpsM1,tpsM2)
        return c

    ordre = ordonnancement(matrice)
    return ordre, C_max(matrice,ordre)

def HeuristiqueJ(matrice):
    '''ENTREE : matrice du problème : np.array([[num_pieceA,num_pieceB,...],[t_machine1_pA,t_machine2_pA],[t_machine1_pB,...],...])
    SORTIE : decomposition_machines,ordre,c_max_min'''
    if matrice.shape[0] <= 3 :
        return "Erreur : méthode pour nbre_machines > 2 !"
    population = []
    nbre_machines = matrice.shape[0]-1

    for k in range(2,nbre_machines):
        paquet = [[],[],0]
        for i in range(1,k):
            paquet[0].append(i)
        for j in range(k,nbre_machines+1):
            paquet[1].append(j)
        population.append(paquet)
    for l in range(len(population)):
        #creation bonne matrice : extraire avec des matrice[1], somme direct des arrays puis np.concatenate...
        mach_eq_1 = np.zeros((1,np.shape(matrice)[1]))
        mach_eq_2 = np.zeros((1,np.shape(matrice)[1]))
        for m1 in population[l][0]:
            mach_eq_1 += matrice[m1]
        for m2 in population[l][1]:
            mach_eq_2 += matrice[m2]
        matrice_travail = np.concatenate((mach_eq_1,mach_eq_2),axis = 0)
        matrice_travail = np.concatenate(([matrice[0]],matrice_travail),axis = 0)

        #appliquer johnson[1]
        ordo,c_max = Johnson(matrice_travail)
        #renseigner le c_max pour population[l][0][2]
        population[l][2] = c_max
        population[l].append(ordo)

        #garder le meilleur c_max : phase de selection
        # algo de min

    def indice_et_mini(l):
        mini = l[0]
        indice = 0
        for j in range(1,len(l)):
            if mini>l[j]:
                mini = l[j]
                indice = j
        return mini,indice

    liste_c_max = []
    for l in range(len(population)):
        liste_c_max.append(population[l][2])
    c_max_min, indice = indice_et_mini(liste_c_max)

    decomposition_machines = population[indice][:2]
    ordre = population[indice][3]
    return decomposition_machines,ordre,c_max_min


def ordonnancement(liste_produits_seuls,solution_equilibrage):
    '''ENTREE : liste_produits_seuls : [object produit1,object produit2,...] ;
    solution d equilibrage : [[operation_1,operation2],[operation3,...],[]] avec [op1,op2] representant la premiere machine, et operation_i = [nom_operation_i,objet_produit]
    SORTIE : liste_ordonnancement : [object_product_A,object_product_B,...] le premier element de la liste est celui qui doit être réalisé en premier'''
    #reconstruction de la matrice pour HeuristiqueJ :
    m = len(solution_equilibrage) #nombre de machines
    nbr_types = len(liste_produits_seuls) #nombre de types de produits
    liste_matrices_types = []
    #calcul matrice initiales pour chaque produit :
    for product_type in range(nbr_types):
        product = liste_produits_seuls[product_type]
        matrice = np.zeros((m+1,1))
        matrice[0] = product_type
        for k in range(m):
            matrice[k+1][0] = Sjk_machine(solution_equilibrage[k],product)
        liste_matrices_types.append(matrice)

    #concatenations et creation de la matrice finale
    matrice_travail = liste_matrices_types[0]
    for i in range(1,nbr_types):
        matrice_local_product = liste_matrices_types[i]
        matrice_travail = np.concatenate((matrice_travail,matrice_local_product),axis = 1)

    #Si nombre de postes égal à 2:
    if m == 2:
        liste_ordre_produits_indices = Johnson(matrice_travail)[0]
    #Si nombre de postes supérieur à 2:
    else:
        #appel du code heuristique:
        liste_ordre_produits_indices = HeuristiqueJ(matrice_travail)[1]
#
    #reconstitution sous la forme voule en sortie:
    #retransformation en object_produits :
    liste_ordonnancement = []
    for i in range(len(liste_ordre_produits_indices)):
        liste_ordonnancement.append(liste_produits_seuls[int(liste_ordre_produits_indices[i])][0])
    return liste_ordonnancement

#==================================================================================================
#==================================================================================================
##classes:
#==================================================================================================
#==================================================================================================


class produit:
    def __init__(self,nom):
        '''ENTREE : nom du produit : type str'''
        self.nom = nom
        self.precedences = []
        self.temps_operatoires = []
        self.nombre_operations_total = 0

    def add_operation(self,nom_operation,temps_de_travail):
        '''ENTREE : nom de l operatoin nouvelle : type str, son temps requis
        FONCTION : creer une NOUVELLE operation'''
        self.temps_operatoires.append([nom_operation,temps_de_travail])
        self.precedences.append([nom_operation])
        self.nombre_operations_total += 1

    def modify_operation(self,nom_operation,temps_de_travail):
        '''ENTREE : nom de l operatoin nouvelle : type str, son temps requis
        FONCTION : modifier une operation EXISTANTE'''
        for i in range(len(self.temps_operatoires)):
            if self.temps_operatoires[i][0] == nom_operation:
                self.temps_operatoires[i][1] = temps_de_travail

    def remove_operation(self,nom_operation):
        '''ENTREE : nom de l operatoin a supprimer : type str, son temps requis
        FONCTION : retirer une operation EXISTANTE'''
        indice = 0
        for i in range(len(self.temps_operatoires)):
            if self.temps_operatoires[i][0] == nom_operation:
                indice = i
        self.temps_operatoires.pop(indice)
        for i in range(len(self.precedences)):
            if self.precedences[i][0] == nom_operation:
                indice = i
        self.precedences.pop(indice)
        self.nombre_operations_total += -1

    def return_liste_operations(self):
        liste = []
        for i in range(len(self.temps_operatoires)):
            liste.append(self.temps_operatoires[i][0])
        return liste

    def add_precedence(self,operation_principale,liste_operation_directement_precedentes):
        '''ENTREE : operation consideree ; liste des operations qui doivent être realisees juste avant : exemple A puis B puis C. L operation principale C doit etre reliee a B uniquement et non A et B car A non directement precedente
        FONCTION : realise le graphe de precedences'''
        for i in range(len(self.precedences)):
            if self.precedences[i][0] == operation_principale:
                for j in range(len(liste_operation_directement_precedentes)):
                    self.precedences[i].append(liste_operation_directement_precedentes[j])

    def remove_precedence(self,nom_operation_principale,liste_operations_precedentes_suppr):
        '''ENTREE : nom de l operatoin principale, liste des operations directement precedentes a retirer
        FONCTION : retirer des contraintes de precedence'''
        for i in range(len(self.precedences)):
            if self.precedences[i][0] == nom_operation_principale:
                for j in range(len(liste_operations_precedentes_suppr)):
                    self.precedences[i].remove(liste_operations_precedentes_suppr[j])

    def temps_travail(self,nom_operation):
        '''ENTREE : nom du produit : type str, nom de l op
        SORTIE : temps de travail de l operation nommee'''
        for i in range(len(self.temps_operatoires)):
            if self.temps_operatoires[i][0] == nom_operation:
                return self.temps_operatoires[i][1]

    def return_direct_predecesseurs(self,nom_operation):
        '''ENTREE : nom du produit : type str
        SORTIE : liste des predecesseurs directs'''
        for i in range(len(self.precedences)):
            if self.precedences[i][0] == nom_operation:
                return(self.precedences[i][1:])

    def return_direct_successeurs(self,nom_operation):
        '''ENTREE : nom du produit : type str
        SORTIE : liste successeurs directs'''
        liste_successeurs = []
        for i in range(len(self.precedences)):
            operation = self.precedences[i]
            if appartient_liste(nom_operation,operation[1:]):
                liste_successeurs.append(operation[0])
        return liste_successeurs

    def return_tous_predecesseurs(self,nom_operation):
        '''ENTREE : nom du produit : type str
        SORTIE : liste de tous predecesseurs (graphe complet)'''
        def iterative(product,nom_operation):
            '''ENTREE : nom du produit : type str
            SORTIE : liste de tous predecesseurs (graphe complet) mais avec doublons'''
            liste_total = [nom_operation]
            liste_predecesseurs = product.return_direct_predecesseurs(nom_operation)
            if liste_predecesseurs == []:
                return liste_total
            else:
                for i in range(len(liste_predecesseurs)):
                    liste_total += iterative(product,liste_predecesseurs[i])
            return liste_total
        liste_pred = enleve_doublons(iterative(self,nom_operation))
        return liste_pred[1:]

    def return_tous_successeurs(self,nom_operation):
        '''ENTREE : nom du produit : type str
        SORTIE : liste de tous successeurs (graphe complet)'''
        def iterative(product,nom_operation):
            '''ENTREE : nom du produit : type str
            SORTIE : liste de tous successeurs (graphe complet) mais avec doublons'''
            liste_total = [nom_operation]
            liste_successeurs = product.return_direct_successeurs(nom_operation)
            if liste_successeurs == []:
                return liste_total
            else:
                for i in range(len(liste_successeurs)):
                    liste_total += iterative(product,liste_successeurs[i])
            return liste_total
        liste_succ = enleve_doublons(iterative(self,nom_operation))
        return liste_succ[1:]

    def return_niveaux_predecesseurs(self):
        '''ENTREE : produit
        SORTIE : niveau de predecesseurs : op A puis B et C puis D :
        [[A],[B,C],[D]]'''
        n = self.nombre_operations()
        op_placees = 0
        liste_op = self.return_liste_operations() #liste des operations sans temps operatoire
        liste_op_placees = []
        liste_niveaux = []
        while len(liste_op) != 0:
            niveau_courant = []
            for i in range(len(liste_op)):
                liste_predecesseurs = self.return_direct_predecesseurs(liste_op[i]) #predecesseurs
                if liste_appartient_liste(liste_predecesseurs,liste_op_placees):
                    niveau_courant.append(liste_op[i])

            liste_niveaux.append(niveau_courant)
            liste_op_placees += niveau_courant
            for i in range(len(niveau_courant)):
                liste_op.remove(niveau_courant[i])
        return liste_niveaux

    def nombre_operations(self):
        return self.nombre_operations_total


##import:
import simpy
import numpy as np
#idees de façon de coder :
#les produits sont pris par les machines entre deux stocks de type Store
#Il veulent prendre le produit d'un stock, attendre le temps de travail puis mettre le produit dans un autre store qui est le stock suivant

#la simulation commence par mettre tous les objets dans le store de debut de ligne
#Puis chacune des machine est appellee dans un while True (jusqu'à ce que tous les produits soient passes sur la ligne)


##utilitaires
def moyenne(liste):
    somme = 0
    n = len(liste)
    for i in range(n):
        somme += liste[i]
    return somme/n

def inverse_liste(liste):
    liste_inverse = []
    n = len(liste)
    for i in range(n):
        liste_inverse.append(liste[n-i-1])
    return liste_inverse

def tri(liste_elmts,decroissant = False):
    '''ENTREE : liste non triee
    SORTIE : liste triee par ordre decroissant ou croissant par defaut ; liste des indices de depart correspondant'''
    n = len(liste_elmts)
    #copie de la liste initiale pour non destruction :
    liste_elmts_copie = []
    liste_elmts_copie_avec_indices = []
    for i in range(n):
        liste_elmts_copie.append(liste_elmts[i])
        liste_elmts_copie_avec_indices.append([liste_elmts[i],i])
    #tri croissant :
    liste_triee_indices_et_elmts = []
    for i in range(n):
        mini = min(liste_elmts_copie)
        indice_mini = liste_elmts_copie.index(mini)
        liste_triee_indices_et_elmts.append(liste_elmts_copie_avec_indices[indice_mini])
        liste_elmts_copie_avec_indices.pop(indice_mini)
        liste_elmts_copie.pop(indice_mini)

    #reconstitution des listes:
    liste_triee,liste_indices_triee = [],[]
    for i in range(n):
        liste_triee.append(liste_triee_indices_et_elmts[i][0])
        liste_indices_triee.append(liste_triee_indices_et_elmts[i][1])

    #retourne la liste si decroissant demandé
    if not(decroissant):
        return liste_triee,liste_indices_triee
    else:
        return inverse_liste(liste_triee),inverse_liste(liste_indices_triee)

##classes et fonctions :
class machine:
    def __init__(self,env,buffer_in,buffer_out,indice,matrice_definition):
        self.env = env
        self.indice = indice
        self.buffer_in = buffer_in
        self.buffer_out = buffer_out
        self.turned_on = False
        self.matrice_definition = matrice_definition
        self.indice_produit_passe = -1

    def turn_on(self):
        self.env.process(self.produce())
        self.turned_on = True

    def produce(self):
        while self.turned_on: #tant que machine allumée
            #prise de l elmt dans le buffer d entree :
            part = yield self.buffer_in.get() #element du stock tampon vers la machine

            self.indice_produit_passe += 1 #nouveau produit entre sur la machine
            #calculs des indices correspondant pour end_times_product :
            indice_produit = self.indice_produit_passe #indice du produit
            indice_buffer_in_dans_end_times = 2*self.indice+1 #buffer in
            indice_machine_dans_end_times = 2*self.indice+2 #machine
            indice_buffer_out_dans_end_times = 2*self.indice+3 #buffer out

            end_times_products[indice_produit][indice_buffer_in_dans_end_times][1] = env.now #enregistrement

            #traitement de l elmt par le poste
            time_wait = time_on_machine_from_product(self.matrice_definition,self.indice,part)
            end_times_products[indice_produit][indice_machine_dans_end_times][0] = env.now #tps entree sur poste

            yield self.env.timeout(time_wait)

            end_times_products[indice_produit][indice_machine_dans_end_times][1] = env.now #tps fin traitement

            #mise de l elmt dans le buffer de sortie :
            yield self.buffer_out.put(part)#element de la machine vers le stock tampon
            end_times_products[indice_produit][indice_machine_dans_end_times][2] = env.now #tps sortie sur poste
            end_times_products[indice_produit][indice_buffer_out_dans_end_times][0] = env.now #tps entree buffer out


            #condition evenement de fin de produit :
            if end_times_products[-1][-1][0] !=0: #veut dire que dernier produit a enregistre une entree dans le buffer de sortie
                end_event.succeed()


class line:
    def __init__(self):
        self.liste_machines = []

    def add_machine(self,machine_object):
        self.liste_machines.append(machine_object)

    def turn_on_the_line(self):
        for i in range(len(self.liste_machines)):
            self.liste_machines[i].turn_on()


#pour garder la dernière simulation en memoire :
end_times_products = []

#end_times_products : [liste_produit_A_1,liste_produit_A_2,...,liste_produit_B_1,...]
#avec liste_produit : [object_produit_correspondant,[temps_entree_buffer_1,temps_sortie_buffer_1],[temps_entree_poste_1,temps_fin_traitement,temps_sortie_poste_1],[temps_entree_buffer_2,temps_sortie_buffer_2],...]



#creation environnement
env = simpy.Environment()

 #arret de la simulation quand plus de produit à passer sur la ligne

def auto_simulation(solution_equilibrage,liste_produits,ordonnancement,liste_buffers_sizes = "auto"):
    '''ENTREE : donnes provenant des algos (sauf si modif manuelle), liste des tailles des buffers entre le buffer d'appro, chaque machines et le buffer de sortie de ligne. "auto" : buffer infini, sinon contenance (tout type),"ones" : buffer de taille maximale de 1 entre chacune des machines
    SORTIE : liste_sortie : [liste_produit_A_1,liste_produit_A_2,...,liste_produit_B_1,...]
    avec liste_produit : [object_produit_correspondant,[temps_entree_poste_1,temps_sortie_poste_1],[temps_entree_poste_2,temps_sortie_poste_2],...] '''

    global end_event
    end_event = env.event()

    #donnes
    nbre_machines = len(solution_equilibrage)

    #seed random:
    random_seed = 342
    np.random.seed(random_seed)

    #creation de la ligne
    simu_line = line()

    #creation matrice_definition :
    simu_matrice_definition = matrice_definition(solution_equilibrage,liste_produits)

    #creation des buffers :
    if liste_buffers_sizes == "auto":
        liste_buffers_sizes = []
        for i in range(nbre_machines-1): #nbre_machines -1 = nombre de buffers != start et end
            liste_buffers_sizes.append(-1)
    elif liste_buffers_sizes == "ones":
        liste_buffers_sizes = []
        for i in range(nbre_machines-1): #nbre_machines -1 = nombre de buffers != start et end
            liste_buffers_sizes.append(1)

    buffer_start = simpy.Store(env)
    buffer_end = simpy.Store(env)

    liste_buffers = [buffer_start]

    for i in range(len(liste_buffers_sizes)):
        value_storage = liste_buffers_sizes[i]
        if  value_storage == -1:
            liste_buffers.append(simpy.Store(env))
        else:
            liste_buffers.append(simpy.Store(env,value_storage))

    liste_buffers.append(buffer_end)

    #creation des machines et ajout des objets :
    for i in range(nbre_machines):
        simu_line.add_machine(machine(env,liste_buffers[i],liste_buffers[i+1],i,simu_matrice_definition))

    #remplissage du buffer de depart avec ordonnancement :
    #definition de la liste des produits decomposée  [A,A,A,B,B,C,C,D,D,D,D,D,D,D,...]:
    liste_produits_sur_ligne = []
    for i in range(len(ordonnancement)):
        product = ordonnancement[i]

        nbr_of_products_by_type = 0

        for k in range(len(liste_produits)):
            if product == liste_produits[k][0]:
                nbr_of_products_by_type = liste_produits[k][1]
                break

        for j in range(nbr_of_products_by_type):
            liste_produits_sur_ligne.append(product)

    for i in range(len(liste_produits_sur_ligne)):
        buffer_start.put(liste_produits_sur_ligne[i])

    #vide la liste des temps qui est une memoire globale
    end_times_products.clear()

    #remplissage de la matrice end_times avec les produits et les listes qui seront remplies:

    for i in range(len(liste_produits_sur_ligne)):
        end_times_products.append([liste_produits_sur_ligne[i]])
        for m in range(2*nbre_machines+1):  #nbre _machines + buffers = nb_mach*2+1
            end_times_products[i].append([0,0,0]) #ajout temps entree sortie sur chaque poste + buffers

    #lancement de la simulation :
    simu_line.turn_on_the_line()
    env.run()

    return

def matrice_definition(solution_equilibrage,liste_produits):
    '''ENTREE : solution d equilibrage, liste des produits
    SORTIE : matrice_definition : np.array([[op_produit_A,op_produit_B,...],[[op_produit_A,op_produit_B,...],...] : une ligne par machine avec op_produit_A = [object_product_A,mu,sigma = 0 par defaut si pas connu] '''
    nbre_machines = len(solution_equilibrage)
    nbre_produits = len(liste_produits)
    matrice_sortie = []
    for m in range(nbre_machines): #on crée les lignes
        matrice_sortie.append([])
    #RQ.: on va mettre à 0 le temps de travail d une machine sur un produit si le produit n utilise pas la machine
    for m in range(nbre_machines):
        for p in range(nbre_produits): #on crée les colonnes
            matrice_sortie[m].append([liste_produits[p][0],0]) #[object_produit,mu,sigma]
    #regarde chacune des op et fait la sommation pour chaque machine des mu et sigma pour chaque produit :
    for m in range(nbre_machines):
        for op in range(len(solution_equilibrage[m])):
            nom_op,object_produit = solution_equilibrage[m][op][0],solution_equilibrage[m][op][1]
            mu_op = object_produit.temps_travail(nom_op)
            #recherche de la colonne correspondante :
            for p in range(nbre_produits):
                if matrice_sortie[m][p][0] == object_produit:
                    #addition des moyennes :
                    matrice_sortie[m][p][1] += mu_op
    return matrice_sortie

def time_on_machine_from_product(matrice_definition,indice_machine,object_produit):
    '''ENTREE : matrice_definition, indice de la machine dans la sol d equilibrage, obejct produit utilise
    SORTIE : temps passe avec aleatoire pris en compte ici'''
    for j in range(len(matrice_definition[indice_machine])):
        if matrice_definition[indice_machine][j][0] == object_produit:
            mu = matrice_definition[indice_machine][j][1]
            if mu == 0: #pas d op a realiser sur ce poste pour ce produit
                time_waiting = 0
            else:
                time_waiting = np.random.normal(mu) #loi exponentielle en avec lambda = 1/E(X) = 1/mu
    return time_waiting


##Indicateurs et donnees
def temps_production_total():
    '''SORTIE : temps total de production pour realiser tous les produits desires'''
    return end_times_products[-1][-1][0]

def occupation_postes(decroissant = False):
    '''ENTREE : si ordre croissant ou decroissant
    SORTIE : [[numero_du_poste,temps_occupation],[...,...],...]'''

    #reperer les indices des postes pour acces rapide apres
    liste_indices_postes_dans_listes = []

    nombre_de_postes = int((len(end_times_products[0])-2)/2)
    for i in range(nombre_de_postes):
        liste_indices_postes_dans_listes.append(2*i+2)

    #creation liste occupations postes non triee + liste des indices
    liste_occupations = []
    for m in liste_indices_postes_dans_listes:
        temps_travail= 0
        temps_prod_total= temps_production_total()
        for p in range(len(end_times_products)):
            temps_travail += end_times_products[p][m][1]-end_times_products[p][m][0]#a coder
        liste_occupations.append(temps_travail/temps_prod_total)

    #tri
    liste_occupations_triee,liste_indices = tri(liste_occupations,decroissant)
    #reconstitution liste sortie voulue
    liste_sortie = []
    for i in range(nombre_de_postes):
        liste_sortie.append([liste_indices[i]+1,liste_occupations_triee[i]])
    return liste_sortie


def lead_time_produit(object_produit):
    '''ENTREE : liste_sortie provenant du main, object produit considéré (type de produit)
    SORTIE : lead time moyen du type de produit sur le run'''
    liste_lead_time = []
    #Pour chacune des listes de produits qui correspondent à ce produit:
    for i in range(len(end_times_products)):
        if end_times_products[i][0] == object_produit:
            lead_time_i = end_times_products[i][-1][0]- end_times_products[i][1][1]
            liste_lead_time.append(lead_time_i) #enregistrer le lead_time dans une liste
    #renvoyer la valeur moyenne de cette liste
    return moyenne(liste_lead_time)


def TRS_theorique(production_rate): #a toujours du sens ?
    '''ENTREE : production_rate : nombre de pieces bonnes produites en moyenne
    SORTIE : le TRS theorique correspondant a la simulation'''
    #theoriquement proche de 1 si le production_rate est à jour et cohérent
    nbre_pieces = len(end_times_products)
    duree = temps_production_total()
    return nbre_pieces*duree/production_rate

def cadence_ligne():
    '''SORTIE : cadence de la ligne en moyenne sur le run tous produits consideres [tps/produit]'''
    return temps_production_total()/len(end_times_products)



##main_test :

#creation du produit A1
A1 = produit("A1")

#ajout des operations
A1.add_operation("prepose_2_vis_chapeau_1er",9.34)
A1.add_operation("prepose_2_vis_chapeau_2e",9.34)
A1.add_operation("visser_1_vis_1er_sur_chapeau_1er",4.4)
A1.add_operation("visser_1_vis_2e_sur_chapeau_1er",4.4)
A1.add_operation("visser_1_vis_1er_sur_chapeau_2e",4.4)
A1.add_operation("visser_1_vis_2e_sur_chapeau_2e",4.4)

A1.add_operation("piston_dans_chapeau",4.05)
A1.add_operation("piston_chapeau_dans_corps",5.65)
A1.add_operation("preposer_1_valve_1er_sur_corps",5.92)
A1.add_operation("serrer_1_valve_1er_cle",3)
A1.add_operation("preposer_1_valve_2e_sur_corps",5.92)
A1.add_operation("serrer_1_valve_2e_cle",3)
A1.add_operation("mettre_truc_blanc_sur_fil",6.67)
A1.add_operation("installer_fil",8.75)
A1.add_operation("mettre_ekr_1er_preposer_vis",13.95)
A1.add_operation("mettre_ekr_2e_preposer_vis",13.95)
A1.add_operation("visser_1_vis_1er_ekr_1er",4.3)
A1.add_operation("visser_1_vis_2e_ekr_1er",4.3)
A1.add_operation("visser_1_vis_1er_ekr_2e",4.3)
A1.add_operation("visser_1_vis_2e_ekr_2e",4.3)
A1.add_operation("ecrou_sur_tige",6.81)
A1.add_operation("chape_sur_tige",7.11)
A1.add_operation("clipser_bout_sur_chape",6.49)
A1.add_operation("serrage_bout_sur_chape",4.98)

#ajout des precedences entre operations
A1.add_precedence("chape_sur_tige",["ecrou_sur_tige"])

A1.add_precedence("visser_1_vis_1er_ekr_1er",["mettre_ekr_1er_preposer_vis"])
A1.add_precedence("visser_1_vis_2e_ekr_1er",["visser_1_vis_1er_ekr_1er"])

A1.add_precedence("visser_1_vis_1er_ekr_2e",["mettre_ekr_2e_preposer_vis"])
A1.add_precedence("visser_1_vis_2e_ekr_2e",["visser_1_vis_1er_ekr_2e"])

A1.add_precedence("installer_fil",["visser_1_vis_1er_ekr_2e"])

A1.add_precedence("serrage_bout_sur_chape",["clipser_bout_sur_chape"])

A1.add_precedence("serrer_1_valve_1er_cle",["preposer_1_valve_1er_sur_corps"])
A1.add_precedence("serrer_1_valve_2e_cle",["preposer_1_valve_2e_sur_corps"])

A1.add_precedence("piston_chapeau_dans_corps",["piston_dans_chapeau"])

A1.add_precedence("visser_1_vis_1er_sur_chapeau_1er",["prepose_2_vis_chapeau_1er"])
A1.add_precedence("visser_1_vis_2e_sur_chapeau_1er",["visser_1_vis_1er_sur_chapeau_1er"])
A1.add_precedence("prepose_2_vis_chapeau_1er",["piston_chapeau_dans_corps"])

A1.add_precedence("visser_1_vis_1er_sur_chapeau_2e",["prepose_2_vis_chapeau_2e"])
A1.add_precedence("visser_1_vis_2e_sur_chapeau_2e",["visser_1_vis_1er_sur_chapeau_2e"])


#creation du produit B0
B0 = produit("B0")

#ajout des operations
B0.add_operation("prepose_2_vis_chapeau_1er",9.34)
B0.add_operation("prepose_2_vis_chapeau_2e",9.34)
B0.add_operation("visser_1_vis_1er_sur_chapeau_1er",4.4)
B0.add_operation("visser_1_vis_2e_sur_chapeau_1er",4.4)
B0.add_operation("visser_1_vis_1er_sur_chapeau_2e",4.4)
B0.add_operation("visser_1_vis_2e_sur_chapeau_2e",4.4)

B0.add_operation("dromadaire_prepose_4_vis",27.20)
B0.add_operation("serrage_vis_1_dromadaire",4.32)
B0.add_operation("serrage_vis_2_dromadaire",4.32)
B0.add_operation("serrage_vis_3_dromadaire",4.32)
B0.add_operation("serrage_vis_4_dromadaire",4.32)

B0.add_operation("piston_dans_chapeau",4.05)
B0.add_operation("piston_chapeau_dans_corps",5.65)
B0.add_operation("preposer_1_valve_1er_sur_corps",5.92)
B0.add_operation("serrer_1_valve_1er_cle",3)
B0.add_operation("preposer_1_valve_2e_sur_corps",5.92)
B0.add_operation("serrer_1_valve_2e_cle",3)

B0.add_operation("ecrou_sur_tige",6.81)
B0.add_operation("chape_sur_tige",7.11)
B0.add_operation("clipser_bout_sur_chape",6.49)
B0.add_operation("serrage_bout_sur_chape",4.98)

#ajout des precedences entre operations
B0.add_precedence("chape_sur_tige",["ecrou_sur_tige"])
B0.add_precedence("serrage_bout_sur_chape",["clipser_bout_sur_chape"])

B0.add_precedence("serrer_1_valve_1er_cle",["preposer_1_valve_1er_sur_corps"])
B0.add_precedence("serrer_1_valve_2e_cle",["preposer_1_valve_2e_sur_corps"])

B0.add_precedence("piston_chapeau_dans_corps",["piston_dans_chapeau"])

B0.add_precedence("visser_1_vis_1er_sur_chapeau_1er",["prepose_2_vis_chapeau_1er"])
B0.add_precedence("visser_1_vis_2e_sur_chapeau_1er",["visser_1_vis_1er_sur_chapeau_1er"])
B0.add_precedence("prepose_2_vis_chapeau_1er",["piston_chapeau_dans_corps"])

B0.add_precedence("visser_1_vis_1er_sur_chapeau_2e",["prepose_2_vis_chapeau_2e"])
B0.add_precedence("visser_1_vis_2e_sur_chapeau_2e",["visser_1_vis_1er_sur_chapeau_2e"])

B0.add_precedence("serrage_vis_1_dromadaire",["dromadaire_prepose_4_vis"])
B0.add_precedence("serrage_vis_2_dromadaire",["serrage_vis_1_dromadaire"])
B0.add_precedence("serrage_vis_3_dromadaire",["serrage_vis_2_dromadaire"])
B0.add_precedence("serrage_vis_4_dromadaire",["serrage_vis_3_dromadaire"])




#creation du produit B6
B6 = produit("B6")

#ajout des operations
B6.add_operation("prepose_2_vis_chapeau_1er",9.34)
B6.add_operation("prepose_2_vis_chapeau_2e",9.34)
B6.add_operation("visser_1_vis_1er_sur_chapeau_1er",4.4)
B6.add_operation("visser_1_vis_2e_sur_chapeau_1er",4.4)
B6.add_operation("visser_1_vis_1er_sur_chapeau_2e",4.4)
B6.add_operation("visser_1_vis_2e_sur_chapeau_2e",4.4)

B6.add_operation("dromadaire_prepose_4_vis",27.20)
B6.add_operation("serrage_vis_1_dromadaire",4.32)
B6.add_operation("serrage_vis_2_dromadaire",4.32)
B6.add_operation("serrage_vis_3_dromadaire",4.32)
B6.add_operation("serrage_vis_4_dromadaire",4.32)

B6.add_operation("piston_dans_chapeau",4.05)
B6.add_operation("piston_chapeau_dans_corps",5.65)
B6.add_operation("preposer_1_valve_1er_sur_corps",5.92)
B6.add_operation("serrer_1_valve_1er_cle",3)
B6.add_operation("preposer_1_valve_2e_sur_corps",5.92)
B6.add_operation("serrer_1_valve_2e_cle",3)

B6.add_operation("ecrou_sur_tige",6.81)
B6.add_operation("chape_sur_tige",7.11)
B6.add_operation("clipser_bout_sur_chape",6.49)
B6.add_operation("serrage_bout_sur_chape",4.98)


B6.add_operation("chameau_tige",8.19)
B6.add_operation("cercles_sur_tige_chameau",12.78)


#ajout des precedences entre operations
B6.add_precedence("chape_sur_tige",["ecrou_sur_tige"])
B6.add_precedence("serrage_bout_sur_chape",["clipser_bout_sur_chape"])

B6.add_precedence("serrer_1_valve_1er_cle",["preposer_1_valve_1er_sur_corps"])
B6.add_precedence("serrer_1_valve_2e_cle",["preposer_1_valve_2e_sur_corps"])

B6.add_precedence("piston_chapeau_dans_corps",["piston_dans_chapeau"])

B6.add_precedence("visser_1_vis_1er_sur_chapeau_1er",["prepose_2_vis_chapeau_1er"])
B6.add_precedence("visser_1_vis_2e_sur_chapeau_1er",["visser_1_vis_1er_sur_chapeau_1er"])
B6.add_precedence("prepose_2_vis_chapeau_1er",["piston_chapeau_dans_corps"])

B6.add_precedence("visser_1_vis_1er_sur_chapeau_2e",["prepose_2_vis_chapeau_2e"])
B6.add_precedence("visser_1_vis_2e_sur_chapeau_2e",["visser_1_vis_1er_sur_chapeau_2e"])

B6.add_precedence("serrage_vis_1_dromadaire",["dromadaire_prepose_4_vis"])
B6.add_precedence("serrage_vis_2_dromadaire",["serrage_vis_1_dromadaire"])
B6.add_precedence("serrage_vis_3_dromadaire",["serrage_vis_2_dromadaire"])
B6.add_precedence("serrage_vis_4_dromadaire",["serrage_vis_3_dromadaire"])

B6.add_precedence("chameau_tige",["serrage_vis_4_dromadaire"])
B6.add_precedence("cercles_sur_tige_chameau",["chameau_tige"])


#tests:
nombre_de_postes_choisi = 0
liste_produits = []

#calculs:
#equilibrage_test = equilibrage(nombre_de_postes_choisi,liste_produits)
#ordonnancement_test = ordonnancement(liste_produits,equilibrage_test)

#auto_simulation(equilibrage_test,liste_produits,ordonnancement_test,"ones")

#resultats:
#print("\nequilibrage:\n"+str(equilibrage_test))
#print("\nordonnancement:\n"+str(ordonnancement_test))
#print("\ntemps_production_total:\n"+str(temps_production_total()))
#print("\noccupations_des_postes:\n"+str(occupation_postes(True))) #true pour ordre decroissant
#print("\nlead_time_produit_A1:\n"+str(lead_time_produit(A1)))
#print("\ncadence_moyenne_ligne:\n"+str(cadence_ligne()))
def texte_equilibrage(liste_equilibrage):
    '''ENTREE : equilibrage sortant d un algo
    SORTIE : liste de versions textes de l equilibrage exploitables par un operateur:
    [texte_poste_1,texte_poste_2,...] '''
    nombre_de_postes = len(liste_equilibrage)
    liste_sortie = []
    #recherche du nombre de produits differents existant
    liste_produits_found = [] #liste des objets produits
    for i in range(nombre_de_postes):
        for j in range(len(liste_equilibrage[i])): #operations
            if not(appartient_liste(liste_equilibrage[i][j][1],liste_produits_found)):
                liste_produits_found.append(liste_equilibrage[i][j][1])
    #pour chacun des postes
    for i in range(nombre_de_postes):
        #creation des textes pour tous les produits :
        texte_i = ["" for k in range(len(liste_produits_found))]
        for j in range(len(liste_equilibrage[i])): #operations
            #recherche du produit associé:
            for l in range(len(liste_produits_found)):
                if liste_equilibrage[i][j][1] == liste_produits_found[l]:
                    texte_i[l]+="- "+liste_equilibrage[i][j][0]+"\n"
        #retravail en ajoutant les noms des produits:
        texte_final_i = "\nEquilibrage du poste "+str(i+1)+":\n"
        for m in range(len(texte_i)):
            if texte_i[m] != "": #si il y a des operations sur le produit:
                texte_final_i += "\nProduit " + liste_produits_found[m].nom + ":\n"
                texte_final_i += texte_i[m]
        liste_sortie.append(texte_final_i)
    return liste_sortie


def texte_ordonnancement(ordonnancement):
    '''ENTREE : ordonnancement sortant d un algo
    SORTIE : liste de versions textes de l ordonnancement exploitables par un operateur: A1->B1->B2->B3 ...'''
    texte_resultat = "\nOrdonnancement:\n\n"
    for i in range(len(ordonnancement)):
        if i != 0:
            texte_resultat += "->"
        texte_resultat += ordonnancement[i].nom
    return texte_resultat
##Interface

import tkinter
import tkinter.ttk as ttk
import xlrd
import xlwt
import xlutils.copy
from PIL import Image
from PIL import ImageTk


Lprod = ["A1", "B0", "B6"] #Liste avec l'ensemble des produits fabriqués

root = tkinter.Tk() #création de la fenêtre pour l'interface

# canvas= tkinter.Canvas(root)
# canvas.pack(fill='both',expand = True)
#
# bg=tkinter.PhotoImage(file="C:\\Users\\quent\\OneDrive\\Images\\ENSAM.gif")
# canvas.create_image(0,0, image=bg,anchor="nw")


c = tkinter.Label(root, text = "Nombre de poste") #Insertion d'une question en haut de la fenêtre
c.pack()


s2 = ttk.Spinbox(root, from_=0, to=np.inf) #On crée un menu déroulant contenant les nombres de 0 jusqu'au nombre de produits fabriqués sur la chaine de prod. L'objectif est de répondre à la question ci-dessus.
s2.insert(0,2) #on impose une condition initiale de 1 produit minimum sur la chaine de prod
s2.pack()

nbposte=s2.get()

espace= tkinter.Label(root, text="        ") #on crée un espace pour une meilleure lisibilité de l'interface
espace.pack()

c = tkinter.Label(root, text = "Choisir le nombre de produit sur la chaîne de production") #Insertion d'une question en haut de la fenêtre
c.pack()


s = ttk.Spinbox(root, from_=0, to=len(Lprod)) #On crée un menu déroulant contenant les nombres de 0 jusqu'au nombre de produits fabriqués sur la chaine de prod. L'objectif est de répondre à la question ci-dessus.
s.insert(0,0) #on impose une condition initiale de 1 produit minimum sur la chaine de prod
s.pack()
nbprod=s.get() #on récupère le nombre de produits fabriqués choisi par l'utilisateur


espace= tkinter.Label(root, text="        ") #on crée un espace pour une meilleure lisibilité de l'interface
espace.pack()



i=10 #nombre de bouton, pour ne pas qu'ils se suppriment lors de l'update

liste_fenetres = []
def update():   #fonction qui permet de faire une mise à jour de l'interface après le choix de l'utilisateur
    liste_fenetres.clear()
    label.pack()
    nbprod=s.get()
    L=root.winfo_children() #liste des widgets qu'il y a dans la fenêtre
    prod_qt=[] #création d'une liste qui contiendra la quantite de produits fabriqués selon leur type
    if len(L)>i:
        for w in range (len(L)-(i)):
            L[len(L)-1].destroy() #on supprime les anciens éléments de la page pour les remplacer par les nouveaux
            L.pop(len(L)-1)
    for k in range (int(nbprod)):
        o = ttk.Combobox(root, values=Lprod) #création d'un menu déroulant avec la liste des produits
        o.pack ()
        b = tkinter.Label (root, text = "Produit "+ str(k+1)) #numérotation des produits
        b.pack ()
        a = ttk.Entry(root) #création d'un widget où l'utilisateur écrit ce qu'il veut
        a.pack ()
        c = tkinter.Label (root, text = "Quantité " )
        c.pack ()
        espace= tkinter.Label(root, text="        ")
        espace.pack()
        liste_fenetres.append([o,a])



liste_resultat =[]
def fenetre2():
    liste_produits.clear()
    liste_resultat.clear()

    for i in range(len(liste_fenetres)):
        product_name,qtt = liste_fenetres[i][0].get(),liste_fenetres[i][1].get()
        if product_name == "A1":
            liste_produits.append([A1,int(qtt)])
        elif product_name == "B0":
            liste_produits.append([B0,int(qtt)])
        elif product_name == "B6":
            liste_produits.append([B6,int(qtt)])

    nbposte=int(s2.get())
    equilibrage_test = equilibrage(nbposte,liste_produits)
    ordonnancement_test = ordonnancement(liste_produits, equilibrage_test)
    auto_simulation(equilibrage_test,liste_produits,ordonnancement_test,"auto")

    liste_resultat.append(equilibrage_test)
    liste_resultat.append(ordonnancement_test)

    win = tkinter.Toplevel(root) #crée une deuxième fenêtre en plus de la première
    boutonequi=tkinter.Button(win, text="Equilibrage", command=fenetreposte)
    boutonequi.pack()

    espace= tkinter.Label(win, text="        ") #on crée un espace pour une meilleure lisibilité de l'interface
    espace.pack()

    boutonordo=tkinter.Button(win, text="Ordonnancement",command=fenetreordo)
    boutonordo.pack()

    espace= tkinter.Label(win, text="        ") #on crée un espace pour une meilleure lisibilité de l'interface
    espace.pack()

    boutonsimu=tkinter.Button(win, text="Simulation",command=fenetresimu)
    boutonsimu.pack()

    exit_button = tkinter.Button(win, text="Exit", command=win.destroy)
    exit_button.pack(pady=20)

def fenetreposte():
    win2=tkinter.Toplevel(root)
    win2.geometry("3000x4000")

    liste_text_affiche = []
    liste_text_equi = texte_equilibrage(liste_resultat[0])
    for i in range(len(liste_text_equi)):
        liste_local_text_affiche = liste_text_equi[i].split("\n")
        for j in range(len(liste_local_text_affiche)):
            liste_text_affiche.append(liste_local_text_affiche[j])

    scrollbar=tkinter.Scrollbar(win2,width=30)
    scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    mylist = tkinter.Listbox(win2, yscrollcommand = scrollbar.set,width=200, justify=tkinter.CENTER)
    for line in range (len(liste_text_affiche)):
        mylist.insert(tkinter.END,liste_text_affiche[line])

    mylist.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
    scrollbar.config(command=mylist.yview)
    exit_button = tkinter.Button(win2, text="Exit",width=30,height =5, command=win2.destroy)
    exit_button.pack(pady=100)



def fenetreordo():
    win3=tkinter.Toplevel(root)
    win3.geometry("1000x200")

    text_affiche = texte_ordonnancement(liste_resultat[1])
    q= tkinter.Label(win3, text = text_affiche)
    q.pack()
    exit_button = tkinter.Button(win3, text="Exit", command=win3.destroy)
    exit_button.pack(pady=20)

def fenetresimu():
    win4=tkinter.Toplevel(root)
    win4.geometry("1000x400")

    text_affiche = "Resultats de la simulation:\nTemps de production total: "
    text_affiche += str(temps_production_total()) + " s"
    text_affiche += "\nOccupation des postes: "+str(occupation_postes())
    text_affiche += "\nCadence moyenne de la ligne "+str(cadence_ligne())+" s/produit"
    text_affiche += "\nLead Time moyen du produit:"
    for i in range(len(liste_produits)):
        text_affiche += "\n- "+liste_produits[i][0].nom +": "+str(lead_time_produit(liste_produits[i][0]))+" s"
    q= tkinter.Label(win4, text = text_affiche)
    q.pack()
    exit_button = tkinter.Button(win4, text="Exit", command=win4.destroy)
    exit_button.pack(pady=20)

# def fenetreposte():
#
#     nbposte=s2.get()
#     win2=tkinter.Toplevel(root)
#     for i in range(int(nbposte)):
#         tkinter.Button(win2, text = "Poste" +str(i+1),command = listeoperation(i+1)).pack()
#         espace= tkinter.Label(win2, text="        ") #on crée un espace pour une meilleure lisibilité de l'interface
#         espace.pack()

# def listeoperation(k):
#     win3=tkinter.Toplevel(root)
#     texte = str(k)
#     q= tkinter.Label(win3, text = texte)
#     q.pack()



def Close():
    root.destroy()

button = tkinter.Button(text='Rafraichir',command=update) #bouton de commande pour mettre à jour l'interface
button.pack()

btn = tkinter.Button(root, text="Confirmer", command = fenetre2) #bouton pour confirmer l'insertion
btn.pack(pady = 10)

exit_button = tkinter.Button(root, text="Exit",bg="red", command=Close)
exit_button.pack(pady=20)

label = tkinter.Label(text='')

prod_qt=update()


root.mainloop()