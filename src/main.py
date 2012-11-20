#!/usr/bin/python
# -*-coding:UTF-8 -* 

# Imports
import os
import argparse


# Main - Lancement des calculs
def Main():
  '''Fonction Principal
  '''
  print("----- Projet NF20 -----".center(60,"-")+"\n")

  # Création du parser d'aguments
  parser = argparse.ArgumentParser(description="Script Arguments Parser")
  parser.add_argument("-d", "--data", dest="data", type=str, action="store", default="No Path", help="Relative path to the data file")

  args = parser.parse_args()

  # Appel du parser de fichier
  infoGraph = Parser(args.data)

  # Lancement de Prim
  #result = Prim(graph, sommet)
  #print("Arbre couvrant de poids minimun: "+str(result))

  result = Prim(infoGraph)
 
  print("result "+str(result)) 
  
  # Debug
  #print(infoGraph)


#--------------------------------------------------------------------------------------------------------------------------------------------#

# Fonctions
def Parser(data): # Voir pour la sécurisation du Parsing des données - Ligne manquante/nom des sommet=lettre ou nombre/
  '''Fonction permettant de parser le fichier .dat  
  Retourne la liste des arcs du graphe avec, dans l'ordre, le point de départ, le point d'arrivé et le poids de l'arête
  '''

  print("Parsing du fichier "+data+"\n")
  nbrLigne = 0
  listArcs = []

  fichier = open(data, 'r') # Ouverture du fichier

  for ligne in fichier:
    if nbrLigne==0: # On extrait le type de graph
      titreGraph = ligne.rstrip('\n\r')
    elif nbrLigne==1: # On extrait le nombre de sommet
      nbrNode = ligne.rstrip('\n\r')
    elif nbrLigne == 2: # On extrait le nombre d'arcs
      nbrEdge = ligne.rstrip('\n\r')
    elif nbrLigne>3: # liste des arcs
      if ligne.rstrip('\n\r') == "END": # Fin des données, on sort de la boucle
        break
      else:
        temp = ligne.rstrip('\n\r').replace(" ","") # On dégage les espaces en trop
        temp = temp.split("\t") # On sépare les données grâce aux tabulation du fichier
        for i, value in enumerate(temp): # Permet de convertir les données
          if i == 2:
            temp[i] = float(value)
          else:
            temp[i] = int(value)
        listArcs.append(temp)

    nbrLigne = nbrLigne+1

  fichier.close() # Fermeture du fichier

  # traitement des variables
  nbrNode = nbrNode.split("\t")[2].replace(" ","")
  nbrEdge = nbrEdge.split("\t")[2].replace(" ","")


  return {'Title': titreGraph, 'Nodes': nbrNode, 'Edges': nbrEdge, 'Arcs': listArcs}# On retourne un dictionnaire avec l'ensemble des info parser !


def Prim(graph):
  '''Algorithme de Prim
  Retourne la liste des sommets du chemin de cout minimum
  '''

  nbrNode = graph['Nodes']
  listArcs = graph['Arcs']
  usedEdges = []
  usedArcs = []
  tempArcs = []
  arcToChoose = None
  edgeToChoose = None
  notToChoose = True

  
  usedEdges.append(listArcs[0][0]) # On choisi un sommet duquel on commence le graphe

  while len(usedEdges) < int(nbrNode): # tant qu'on est pas passé par tous les sommets
    actualEdges = usedEdges[-1] # On choisi le dernier somment sur lequel on est arrivé

    print("actualEdges "+str(actualEdges))

    for i in listArcs:
      if actualEdges in i and i not in usedArcs:
        tempArcs.append(i) # on liste l'ensemble des arcs sortant du poids actuel

    print("tempArcs "+str(tempArcs))

    tempMinWeight = tempArcs[0][2] # On prend une valeur de poids parmis les arcs possible
    
    for i, value in enumerate(tempArcs):
      if value[2] <= tempMinWeight: # Si le poids de l'arete teste est inférieur ou egale au poids référence alors on mémorise le poid l'arete et le futur sommet
        tempMinWeight = value[2] 
        arcToChoose = value

        if value[0] == actualEdges:
          edgeToChoose = value[1]
        else:
          edgeToChoose = value[0]

    print("edgeToChoose "+str(edgeToChoose)+"\n")

    usedEdges.append(edgeToChoose)
    usedArcs.append(arcToChoose)    
    
    
    #print("tempMinWeight "+str(tempMinWeight))
    #print("notToChoose "+str(notToChoose)) 
    #print arcToChoose
    #print edgeToChoose
    #print("usedEdges "+str(usedEdges)+"\n") 


    # Reset
    tempArcs = []
    arcToChoose = None
    edgeToChoose = None

  return {'Edges': usedEdges, 'Arcs': usedArcs}

def Kruskal(graph):
  '''Algorithme de Kruskal
  Retourne la liste des sommets du chemin de cout minimum
  '''

  return []


# On lance la fonction
if __name__ == '__main__':
  Main()



'''
Temps Max Parsing
100 sommets => 0.2s
... 
1000 sommets => 17-18s


Le Parsing en lui-même ne met pas bcp de temps, par contre l'affichage des valeurs est très long !!!

Some help :)

http://programmingpraxis.com/2010/04/09/minimum-spanning-tree-prims-algorithm/
'''