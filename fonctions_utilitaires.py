"""
Contient diverses fonctions utilitaires
auteur : cmarichal
"""

from typing import Tuple
from numpy import angle


def angle_sommets(s1: Tuple[int, int], s2: Tuple[int, int]) -> float:
    """calcule l'argument de l'affixe du vecteur associé à 2 sommets"""
    comp = complex(s2[1] - s1[1], s2[0] - s1[0])
    return angle(comp)



