from tkinter import Tk, Label, Canvas, LabelFrame
from PIL import Image, ImageTk
from fonction import afficher_Image


Images = []
val = 120
taille = (int(4/3*val),val)

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
fen_analyse.config(background='#D3D3D3')
#Ajout d'un titre 
label_titre = Label(fen_analyse, text='Analyse de production', height=1,fg='black',font=('Calibri', 14),bg='#D3D3D3') 
label_titre.grid(row=0,column=1)

#Frame TRS
frame_TRS = LabelFrame(fen_analyse, text='TRS', font =('Calibri', 12), bg='#D3D3D3', labelanchor='nw')
frame_TRS.grid(row=1,column=0)
Label(frame_TRS, text='Fonderie').grid(row=1, column=0)
Label(frame_TRS, text='Usinage').grid(row=3, column=0)
Label(frame_TRS, text='Assemblage').grid(row=5, column=0)



Images += afficher_Image(frame_TRS,2,0,"TRS_usinage.png",taille,Images)
Images += afficher_Image(frame_TRS,4,0,"TRS_fonderie.png",taille,Images)
Images += afficher_Image(frame_TRS,6,0,"TRS_assemblage.png",taille,Images)

"""
Label(frame_TRS, label_usinage, bg='#D3D3D3').grid(row=2, column=0)
Label(frame_TRS, label_fonderie, bg='#D3D3D3').grid(row=4, column=0)           ###mettre les images 
Label(frame_TRS, label_assemblage, bg='#D3D3D3').grid(row=6, column=0)
"""

#Frame Temps de production
frame_temps_de_production = LabelFrame(fen_analyse, text='Temps de production', font =('Calibri', 12), bg='#D3D3D3', labelanchor='nw')
frame_temps_de_production.grid(row=1,column=1)
Label(frame_temps_de_production, text='Fonderie').grid(row=2, column=0)
Label(frame_temps_de_production, text='Usinage').grid(row=2, column=1)
Label(frame_temps_de_production, text='Assemblage').grid(row=2, column=2)

Label(frame_temps_de_production, text='0', bg='#D3D3D3').grid(row=3, column=0)
Label(frame_temps_de_production, text='0', bg='#D3D3D3').grid(row=3, column=1)
Label(frame_temps_de_production, text='0', bg='#D3D3D3').grid(row=3, column=2)

#Frame nombre de pièces 
frame_nb_pieces = LabelFrame(fen_analyse, text='Nombre de pièces produites', font =('Calibri', 12), bg='#D3D3D3', labelanchor='nw')
frame_nb_pieces.grid(row=1,column=2)
Label(frame_nb_pieces, text='Fonderie').grid(row=3, column=0)
Label(frame_nb_pieces, text='Usinage').grid(row=3, column=1)
Label(frame_nb_pieces, text='Assemblage').grid(row=3, column=2)

Label(frame_nb_pieces, text='0', bg='#D3D3D3').grid(row=4, column=0)
Label(frame_nb_pieces, text='0', bg='#D3D3D3').grid(row=4, column=1)
Label(frame_nb_pieces, text='0', bg='#D3D3D3').grid(row=4, column=2)

#Boucle d'affichage
fen_analyse.mainloop()