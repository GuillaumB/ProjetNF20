#!/usr/bin/python
# -*-coding:UTF-8 -* 

# Imports
import os
import argparse

from DisjointSet import DisjointSet 

from operator import itemgetter

# Main - Lancement des calculs
def Main():
  '''Fonction Principal
  '''
  print("\n"+"----- Projet NF20 -----".center(70,"-")+"\n")

  # Création du parser d'aguments
  parser = argparse.ArgumentParser(description="Script Arguments Parser")
  parser.add_argument("-d", "--data", dest="data", type=str, action="store", default="No Path", help="Relative path to the data file")
  parser.add_argument("-P", "--Prim", dest="activePrim", action="store_true", default=False, help="Active Prim Algorithme")
  parser.add_argument("-K", "--Kruskal", dest="activeKruskal", action="store_true", default=False, help="Active Kruskal Algorithme")
  parser.add_argument("-D", "--Diametre", dest="activeDiametre", action="store_true", default=False, help="Active Diametre")

  args = parser.parse_args()

  # Appel du parser de fichier
  graph = Parser(args.data)

  if args.activePrim:
    print("Lancement de Prim")
    #resultPrim = Prim(graph)
    resultPrim = PrimCours(graph)
    poidsPrim = CompterPoids(resultPrim)
    print("Prim : "+str(resultPrim))
    print("pour un poids de "+str(poidsPrim))

  if args.activeKruskal:
    print("Lancement de Kruskal")
    #resultKruskal = Kruskal(graph)
    resultKruskal = KruskalCours(graph)
    poidsKruskal = CompterPoids(resultKruskal)
    print("Kruskal : "+str(resultKruskal))
    print("pour un poids de "+str(poidsKruskal))

  if args.activeDiametre:
    resultDiam = Diametre(graph)
    print("Diamètre : "+str(resultDiam))

  if not args.activePrim and not args.activeKruskal and not args.activeDiametre:
    print("Resultat du Parser : "+str(graph))


#----------------------------------------------------------------------#

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
  edges = []
  nodes = []

  fichier = open(data, 'r') # Ouverture du fichier

  for ligne in fichier:
    if nbrLigne==0: # On extrait le type de graph
      if ligne.lower().find("graph")>=0:
        ligne  = ligne.rstrip()
        typeGraph = ligne.rstrip('\n\r')
      else:
        Error("Erreur de Formatage : Type de Graphe")

    elif nbrLigne==1: # On extrait le nombre de sommet
      if ligne.lower().find("nb_nodes")>=0:
        nbrNode = ligne.rstrip('\n\r')
        nbrNode = nbrNode.replace("\t", " ").split()[1]
      else:
        Error("Erreur de Formatage : Nombre de Sommets")

    elif nbrLigne == 2: # On extrait le nombre d'arcs
      if ligne.lower().find("nb_edges")>=0:
        nbrEdge = ligne.rstrip('\n\r')
        nbrEdge = nbrEdge.replace("\t", " ").split()[1]
      else:
        Error("Erreur de Formatage : Nombre d'Arcs")

    elif nbrLigne>3: # liste des arcs
      if ligne.rstrip('\n\r') == "END": # Fin des données, on sort de la boucle
        break
      else:
        temp = ligne.replace("\t", " ").rstrip('\n\r') # On remplace les tabulations pas de espaces
        temp = temp.split() # On découpe le tout en trois grâce aux espaces
        for i, value in enumerate(temp): # Permet de convertir les données
          if i != 0 and i%2 == 0:
            try:
              temp[i] = float(value)
            except ValueError:
              Error("Oops ! Il doit y avoir une erreur dans les valeurs du poids des arcs !")
          else:
            temp[i] = value
            if value not in nodes:
              nodes.append(value)

        edges.append(temp)

    nbrLigne +=1

  fichier.close() # Fermeture du fichier

  nodes.sort()

  return {'Type': typeGraph, 'Nodes': nodes, 'Edges': edges}# On retourne un dictionnaire avec l'ensemble des info parser !

def CompterPoids(liste):
  poids = 0;

  for edge in liste:
    poids += edge[2]

  return poids

#======================================================================#

def PrimCours(graph):
  chemin = []
  forest = []
  possibleEdges = []
  pere = {}

  listNodes = graph['Nodes']
  listEdges = graph['Edges']

  for node in listNodes:
    pere[node] = node

  origin = listNodes[0]

  nbrNode = len(listNodes)-1

  while nbrNode != 0:

    for node in listNodes:
      if pere[node] == origin and node not in forest:
        forest.append(node)

    for edge in listEdges:
      n1, n2, p = edge
   
      if (n1 in forest and n2 not in forest) or (n1 not in forest and n2 in forest):
        possibleEdges.append(edge)

    possibleEdges = sorted(possibleEdges, key=itemgetter(2))

    edgeTochoose = possibleEdges[0]
    chemin.append(edgeTochoose)
    listEdges.remove(edgeTochoose)

    t1, t2, _ = edgeTochoose

    if t1 in forest:
      pere[t2] = pere[t1]
    else:
      pere[t1] = pere[t2]

    nbrNode -= 1

    possibleEdges = []

  return chemin

def Prim(graph): # A revoir totalement avec tas binaire minimun ou fibonacci
  """Algorithme de Prim + Union-Find
  Retourne la liste des arretes du graphe de coût minimum
  """

  forest = DisjointSet()
  chemin = []
  tempEdges = []
  usedNodes = [] 

  for n in graph['Nodes']:
    forest.add(n)

  nbrNodes = len(graph['Nodes'])

  origin = graph['Nodes'][0]

  usedNodes.append(origin)

  while(len(chemin) != nbrNodes-1):
    tempNodes = []
    tempEdges = []    

    for node in forest:
      if forest[node] in usedNodes: # On cherche tous les sommets dont le père fait parti des sommet déjà parcouru
        tempNodes.append(node)

    for node in tempNodes: # A AMELIORER !! SOURCE DE PERTE DE TEMPS !!!!
      for edge in graph['Edges']:
        if node in edge and edge not in chemin:
          tempEdges.append(edge)

    tempEdges = sorted(tempEdges, key=itemgetter(2))   

    chemin.append(tempEdges[0]) # On prend l'arrete avec le plus petit poids

    if graph['Type'].upper() == "UNDIRECTED GRAPH":
      if chemin[-1][0] in usedNodes:
        forest.union(chemin[-1][0], chemin[-1][1])
        usedNodes.append(chemin[-1][0])
      else:
        forest.union(chemin[-1][1], chemin[-1][0])
        usedNodes.append(chemin[-1][1])             
    else:
      forest.union(chemin[-1][1], chemin[-1][0])
      usedNodes.append(chemin[-1][1])

  return chemin

#======================================================================#

def KruskalCours(graph):
  chemin = []
  arbres = {}

  for node in graph['Nodes']:
    arbres[node] = node

  listEdges = sorted(graph['Edges'], key=itemgetter(2)) 

  while(len(chemin)<len(graph['Nodes'])-1):
    edgeTochoose = listEdges[0]
    listEdges.remove(edgeTochoose)

    n1, n2, p = edgeTochoose

    if arbres[n1] != arbres[n2]:
      chemin.append(edgeTochoose)

      arbres[n2] = arbres[n1]

  return chemin

def Kruskal(graph):
  """Algorithme de Kruskal
  Retourne la liste des arretes du graphe de coût minimum
  """

  forest = DisjointSet()
  chemin = []

  for n in graph['Nodes']:
    forest.add(n)

  nbrNodes = len(graph['Nodes']) - 1

  for arc in sorted(graph['Edges'], key=itemgetter(2)): #O( --- )
    n1, n2, poids = arc

    t1 = forest.find(n1)
    t2 = forest.find(n2)

    if t2 != t1:
      chemin.append(arc)
      nbrNodes -= 1

      if nbrNodes == 0:
        return chemin

      forest.union(t1, t2)

#======================================================================#

def Diametre(graph):
  """Double recherche en largeur
  retourne ...
  """
  diametre = []
  adj = []
  parcouru = {}  

  listNodes = graph['Nodes']
  listEdges = graph['Edges']


  # Premier Parcours pour trouver une extrémité du graphe
  for node in listNodes:
    parcouru[node] =  False

  actual = listNodes[0]
  parcouru[actual] = True

  diametre.append(actual)

  while len(diametre) != len(listNodes):
    
    for edge in listEdges:
      if actual in edge:
        if edge[0] == actual:
          adj.append(edge[1])
        else:
          adj.append(edge[0])

    for node in adj:
      if not parcouru[node]:
        parcouru[node] = True
        diametre.append(node)

    actual = diametre[-1]

  # Second parcours pour trouver le diametre du graphe
  first = diametre[-1]
  diametre = []

  for node in listNodes:
    parcouru[node] =  False

  actual = first
  parcouru[actual] = True

  diametre.append(actual)

  while len(diametre) != len(listNodes):
    
    for edge in listEdges:
      if actual in edge:
        if edge[0] == actual:
          adj.append(edge[1])
        else:
          adj.append(edge[0])

    for node in adj:
      if not parcouru[node]:
        parcouru[node] = True
        diametre.append(node)

    actual = diametre[-1]

  return diametre

#----------------------------------------------------------------------#
# On lance la fonction
if __name__ == '__main__':
  Main()

