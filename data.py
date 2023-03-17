import xlrd
from opcua import Client


LogoAM = "logo-AM.ico"

#données OF

document = xlrd.open_workbook('OF.xls')
nb_feuilles = document.nsheets
OF=[]

for i in range (0,nb_feuilles) :
    feuille = document.sheet_by_index(i)
    nom_produit = feuille.name
    nb_colonnes = feuille.ncols
    nb_lignes = feuille.nrows
    n_OF=[]
    nom_OF=[]
    machine_OF=[]
    debut_OF=[]
    caracteristique=[feuille.cell_value(rowx=0,colx=1),feuille.cell_value(rowx=1,colx=1),feuille.cell_value(rowx=2,colx=1) ]
    for i in range (4,nb_lignes):
        n_OF.append(feuille.cell_value(rowx=i, colx=0))
        nom_OF.append(feuille.cell_value(rowx=i, colx=1))
        machine_OF.append(feuille.cell_value(rowx=i, colx=2))
        debut_OF.append(feuille.cell_value(rowx=i, colx=3))
    OF_produit=[nom_produit, n_OF, nom_OF, machine_OF, debut_OF,caracteristique]
    OF.append(OF_produit)
    OF_produit=[]
    
#forme des odres de fabrication : OF=[[nom_produit, n_OF, nom_OF, machine_OF, debut_OF,caracteristique], [nom_produit, n_OF, nom_OF, machine_OF, debut_OF,caracteristique], ...]

nb_produits = len(OF)
liste_produit =[]
for i in range (nb_produits):
    liste_produit.append(OF[i][0])

#données pour analyse 
TRS=[50,20,30]
Images_TRS = []
Temps_de_production=[46,6,23]
Nombre_pieces=[12,10,7]
LogoAM = "Logo_AM.png"
Images = []
val = 120
taille = (int(4/3*val),val)

#données pour serveur
Serveur_ON = False
url = "opc.tcp://127.0.0.1:4880"
client = Client(url)

#Données couleurs
color_bg1 = "#333333"
color_bg = "#1e1e1e"
color_fg = "#dcdcaa"