# coding: utf-8

# import bibliothèque
from PIL import Image, ImageTk
from tkinter import Label, Tk, Canvas, Menu, Entry, N, S, VERTICAL, LabelFrame, Button
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
#importation de données situées sur d'autres fonctions
from data import client,LogoAM,TRS,Images_TRS,Temps_de_production,Nombre_pieces,color_bg1,color_bg,color_fg,Serveur_ON



def ouvrir_analyse ():
    '''ouvre les programmes suivants: analyse et analyse2'''
    subprocess.Popen("python analyse.py")

def ouvrir_OF ():
    '''ouvre les programmes suivants: ouvrir_OF'''
    subprocess.Popen("python ouvrir_OF.py")

def flux():
    '''sert à appeler le programme flux'''
    subprocess.Popen("python flux.py")

def ouvrir_jum_ass():
    '''sert à appeler le programme Jumeau_Num_Assemblage'''
    subprocess.Popen("python Jumeau_Num_Assemblage.py")

def ajout_produits():
    subprocess.Popen("python produits.py")

def ajout_machines():
    subprocess.Popen("python ajout_suppr_machine.py")

def ouvrir_calendrier():
    subprocess.Popen("python Calendrier.py")



def ouvrir_etat ():
    '''fonction servant à déterminer si le serveur est en fonctionnement ou en veille'''
    print(Serveur_ON)
    if Serveur_ON:
        subprocess.Popen("python Interface_machines.py")
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
        fen_Error_co.config(background=color_bg1)
        #Ajout d'un titre 
        label_titre = Label(fen_Error_co, text='Erreur de connection \nVeuillez lancer le serveur en premier', height=2,font=('Calibri', 14),fg=color_fg, bg = color_bg1) 
        label_titre.grid(row=0,column=0, padx=10, pady=75)

        fen_Error_co.mainloop()

def lancer_serveur():
    '''Sert à lancer le serveur'''
    global Serveur_ON
    if not Serveur_ON:
        subprocess.Popen("python Serveur.py")
        time.sleep(2)
        client.connect()
        print("Interface connectée")
        Serveur_ON = True
        label_etat_serv.configure(text="Etat du serveur : Connecté")
        fen.update()

def stop_serveur():
    '''On restart le programme pour espérer arrêter le serveur'''
    global Serveur_ON
    if Serveur_ON :
        Stop = client.get_node("ns = 2; i = 16")
        Stop.set_value(1)
        client.disconnect()
        Serveur_ON = False
        label_etat_serv.configure(text="Etat du serveur : Déconnecté")
        fen.update()

def quitter():
    '''On quitte le programme et on arrête le serveur'''
    if Serveur_ON :
        stop_serveur()
    fen.destroy()


#Creation de l'objet fenetre
fen= Tk()

#Titre de la fenetre
fen.title('Gestion de production')

#Taille de la fenetre
#fen.geometry('1300x630')

#icone de fenetre
fen.iconbitmap(LogoAM)

#configuration du fond
fen.config(background=color_bg1)

#Menu
mon_menu=Menu(fen)
fen.config(menu=mon_menu)

#Les 4 principaux onglets
mon_menu.add_command(label='Etat',command=ouvrir_etat)
mon_menu.add_command(label='OF',command=ouvrir_OF)
mon_menu.add_command(label='Analyse',command=ouvrir_analyse)

# création des boutons de la fenêtre
bouton_etat = Button (fen, text = 'Etat des machines',bd=1, font=('Calibri', 12),fg=color_fg, bg = color_bg,command=ouvrir_etat)
bouton_etat.grid(row=1, column=0, padx=40, pady=100)

bouton_flux =  Button (fen,text='Affichage du flux', bd=1, font=('Calibri', 12),fg=color_fg, bg = color_bg,command=flux)
bouton_flux.grid(row=3, column=1, padx=40,pady=100)

bouton_OF =  Button (fen, text = 'Ordres de fabrication',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ouvrir_OF)
bouton_OF.grid(row=1, column=1, padx=40, pady=100)

bouton_analyse =  Button (fen, text = 'Analyse de production',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ouvrir_analyse)
bouton_analyse.grid(row=1, column=2, padx=40, pady=100)

bouton_jumeau_assemblage =  Button (fen, text = 'Jumeau Numérique Assemblage',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ouvrir_jum_ass)
bouton_jumeau_assemblage.grid(row=1, column=3, padx=40, pady=100)

bouton_start_server =  Button (fen, text = 'Lancer le serveur',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=lancer_serveur)
bouton_start_server.grid(row=2, column=1, padx=40, pady=100)

bouton_ajout_produits =  Button (fen, text = 'Ajouter des produits',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ajout_produits)
bouton_ajout_produits.grid(row=4, column=0, padx=40, pady=100)

bouton_ajout_machines =  Button (fen, text = 'Ajouter des machines',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ajout_machines)
bouton_ajout_machines.grid(row=4, column=1, padx=40, pady=100)

bouton_ouvrir_calendrier =  Button (fen, text = 'Ouvrir le calendrier',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ouvrir_calendrier)
bouton_ouvrir_calendrier.grid(row=4, column=2, padx=40, pady=100)

bouton_serv =  Button (fen, text = 'Stopper le serveur',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=stop_serveur)
bouton_serv.grid(row=2, column=2, padx=40, pady=100)

label_etat_serv = Label(fen, text='Etat du serveur : Déconnecté', height=2,font=('Calibri', 14),fg=color_fg, bg = color_bg1)
label_etat_serv.grid(row=2, column=0, padx=40, pady=100)

bouton_quitter =  Button (fen, text = 'Quitter',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=quitter)
bouton_quitter.grid(row=3, column=0, padx=40, pady=40)


#Boucle d'affichage
fen.mainloop()



# ajouter un bouton "ajouter un ordre de fabrication" : voir le bug 
#modifier le produit

