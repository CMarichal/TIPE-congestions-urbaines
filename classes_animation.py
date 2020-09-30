"""
Module contenant la classe AnimationPlan permettant d'animer le réseau sur le plan
auteur: cmarichal
"""

from matplotlib import pyplot as plt
from matplotlib import animation as animation
from classes_simulation import Reseau
from typing import List, Tuple, Callable
from math import sqrt, cos, sin, atan
import numpy as np


class AnimationPlan:

    def __init__(self, fond, tmax: int = 500):
        self.tmax = tmax
        self.fond = fond

    def animer_reseau(self, reseau: Reseau, fonction_avancer: Callable) -> None:
        """Méthode lançant l'animation du réseau"""

        fig, ax = plt.subplots()
        ax.imshow(self.fond)

        t = 0
        data = []  # liste des plans avec les voitures dessus
        while t < self.tmax:
            if t % 4 == 0:
                data.append(self.positions_voitures_sur_plan(reseau))
            fonction_avancer()
            t += 1
        data = np.array(data)

        def animate2(t: int):
            """fonction affichant les plans les unes après les autres sous forme d'animation"""
            plt.cla()
            for i in range(len(data[t])):
                plt.plot(data[t][i][0], data[t][i][1], 'g.')
            plt.title("Temps = " + str(t / 2) + "s")
            plt.imshow(self.fond)
            return

        ani = animation.FuncAnimation(fig, animate2, frames=self.tmax // 4, interval=10, repeat=0)
        plt.show()

    @staticmethod
    def positions_voitures_sur_plan(reseau: Reseau, ecart: int = 3) -> List[Tuple[float, float]]:
        """Place les voitures sur le plan"""

        posVoitures = []
        for v in reseau.circulation.liste_voitures:

            pos_sommet_debut_route = v.route.sommets[0].pos
            pos_sommet_fin_route = v.route.sommets[1].pos

            # les sommets sont juste l'un en dessous de l'autre
            if pos_sommet_debut_route[1] == pos_sommet_fin_route[1]:
                Dy = pos_sommet_fin_route[0] - pos_sommet_debut_route[0]
                pas = Dy / (v.route.longueur + 2)
                epsilon = 1
                if Dy < 0:
                    epsilon = -1
                position = [pos_sommet_debut_route[1] - epsilon * ecart,
                            pos_sommet_debut_route[0] + pas * (v.pos_route + 1)]

            # les sommets sont juste l'un à côté de l'autre
            elif pos_sommet_debut_route[0] == pos_sommet_fin_route[0]:
                Dy = pos_sommet_fin_route[1] - pos_sommet_debut_route[1]
                pas = Dy / (v.route.longueur + 2)
                epsilon = 1
                if Dy < 0:
                    epsilon = -1
                position = [pos_sommet_debut_route[1] + pas * (v.pos_route + 1),
                            pos_sommet_debut_route[0] + epsilon * ecart]
            else:
                Dy = pos_sommet_fin_route[0] - pos_sommet_debut_route[0]
                Dx = pos_sommet_fin_route[1] - pos_sommet_debut_route[1]
                D = sqrt(abs(Dy ** 2 + Dx ** 2))
                delta1 = ecart * sin(atan(Dx / Dy))
                delta2 = ecart * cos(atan(Dx / Dy))
                pas = D / (v.pos_route + 2)
                adjReduite = ((v.pos_route + 1) * pas / D) * Dy
                oppReduite = ((v.pos_route + 1) * pas / D) * Dx
                if Dy > 0 and Dx > 0:
                    delta2 = -abs(delta2)
                elif Dy < 0 and Dx > 0:
                    delta2 = abs(delta2)
                    delta1 = abs(delta1)
                elif Dy < 0 and Dx < 0:
                    delta1 = -abs(delta1)
                elif Dy > 0 and Dx < 0:
                    delta1 = -abs(delta1)
                    delta2 = -abs(delta2)

                position = (pos_sommet_debut_route[1] + oppReduite + delta2,
                            pos_sommet_debut_route[0] + adjReduite + delta1)
            posVoitures.append(position)

        return posVoitures
