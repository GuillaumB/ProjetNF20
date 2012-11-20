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
  graph, sommet = Parser(args.data)
  print graph

  # Lancement de Prim
  #result = Prim(graph, sommet)
  #print("Arbre couvrant de poids minimun: "+str(result))

#--------------------------------------------------------------------------------------------------------------------------------------------#

# Fonctions
def Parser(data): # Voir pour la sécurisation du Parsing des données - Ligne manquante/nom des sommet=lettre ou nombre/
  '''Fonction permettant de parser le fichier .dat  
  Retourne la liste des arcs du graphe avec, dans l'ordre, le point de départ, le point d'arrivé et le poids de l'arête
  '''

  print("Parsing du fichier "+data)
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

  # Affichage des infos - Debug
  #print("Type de graphe: "+titreGraph)
  #print("Nombre de Sommets: "+nbrNode)
  #print("Nombre d'arcs: "+nbrEdge)
  #print("Liste des arcs: "+str(listArcs))

  return listArcs, nbrNode # On retourne la liste des arcs avec, dans l'ordre, pt départ, pt arrivé, poids


def Prim(graph, nbrNode):
  '''Algorithme de Prim
  Retourne la liste des sommets du chemin de cout minimum
  '''
  listCourtChemin = []
  listSommetCourtChemin = []
  listTempArete = []
  pointDepart = graph[0][0]

  listCourtChemin.append(graph[0])
  listSommetCourtChemin.append(graph[0][0])

  #tailleListCourtchemin = len(listCourtChemin) #Debug
  
  while len(listCourtChemin) != int(nbrNode):
    # On cherche tous les aretes sortant du point sur lequel on est
    for i, value in enumerate(graph):
      if listCourtChemin[len(listCourtChemin)-1][0] in graph[i]:
        listTempArete.append(graph[i])
    
    # On cherche l'arete de poids minimum en verifiant que ça boucle pas
    for i, value in enumerate(listTempArete):
      if i == 0:
        poidMini = listTempArete[i][2]
      else:
        if listTempArete[i][2]<poidMini:
          if listCourtChemin[i][1] not in listSommetCourtChemin:
            poidMini = listTempArete[i][2]
            arcsSuivant = listTempArete[i]
            pointSuivant = listTempArete[i][1]
        

    listCourtChemin.append(arcsSuivant)
    listSommetCourtChemin.append(pointSuivant)
    listTempArete = []
    #tailleListCourtchemin = tailleListCourtchemin+1 #Debug
    




  return listCourtChemin

def Kruskal(graph):
  '''Algorithme de Kruskal
  Retourne la liste des sommets du chemin de cout minimum
  '''

  return []

# On lance la fonction
Main()

'''
Temps Max Parsing
100 sommets => 0.2s
... 
1000 sommets => 17-18s


Le Parsing en lui-même ne met pas bcp de temps, par contre l'affichage des valeurs est très long !!!
'''