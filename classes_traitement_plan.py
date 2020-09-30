"""
Module contenant les classes utiles au traitement du plan étudié :
CouleurSpeciale, Plan
auteur : cmarichal
"""

from typing import Tuple
import matplotlib.image as mpimg
import numpy as np
from math import floor
from enum import Enum


class CouleurSpeciale(Enum):
    """Enumération des codes des pixels spéciaux"""
    ROUGE = [237, 28, 36, 255]
    ROSE = [255, 174, 201, 255]
    BLEU = [63, 72, 204, 255]
    VIOLET = [163, 73, 164, 255]
    NOIR = [0, 0, 0, 255]


class Plan:
    """Image du réseau étudié"""

    def __init__(self, chemin: str, echelle: int = 1):
        self.image = mpimg.imread(chemin)
        self.image_copie = np.copy(self.image)
        self.image_255 = self.mpimg_to_RGB()
        self.echelle = echelle

    def mpimg_to_RGB(self):
        """
        Transforme une image matplotlib en une image PIL
        C'est à dire une matrice de listes de 3 éléments RGB entre 0 et 1
        et une matrice de listes de 3 éléments RGB entre 0 et 255
        """
        matRGB = []
        for i in range(len(self.image)):
            Li = []
            for j in range(len(self.image[0])):
                Lij = []
                for k in range(len(self.image[0][0])):
                    Lij.append(int(self.image[i][j][k] * 255))
                Li.append(Lij)
            matRGB.append(Li)
        matRGB = np.array(matRGB)
        return matRGB

    def verifLignePaint(self, S1: Tuple[int, int], S2: Tuple[int, int]) -> bool:
        """verifie si une arete existe entre 2 sommets dans un graphe"""

        def f(x, S1: Tuple[int, int] = S1, S2: Tuple[int, int] = S2) -> float:
            """construit l'unique fonction affine passant par les 2 points donnés"""
            if S1[0] != S2[0]:
                a = ((S1[1] - S2[1]) / (S1[0] - S2[0]))
                b = S1[1] - a * S1[0]
                return a * x + b

        derniereCouleur = CouleurSpeciale.ROUGE.value  # on part d'un pixel rouge (sommet)
        Dx = S2[0] - S1[0]  # distance entre les pixels sur x
        Dy = S2[1] - S1[1]  # distance entre les pixels sur y
        n = abs(Dx) + abs(Dy)  # nb de pt suffisant (inegalite triangulaire)

        signey = 1  # oriente le tracé de la fonction
        if Dy < 0:
            signey = -1

        compteur = 0

        for k in range(n + 1):
            if Dx != 0:  # qd la fonction existe, on la trace
                coord = (S1[0] + (k / n) * Dx, f(S1[0] + (k / n) * Dx))
            else:  # sinon on suit l'axe des ordonnees
                coord = (S1[0], S1[1] + signey * k)
            a = floor(coord[0])  # approximation au pixel près
            b = floor(coord[1])

            # si un pixel de la ligne n'est pas un sommet, une zone de sommet ou un arc ou un indice de feu rouge
            if list(self.image_255[a][b]) not in (CouleurSpeciale.ROUGE.value, CouleurSpeciale.BLEU.value,
                                                  CouleurSpeciale.NOIR.value, CouleurSpeciale.ROSE.value):
                return False
            # si on a franchi 2 zones de sommets
            if compteur > 5:
                return False

            # si on change de couleur de pixel par rapport au précédent
            if not (list(self.image[a][b]) == derniereCouleur):
                compteur += 1
                derniereCouleur = list(self.image[a][b])

        return True
