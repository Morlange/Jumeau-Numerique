from tkinter import *
import tkinter as tk
from tkinter import ttk
from data import color_bg,color_bg1,color_fg

def main():
    #ouverture du fichier en lecture
    liste_machine=open('liste_machine.txt', 'r')
    l=liste_machine.readlines()
    machine=[]
    nom_machine=[]
    zone_machine=['Composite', 'Usinage', 'Forge','Metrologie','Assemblage','Bois','Fonderie']



    for i in range (len(l)):
        l[i] = l[i][:-1]
        if l[i]: #supprime les lignes qui sont 'vides' 
            machine.append(l[i].split(';'))
            nom_machine.append(machine[i][0]) # nom_machine est sous forme [['machine1', 'zone1'], ['machine2', 'zone2'],...]

    #ajout machine : programme qui est commandé par le boutton "ajouter" défini après
    def ajout_machine():
        machine_ajout= nom_machine_ajout.get()
        machine_ajout_zone=nom_machine_ajout_zone.get()
        
        machine_write=open('liste_machine.txt', 'w')
        for i in range (len (machine)):
            machine_write.write(machine[i][0])
            machine_write.write(';')
            machine_write.write(machine[i][1])
            machine_write.write('\n')
        #ajoute le nouveau produit sous forme nom_machine;zone (fichier en écriture)
            
        machine_write.write(machine_ajout)
        machine_write.write(';')
        machine_write.write(machine_ajout_zone)
        machine_write.write('\n') #ajoute les machines déjà présentent dans le fichier txt
        liste_machine.close()
        machine_ajout = nom_machine_ajout.delete(0,len(machine_ajout)) 

    #supprimer machine : programme qui est commandé par le boutton "supprimer" défini après
    def suppr_machine():
        machine_suppr= nom_machine_suppr.get()
        machine_write=open('liste_machine.txt', 'w')

        for i in range (len (machine)):
            if machine[i][0]!=machine_suppr:
                machine_write.write(machine[i][0])
                machine_write.write(';')
                machine_write.write(machine[i][1])
                machine_write.write('\n')
                print("aaaaaa"+machine[i][0]+";"+machine[i][1]+'\n')
        liste_machine.close()

    #fenêtre machine
    fen_machine=tk.Tk()
    fen_machine.geometry("1500x1500")
    fen_machine.config(bg="#333333")
    fen_machine.title("Machine")

    #ajout d'un titre
    frame_ajout = tk.LabelFrame(fen_machine, text='Ajouter une machine', font =('Times new roman', 12), fg=color_fg, bg=color_bg1, labelanchor='nw')
    frame_ajout.grid(row=2,column=7,padx=5, pady=10)

    frame_suppr = tk.LabelFrame(fen_machine, text='Supprimer une machine', font =('Times new roman', 12), fg=color_fg, bg=color_bg1, labelanchor='nw')
    frame_suppr.grid(row=7,column=7,padx=5, pady=10)

    frame_mach = tk.LabelFrame(fen_machine, text='Liste des machines :', font =('Times new roman', 12), fg=color_fg, bg=color_bg1)
    frame_mach.grid(row=8,column=7,padx=20, pady=10)
    nom_machine1=""
    for k in (nom_machine):
        print(k)
        nom_machine1 += k+str("\n")
    
    frame_nom_mach=tk.Label(frame_mach, text=nom_machine1, font =('Times new roman', 12), fg=color_fg, bg=color_bg1)
    frame_nom_mach.grid(row=9,column=7,padx=20, pady=10)


    L_machine = Label(frame_ajout, text='Nom de la machine',fg=color_fg, bg=color_bg1).grid(row=2, column=2,padx=10,pady=10)
    L_machine = Label(frame_ajout, text='Zone',fg=color_fg, bg=color_bg1).grid(row=2, column=3,padx=10,pady=10)

    #zone texte bouton
    ajout_var = StringVar()  #zone de texte pour rentrer un nouveau produit
    nom_machine_ajout=tk.Entry(frame_ajout, textvariable=ajout_var)
    nom_machine_ajout.grid(row=3, column=2, padx=10,pady=10)

    nom_machine_ajout_zone=ttk.Combobox(frame_ajout, values=zone_machine) #liste déroulante des zones
    nom_machine_ajout_zone.grid(row=3, column=3)

    nom_machine_suppr=ttk.Combobox(frame_suppr, values=nom_machine) #liste déroulante des machines
    nom_machine_suppr.grid(row=7, column=2, padx=10, pady=10)

    #ajout d'un bouton (ajouter et supprimer)
    bouton_ajout=tk.Button(frame_ajout, text='Ajouter', fg=color_fg, bg=color_bg, command= ajout_machine)
    bouton_ajout.grid(row=5, column=2, padx=10,pady=10)
    bouton_suppr=tk.Button(frame_suppr, text='Supprimer', fg=color_fg, bg=color_bg, command=suppr_machine)
    bouton_suppr.grid(row=8, column=2, padx=10,pady=10)

    liste_machine.close()
    fen_machine.mainloop()

if __name__ == "__main__" :
    main()
