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

  newGraph = Prim(infoGraph)

  print(newGraph)

  result = Prim(infoGraph)
 
  print("result "+str(result)) 
  
  # Debug
  #print(infoGraph)


#--------------------------------------------------------------------------------------------------------------------------------------------#

# Fonctions
def Error(msg):
  """Affiche un meesage d'erreur et quitte l'application
  """
  print(msg)
  quit()


def Parser(data):
  """Fonction permettant de parser le fichier .dat  
  """
  print("Parsing du fichier "+data+"\n")
  nbrLigne = 0
  listArcs = []

  fichier = open(data, 'r') # Ouverture du fichier

  for ligne in fichier:
    if nbrLigne==0: # On extrait le type de graph
      if ligne.lower().find("graph")>=0:
        typeGraph = ligne.rstrip('\n\r')
      else:
        Error("Erreur de Formatage : Type de Graphe")

    elif nbrLigne==1: # On extrait le nombre de sommet
      if ligne.lower().find("nb_nodes")>=0:
        nbrNode = ligne.rstrip('\n\r')
        nbrNode = nbrNode.split("\t")[2].replace(" ","")
      else:
        Error("Erreur de Formatage : Nombre de Sommets")

    elif nbrLigne == 2: # On extrait le nombre d'arcs
      if ligne.lower().find("nb_edges")>=0:
        nbrEdge = ligne.rstrip('\n\r')
        nbrEdge = nbrEdge.split("\t")[2].replace(" ","")
      else:
        Error("Erreur de Formatage : Nombre d'Arcs")

    elif nbrLigne>3: # liste des arcs
      if ligne.rstrip('\n\r') == "END": # Fin des données, on sort de la boucle
        break
      else:
        temp = ligne.rstrip('\n\r').replace(" ","") # On dégage les espaces en trop
        temp = temp.split("\t") # On sépare les données grâce aux tabulation du fichier
        for i, value in enumerate(temp): # Permet de convertir les données
          if i != 0 and i%2 == 0:
            try:
              temp[i] = float(value)
            except ValueError:
              Error("Oops ! Il doit y avoir une erreur dans les valeurs du poids des arcs !")
          else:
            temp[i] = value

        listArcs.append(temp)

    nbrLigne = nbrLigne+1

  fichier.close() # Fermeture du fichier


  return {'Title': typeGraph, 'Nodes': nbrNode, 'Edges': nbrEdge, 'Arcs': listArcs}# On retourne un dictionnaire avec l'ensemble des info parser !


def Prim(graph):
  """Algorithme de Prim
  Retourne la liste des sommets du chemin de cout minimum et la liste des arcs qui composent le nouveau graphe 
  """

  nbrNode = graph['Nodes']
  listArcs = graph['Arcs']
  usedEdges = []
  usedArcs = []

  tempArcs = []
  
  arcToChoose = None
  edgeToChoose = None

  usedEdges.append(listArcs[0][0]) # On choisi un sommet pour on commence le graphe

  while len(usedEdges) < int(nbrNode): # tant qu'on est pas passé par tous les sommets
    actualEdge = usedEdges[-1] # On choisi le dernier somment sur lequel on est arrivé

    #print("actualEdges "+actualEdge)

    for i in listArcs:
      if actualEdge in i:
        tempArcs.append(i) # on liste l'ensemble des arcs sortant du point actuel et qui ne va pas vers point déjà utilisé


    for j in usedArcs: # on enlève des arcs possible les arcs sur lesquels on est déjà passés
      if j in tempArcs:
        tempArcs.remove(j)

    #print(tempArcs)

    tempMinWeight = tempArcs[0][2] # On prend une valeur de poids parmis les arcs possible

    for i, value in enumerate(tempArcs):
      if value[2] <= tempMinWeight: # Si le poids de l'arete teste est inférieur ou egale au poids référence alors on mémorise le poid l'arete et le futur sommet
        tempMinWeight = value[2] 
        arcToChoose = value
        edgeToChoose = value[1]

        if value[0] == actualEdge:
          edgeToChoose = value[1]
        else:
          edgeToChoose = value[0]
        
    usedEdges.append(edgeToChoose)
    usedArcs.append(arcToChoose)
    
    # Reset
    tempArcs = []
    arcToChoose = None
    edgeToChoose = None


  return {'Edges':usedEdges, 'Arcs': usedArcs}

def Kruskal(graph):
  """Algorithme de Kruskal
  Retourne la liste des sommets du chemin de cout minimum
  """

  return []

# On lance la fonction
if __name__ == '__main__':
  Main()



'''
Le Parsing en lui-même ne met pas bcp de temps, par contre l'affichage des valeurs est très long !!!

Some help :)

http://programmingpraxis.com/2010/04/09/minimum-spanning-tree-prims-algorithm/
'''
