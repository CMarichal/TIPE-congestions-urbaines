"""
Module contenant les classes utiles à la modélisation sous forme de graphe :
Sommet, Arc, Graphe
auteur : cmarichal
"""

from typing import Tuple, List
from math import floor
import numpy as np

from classes_traitement_plan import CouleurSpeciale, Plan


class Sommet:
    """Sommet ayant une position et un numéro"""

    def __init__(self, numero: int, pos: Tuple[int, int], majeur: bool = False):
        self.pos = pos
        self.numero = numero
        self.majeur = majeur


class Arc:
    """Arc comportant 2 sommets, une longueur et une route"""

    def __init__(self, sommet_depart: Sommet, sommet_arrive: Sommet, longueur: int):
        self.sommets = (sommet_depart, sommet_arrive)
        self.longueur = longueur


class Graphe:
    """Graphe mathématique comportant la liste des sommets et la matrice d'adjacence"""

    def __init__(self):
        self.matrice_adjacence = np.array([])
        self.liste_sommets = []

    @staticmethod
    def graphe_from_plan(plan: Plan):
        """retourne le graphe associé à une image prétraitée"""
        nouveau_graphe = Graphe()
        sommets, coefprop = Graphe.cherche_sommets(plan)
        nouveau_graphe.liste_sommets = sommets

        Gr = []
        for i in range(len(sommets)):  # crée une matrice de zéros d'une taille adaptée
            Gr.append([0] * len(sommets))
        for i in range(len(sommets) - 1):
            for k in range(i + 1, len(sommets)):
                if plan.verifLignePaint(sommets[i].pos, sommets[k].pos):  # vérifie que 2 sommets sont reliés par un arc
                    x = sommets[i].pos[0] - sommets[k].pos[0]
                    y = sommets[i].pos[1] - sommets[k].pos[1]
                    Gr[i][k] = floor(coefprop * np.sqrt(x ** 2 + y ** 2))  # distance entre les sommets
                    Gr[k][i] = Gr[i][k]  # matrice symetrique
                else:
                    Gr[i][k] = -1  # sommet inaccessible
                    Gr[k][i] = -1
        nouveau_graphe.matrice_adjacence = np.array(Gr)
        return nouveau_graphe

    @staticmethod
    def cherche_sommets(plan: Plan) -> Tuple[List[Sommet], float]:
        """repère les sommets/pixels rouges"""
        sommets = []
        echelle = []
        for i in range(len(plan.image_255)):
            for j in range(len(plan.image_255[0])):
                code_pixel = list(plan.image_255[i][j])
                if code_pixel == CouleurSpeciale.ROUGE.value:
                    sommets.append(Sommet(numero=len(sommets), pos=(i, j)))
                elif code_pixel == CouleurSpeciale.ROSE.value:
                    sommets.append(Sommet(numero=len(sommets), pos=(i, j), majeur=True))
                elif code_pixel == CouleurSpeciale.VIOLET.value:
                    echelle.append((i, j))
        coefprop = plan.echelle / (echelle[1][1] - echelle[0][1])  # coefficient de propotionnalité pixels/metres
        return sommets, coefprop

    def get_liste_arcs_graphe(self) -> List[Tuple[int, int]]:
        """renvoie la liste de tous les arcs"""
        L = []
        for i in range(len(self.matrice_adjacence)):
            for j in range(len(self.matrice_adjacence[0])):
                if self.matrice_adjacence[i][j] != 0 and self.matrice_adjacence[i][j] != -1:
                    L.append((i, j))
        return L

    def get_liste_sommets_majeurs(self) -> List[Sommet]:
        """Renvoie la liste des sommets majeurs"""
        sommets_majeurs = []
        for sommet in self.liste_sommets:
            if sommet.majeur:
                sommets_majeurs.append(sommet)
        return sommets_majeurs
