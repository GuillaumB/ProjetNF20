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
  graph = Parser(args.data)
  print(graph)

# Fonctions
def Parser(data):
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

  return listArcs # On retourne la liste des arcs avec, dans l'ordre, pt départ, pt arrivé, poids


def Prim(graph):
  '''Algorithme de Prim
  Retourne la liste des sommets du chemin de cout minimum
  '''

  return []

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