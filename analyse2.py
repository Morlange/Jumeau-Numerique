from tkinter import Tk, Label, LabelFrame
from data import LogoAM, TRS, Temps_de_production, Nombre_pieces, taille, Images, color_bg1, color_fg
from fonction import afficher_Image, creerGraphsTRS


# creation de l'objet fenetre
fen_analyse= Tk()

#Titre de la fenetre
fen_analyse.title('Analyse de production')

#Taille de la fenetre
fen_analyse.geometry('1300x630')

#icone de fenetre
fen_analyse.iconbitmap(LogoAM)

#configuration du fond
fen_analyse.config(background=color_bg1)
#Ajout d'un titre 
label_titre = Label(fen_analyse, text='Analyse de production', height=1,font=('Calibri', 14),fg=color_fg, bg = color_bg1) 
label_titre.grid(row=0,column=0, padx=500, pady=10)

#Frame TRS
frame_TRS = LabelFrame(fen_analyse, text='TRS', font =('Calibri', 12), fg=color_fg, bg = color_bg1, labelanchor='nw')
frame_TRS.grid(row=1,column=0,padx=50, pady=10)
Label(frame_TRS, text='Fonderie',fg=color_fg, bg = color_bg1).grid(row=1, column=0, padx=10, pady=20)
Label(frame_TRS, text='Usinage',fg=color_fg, bg = color_bg1).grid(row=1, column=1, padx=10, pady=20)
Label(frame_TRS, text='Assemblage',fg=color_fg, bg = color_bg1).grid(row=1, column=2, padx=10, pady=20)

Label(frame_TRS, text=TRS[0], fg=color_fg, bg = color_bg1).grid(row=2, column=0, padx=10, pady=20)
Label(frame_TRS, text=TRS[1], fg=color_fg, bg = color_bg1).grid(row=2, column=1, padx=10, pady=20)
Label(frame_TRS, text=TRS[2], fg=color_fg, bg = color_bg1).grid(row=2, column=2, padx=10, pady=20)

#Affichage des graphes des TRS

creerGraphsTRS(TRS[0],"TRS_fonderie")
creerGraphsTRS(TRS[1],"TRS_usinage")
creerGraphsTRS(TRS[2],"TRS_assemblage")

Images += afficher_Image(fen_analyse,1,1,"TRS_fonderie",taille,Images)
Images += afficher_Image(fen_analyse,2,1,"TRS_usinage",taille,Images)
Images += afficher_Image(fen_analyse,3,1,"TRS_assemblage",taille,Images)

#Frame Temps de production
frame_temps_de_production = LabelFrame(fen_analyse, text='Temps de production', font =('Calibri', 12), fg=color_fg, bg = color_bg1, labelanchor='nw')
frame_temps_de_production.grid(row=4,column=0,padx=50, pady=10)
Label(frame_temps_de_production, text='Fonderie', fg=color_fg, bg = color_bg1).grid(row=4, column=0, padx=10, pady=20)
Label(frame_temps_de_production, text='Usinage', fg=color_fg, bg = color_bg1).grid(row=4, column=1, padx=10, pady=20)
Label(frame_temps_de_production, text='Assemblage', fg=color_fg, bg = color_bg1).grid(row=4, column=2, padx=10, pady=20)

Label(frame_temps_de_production, text=Temps_de_production[0], fg=color_fg, bg = color_bg1).grid(row=5, column=0, padx=10, pady=20)
Label(frame_temps_de_production, text=Temps_de_production[1], fg=color_fg, bg = color_bg1).grid(row=5, column=1, padx=10, pady=20)
Label(frame_temps_de_production, text=Temps_de_production[2], fg=color_fg, bg = color_bg1).grid(row=5, column=2, padx=10, pady=20)

#Frame nombre de pièces 
frame_nb_pieces = LabelFrame(fen_analyse, text='Nombre de pièces produites', font =('Calibri', 12), fg=color_fg, bg = color_bg1, labelanchor='nw')
frame_nb_pieces.grid(row=7,column=0,padx=50, pady=10)
Label(frame_nb_pieces, text='Fonderie', fg=color_fg, bg = color_bg1).grid(row=7, column=0, padx=10, pady=20)
Label(frame_nb_pieces, text='Usinage', fg=color_fg, bg = color_bg1).grid(row=7, column=1, padx=10, pady=20)
Label(frame_nb_pieces, text='Assemblage', fg=color_fg, bg = color_bg1).grid(row=7, column=2, padx=10, pady=20)

Label(frame_nb_pieces, text=Nombre_pieces[0], fg=color_fg, bg = color_bg1).grid(row=8, column=0, padx=10, pady=20)
Label(frame_nb_pieces, text=Nombre_pieces[1], fg=color_fg, bg = color_bg1).grid(row=8, column=1, padx=10, pady=20)
Label(frame_nb_pieces, text=Nombre_pieces[2], fg=color_fg, bg = color_bg1).grid(row=8, column=2, padx=10, pady=20)

#Boucle d'affichage
frame_nb_pieces.mainloop()