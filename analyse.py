from tkinter import Tk, Label, Canvas, LabelFrame
from PIL import Image, ImageTk
from fonction import afficher_Image, creerGraphsTRS
from data import taille, Images, color_bg1, color_fg, TRS


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

    #Frame TRS
    frame_TRS = LabelFrame(fen_analyse, text='TRS', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    frame_TRS.grid(row=1,column=0)
    Label(frame_TRS, text='Fonderie', background=color_bg1, fg=color_fg).grid(row=1, column=0)
    Label(frame_TRS, text='Usinage', background=color_bg1, fg=color_fg).grid(row=3, column=0)
    Label(frame_TRS, text='Assemblage', background=color_bg1, fg=color_fg).grid(row=5, column=0)

    creerGraphsTRS(TRS[0],"TRS_fonderie","TRS fonderie")
    creerGraphsTRS(TRS[1],"TRS_usinage","TRS usinage")
    creerGraphsTRS(TRS[2],"TRS_assemblage","TRS assemblage")


    Images += afficher_Image(frame_TRS,2,0,"TRS_usinage.png",taille,Images)
    Images += afficher_Image(frame_TRS,4,0,"TRS_fonderie.png",taille,Images)
    Images += afficher_Image(frame_TRS,6,0,"TRS_assemblage.png",taille,Images)

    """
    Label(frame_TRS, label_usinage, bg=color_bg1).grid(row=2, column=0)
    Label(frame_TRS, label_fonderie, bg=).grid(row=4, column=0)           ###mettre les images 
    Label(frame_TRS, label_assemblage, bg=color_bg1).grid(row=6, column=0)
    """

    #Frame Temps de production
    frame_temps_de_production = LabelFrame(fen_analyse, text='Temps de production', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    frame_temps_de_production.grid(row=1,column=1)
    Label(frame_temps_de_production, text='Fonderie', background=color_bg1, fg=color_fg).grid(row=2, column=0)
    Label(frame_temps_de_production, text='Usinage', background=color_bg1, fg=color_fg).grid(row=2, column=1)
    Label(frame_temps_de_production, text='Assemblage', background=color_bg1, fg=color_fg).grid(row=2, column=2)

    Label(frame_temps_de_production, text='0', bg=color_bg1, fg=color_fg).grid(row=3, column=0)
    Label(frame_temps_de_production, text='0', bg=color_bg1, fg=color_fg).grid(row=3, column=1)
    Label(frame_temps_de_production, text='0', bg=color_bg1, fg=color_fg).grid(row=3, column=2)

    #Frame nombre de pièces 
    frame_nb_pieces = LabelFrame(fen_analyse, text='Nombre de pièces produites', font =('Calibri', 12), bg=color_bg1, labelanchor='nw', fg=color_fg)
    frame_nb_pieces.grid(row=1,column=2)
    Label(frame_nb_pieces, text='Fonderie', bg=color_bg1, fg=color_fg).grid(row=3, column=0)
    Label(frame_nb_pieces, text='Usinage', bg=color_bg1, fg=color_fg).grid(row=3, column=1)
    Label(frame_nb_pieces, text='Assemblage', bg=color_bg1, fg=color_fg).grid(row=3, column=2)

    Label(frame_nb_pieces, text='0', bg=color_bg1, fg=color_fg).grid(row=4, column=0)
    Label(frame_nb_pieces, text='0', bg=color_bg1, fg=color_fg).grid(row=4, column=1)
    Label(frame_nb_pieces, text='0', bg=color_bg1, fg=color_fg).grid(row=4, column=2)

    #Boucle d'affichage
    fen_analyse.mainloop()

if __name__ == "__main__":
    main()