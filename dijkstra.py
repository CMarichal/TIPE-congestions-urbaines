"""
Module contenant la révision A* de l'algorithme de Dijkstra
auteur : cmarichal
"""

from typing import List
from math import sqrt, floor
from random import randrange
from classes_graphes import Sommet


def possibilites(matrice_adjacence: List[List[int]], ch: List[int], long: int) -> List[List[int]]:
    """Renvoie les possibilites de parcours et leur longueurs depuis un chemin"""
    p = matrice_adjacence[ch[-1]]  # selectionne la liste du graphe correspondant au possibilité du haut de la pile du chemin
    possibles = []
    for k in range(len(p)):
        if p[k] > 0 and not (k in ch):  # donne les arcs à distance positive
            possibles.append([ch + [k], p[k] + long])  # on ajoute le sommet possible au chemin et on ajoute la longueur à parcourir au total
    return possibles


def distanceVO(S1: int, S2: int, listeSommets: List[Sommet]) -> float:
    """Calcule la distance à vol d'oiseau entre 2 points"""
    P1 = listeSommets[S1].pos
    P2 = listeSommets[S2].pos
    Dx = abs(P1[0] - P2[0])
    Dy = abs(P1[1] - P2[1])
    return floor(sqrt(Dx ** 2 + Dy ** 2))


def Dijkstra_Astar(matrice_adjacence: List[List[int]], e: int, s: int, liste_sommets: List[Sommet]) -> List[List[int]]:
    """Calcule le chemin le plus court entre 2 points d'un graphe orienté, utilise la modification A*,
    simplifie le calcul à effectuer en travaillant sur le point d'arrivé
    """

    chemins = [[[e], 0]]  # initialisation, on part de l'entree
    while chemins[0][0][-1] != s:  # condition d'arret : le chemin le plus court mene à l'arrivee
        P = possibilites(matrice_adjacence, chemins[0][0], chemins[0][1])
        chemins.pop(0)  # on retire des chemins possibles celui que l'on étudie
        chemins += P  # on ajoute les nouvelles possibilites
        plusCourt = []
        coutHeuristique = []
        for i in range(len(chemins)):  # on crée une liste attribuant à un chemin possible un cout
            coutHeuristique.append(chemins[i][1] + distanceVO(chemins[i][0][-1], s, liste_sommets))
        for i in range(len(chemins)):  # on ajoute les chemins correspondant au minimum de cout
            if coutHeuristique[i] == min(coutHeuristique):
                plusCourt.append(chemins[i])
        while len(plusCourt) > 1:
            plusCourt.pop(randrange(len(plusCourt)))
        j = chemins.index(plusCourt[0])
        chemins.pop(j)
        chemins = [plusCourt[0]] + chemins

    return chemins[0]
