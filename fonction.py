#importer les bibliothèques
from PIL import Image, ImageTk
from tkinter import Label
from numpy import c_, linspace, radians, pi, degrees, arange, cos, sin
from matplotlib import cm
from matplotlib.pyplot import subplots, tight_layout, savefig
from matplotlib.patches import Circle, Wedge, Rectangle
from data import color_bg1
from tkinter import Tk,Label



def afficher_Image(fen,row,column,name,size,Images):
    '''Retourne une image png
    Il faut donner en entrée la fenêtre,row,column,name,size,le nom qu'on veut donner à l'image
    '''
    if name[-4:] != '.png':
        name += '.png'
    Images += [ImageTk.PhotoImage(Image.open(name).resize(size))]
    imgLabel = Label(fen, image = Images[-1], background=color_bg1)
    imgLabel.grid(row=row, column=column)
    fen.update()
    return Images



def creerGraphsTRS(x,name,titre = "Titre du graphique"):
    '''Sert à afficher la valeur du TRS'''
    #x valeur en pourcentage
    TRSgraph=[]
    namefile = name
    #conversion en .png
    if not name[-4:] == ".png":
        namefile += ".png"
    
    a=x%10
    if a==1 or a==2 or a==3 : 
        x=int((x/10)%10)*10
    elif a==4 or a==5 :
        x=int((x/10)%10)*10+5
    elif a==6 or a==7 or a==8 : 
        x=int((x/10)%10)*10+5
    elif a==9 : 
        x=int((x/10)%10)*10+10
    
    #on sépart les possibilités en segments (la valeur affichée n'est pas précise mais correspond à une zone)
    TRSlist=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
    TRSgraph.append(TRSlist.index(x)+1)  

    
    def degree_range(n): 
        start = linspace(0,180,n+1, endpoint=True)[0:-1]
        end = linspace(0,180,n+1, endpoint=True)[1::]
        mid_points = start + ((end-start)/2.)
        return c_[start, end], mid_points


    def rot_text(ang): 
        """Permet d'écrire le texte le long d'un arc de cercle"""
        rotation = degrees(radians(ang) * pi / pi - radians(90))
        return rotation

    def gauge(labels=['LOW','MEDIUM','HIGH','VERY HIGH','EXTREME'], \
            colors='jet_r', arrow=1, title='', fname=False): 
        
        """some sanity checks first"""
        N = len(labels)
        
        if arrow > N: 
            raise Exception("\n\nThe category ({}) is greated than \
            the length\nof the labels ({})".format(arrow, N))
    
        
        """if colors is a string, we assume it's a matplotlib colormap
        and we discretize in N discrete colors"""
        if isinstance(colors, str):
            cmap = cm.get_cmap(colors, N)
            cmap = cmap(arange(N))
            colors = cmap[::-1,:].tolist()
        if isinstance(colors, list): 
            if len(colors) == N:
                colors = colors[::-1]
            else: 
                raise Exception("\n\nnumber of colors {} not equal \
                to number of categories{}\n".format(len(colors), N))

        """begins the plotting"""
        fig, ax = subplots()

        ang_range, mid_points = degree_range(N)

        labels = labels[::-1]
        
        """plots the sectors and the arcs"""
        patches = []
        for ang, c in zip(ang_range, colors): 
            # sectors
            patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
            # arcs
            patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))
        
        [ax.add_patch(p) for p in patches]

        
        """set the labels (e.g. 'LOW','MEDIUM',...)"""
        for mid, lab in zip(mid_points, labels): 

            ax.text(0.35 * cos(radians(mid)), 0.35 * sin(radians(mid)), lab, \
                horizontalalignment='center', verticalalignment='center', fontsize=14, \
                fontweight='bold', rotation = rot_text(mid))

        """set the bottom banner and the title"""
        r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
        ax.add_patch(r)
        
        ax.text(0, -0.05, title, horizontalalignment='center', \
            verticalalignment='center', fontsize=22, fontweight='bold')

        """plots the arrow now"""
        pos = mid_points[abs(arrow - N)]
        
        ax.arrow(0, 0, 0.225 * cos(radians(pos)), 0.225 * sin(radians(pos)), \
                    width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
        
        ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
        ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))

        """removes frame and ticks, and makes axis equal and tight"""
        ax.set_frame_on(False)
        ax.axes.set_xticks([])
        ax.axes.set_yticks([])
        ax.axis('equal')
        tight_layout()
        if fname:
            fig.savefig(fname, dpi=200)


    image=gauge(labels=['0',' ','10',' ','20',' ','30',' ','40',' ','50',' ','60',' ','70',' ','80',' ','90',' ','100'], \
        colors=['#ED1C24','#ED1C24','#ED1C24','#ED1C24','#ED1C24','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00',
                '#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#FFCC00','#007A00','#007A00','#007A00','#007A00',
                '#007A00'], arrow=TRSgraph[0], title=titre)
    
    savefig(namefile, transparent = True)