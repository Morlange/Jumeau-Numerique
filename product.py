import time
import numpy as np
import random as rd

class produit():

    def __init__(self,nb_machines):
        self.tps_début_process = time.time()
        self.tps_fin_process = 0
        self.LT = 0
        self.process = 0
        self.etapesfaites = [0]*nb_machines #Indique si l'étape de fabrication est finie
        self.etapestpsdebut = [0]*nb_machines #liste des temps de lancement de debut de cycle de chaque machine
        self.etapestpsdebut[0] = self.tps_début_process #le premier temps correspond au tout début du lancement de la production
        self.etapestpsfin = [0]*nb_machines #liste des temps de lancement de fin de cycle de chaque machine
        self.tps_cycle = [0]*nb_machines #temps de cycle par machine
        self.ID = rd.randint(10**5,10**6-1)
    
    def entree_machine(self,k):
        self.etapestpsdebut[k] = time.time()
        return self
    
    def sortie_machine(self,k):
        self.etapestpsfin[k] = time.time()
        self.etapesfaites[k] = 1
        #print(self.etapestpsfin[k]-self.etapestpsdebut[k],k,self.etapestpsdebut[k],self.ID,self.etapestpsfin[k])
        return self


    def fin_process(self):
        self.tps_fin_process = time.time()
        self.etapestpsfin[-1] = self.tps_fin_process
        self.LT = round(self.tps_fin_process - self.tps_début_process,3)
        self.tps_cycle = list(np.round(np.array(self.etapestpsfin)-np.array(self.etapestpsdebut),3))
        return [self.tps_cycle, self.LT]
    
    def timer_machine(self,k):
        self.etapestpsdebut[k] = time.time()
    
    def __str__(self):
        return str(self.ID)

    


class machine():

    def __init__(self,name):
        self.nom_machine = name
        self.nb_piece = 0
        self.pieces_presentes = []
        self.En_fonctionnement = True
    
    def ajout_piece(self,pieces):
        '''Quand on rajoute une pièce au début de la ligne de production'''
        if self.En_fonctionnement :
            self.nb_piece += 1
            self.pieces_presentes += [pieces]
            return True
        else:
            return False

    
    def fin_piece(self):
        '''Quand la pièce arrive en fin de course'''
        if self.nb_piece > 0 and self.En_fonctionnement:
            self.nb_piece -= 1
            #print(self.nb_piece,self.nom_machine)
            return self.pieces_presentes.pop(0), True
        elif self.nb_piece <= 0:
            print("Pas de pièces")
        else:
            print("La machine ne fonctionne pas !!")
        return None, False
    
    def On_Off(self):
        '''Mise en marche et arrêt de la ligne de production'''
        if self.En_fonctionnement:
            self.En_fonctionnement = False
            print("Ne fonctionne plus")
        else:
            self.En_fonctionnement = True
            print("Fonctionne à nouveau")

def main() :
    quit()

if "__name__" == "__main__":
    main()