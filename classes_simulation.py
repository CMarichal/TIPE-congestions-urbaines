"""
Module contenant les classes utiles à la simulation :
Intersection, Route, Circulation et Reseau
auteur : cmarichal
"""
from classes_graphes import *
from typing import Tuple
from random import choice, randrange
from dijkstra import Dijkstra_Astar
import fonctions_utilitaires


class Intersection(Sommet):
    """Sommet évolué comportant la notion de priorité"""

    def __init__(self, numero: int, pos: Tuple[int, int], majeur: bool = False):
        super().__init__(numero, pos, majeur)
        self.priorites = []

    @staticmethod
    def intersection_from_sommet(sommet: Sommet):
        intersection = Intersection(sommet.numero, sommet.pos, sommet.majeur)
        intersection.priorites = None
        return intersection


class Route(Arc):
    """Arc comportant 2 sommets, une longueur et une simulation de route"""

    def __init__(self, sommet_depart: Sommet, sommet_arrive: Sommet, longueur: int):
        super().__init__(sommet_depart, sommet_arrive, longueur)
        self.grille = [None] * longueur

    def __getitem__(self, item):
        return self.grille[item]

    def __setitem__(self, key, value):
        self.grille[key] = value

    def is_voiture_a_intersection(self) -> bool:
        """vérifie s'il y a une voiture à l'intersection"""
        return self.grille[-1] is not None

    def is_voiture_au_debut_arc(self) -> bool:
        """vérifie s'il y a une voiture à l'intersection"""
        return self.grille[0] is not None


class Voiture:
    """Voiture a un numéro, un arc, une position relative à l'arc et une vitesse"""

    def __init__(self, numero: int, route: Route, pos_route: int, vitesse: int):
        self.numero = numero
        self.pos_route = pos_route
        self.route = route
        self.vitesse = vitesse
        self.sommet_depart = None
        self.sommet_arrivee = None
        self.chemin = None
        self.a_agi = False

    def avancer(self) -> None:
        """avance la voiture d'un cran sur la route"""
        self.route[self.pos_route] = None
        self.pos_route += 1
        self.route[self.pos_route] = self
        self.a_agi = True

    def prendre_nouvelle_route(self, nouvelle_route: Route) -> None:
        """Fait prendre une route à une voiture"""
        if self.route is not None:
            self.route[self.pos_route] = None
        self.route = nouvelle_route
        nouvelle_route[0] = self
        self.pos_route = 0
        self.a_agi = True

    def arriver(self) -> None:
        self.route[self.pos_route] = None
        self.pos_route = None
        self.route = None
        self.a_agi = True


class Circulation:
    """Comporte des informations sur les voitures circulant"""

    def __init__(self):
        self.dict_listes_attente = {}
        self.liste_voitures = []
        self.nb_voitures = 0
        self.nb_voitures_arrivees = 0

    def get_nb_voitures_total(self) -> int:
        nb_voitures = len(self.liste_voitures)
        nb_voitures += sum([len(file) for file in self.dict_listes_attente.values()])
        return nb_voitures


class Reseau(Graphe):
    """Réseau consistant en un graphe amélioré comportant des informations supplémentaires"""

    def __init__(self, graphe: Graphe):
        super().__init__()
        self.liste_sommets = graphe.liste_sommets
        self.matrice_adjacence = graphe.matrice_adjacence
        self.matrice_route = []
        self.dict_intersection = []
        self.circulation = Circulation()

        for i in range(len(graphe.matrice_adjacence)):
            ligne_i = []
            for j in range(len(graphe.matrice_adjacence[0])):
                if graphe.matrice_adjacence[i][j] in (-1, 0):
                    ligne_i.append(None)
                else:
                    ligne_i.append(Route(self.liste_sommets[i], self.liste_sommets[j], graphe.matrice_adjacence[i][j]))
            self.matrice_route.append(ligne_i)

    def init_circulation(self, nbvoitures: int) -> None:
        """Génère une prévision de circulation de manière aléatoire"""

        for i in range(nbvoitures):
            voiture = Voiture(i, None, None, vitesse=1)
            sommet_entree = choice(self.liste_sommets)
            sommet_sortie = choice(self.liste_sommets)

            while sommet_entree == sommet_sortie:  # Autant ne pas prendre la route si c'est pour rester chez soi
                sommet_sortie = choice(self.liste_sommets)

            voiture.chemin = Dijkstra_Astar(self.matrice_adjacence, sommet_entree.numero, sommet_sortie.numero, self.liste_sommets)[0]
            premiere_route = self.matrice_route[sommet_entree.numero][voiture.chemin[1]]
            voiture.pos_route = randrange(premiere_route.longueur)

            compteur_essai_de_placement = 0
            while premiere_route[voiture.pos_route] is not None \
                    and compteur_essai_de_placement < premiere_route.longueur:
                voiture.pos_route = randrange(premiere_route.longueur)
                compteur_essai_de_placement += 1
            # Cas où il serait impossible de ne pas superposer deux voitures déjà existantes : l'arc est complètement occupé
            if compteur_essai_de_placement == premiere_route.longueur:
                print("Le générateur a échoué à placer la voiture n°" + str(i))
                print("Arret de la génération")
                return
            print("Génération en cours : " + str(int((i / nbvoitures) * 100)) + "%")
            voiture.route = premiere_route
            voiture.sommet_depart = sommet_entree
            voiture.sommet_arrivee = sommet_sortie
            self.circulation.liste_voitures.append(voiture)
            self.matrice_route[sommet_entree.numero][voiture.chemin[1]][voiture.pos_route] = voiture
        return

    def init_priorites(self) -> None:
        """Génère les priorités pour chaque intersection (sens antihoraire)"""
        
        self.dict_intersection = {sommet.numero: Intersection(sommet.numero, sommet.pos, sommet.majeur) for sommet in self.liste_sommets}

        liste_arcs_graphe = self.get_liste_arcs_graphe()
        
        for i, intersection_i in self.dict_intersection.items():  # selection des sommets reliés et calcul des angles
            au_sommet_i = []
            for j in range(len(liste_arcs_graphe)):
                if liste_arcs_graphe[j][0] == i:
                    au_sommet_i.append([liste_arcs_graphe[j][1],
                                        fonctions_utilitaires.angle_sommets(intersection_i.pos,
                                                                            self.liste_sommets[liste_arcs_graphe[j][1]].pos)])

            # tri selon l'angle
            
            au_sommet_i.sort(key=lambda x: x[1])
            priorites_en_i = [x[0] for x in au_sommet_i]
            self.dict_intersection[i].priorites = priorites_en_i
        return

    def regle184(self, voiture: Voiture) -> bool:
        """Fait avancer la voiture dans le reseau selon la regle 184 des automates cellulaires"""

        if voiture.pos_route + 1 == voiture.route.longueur:  # cas case devant intersection
            cheminIntersectionLibre = self.gestion_intersection(voiture)
            if cheminIntersectionLibre:  # la case devant l'intersection a été dégagée
                return True
            else:
                return False
        else:  # il existe une case devant
            if voiture.route[voiture.pos_route +1] is None:  # cas case devant libre
                voiture.avancer()
                return True
            else:  # cas case devant occupée
                voiture_devant = voiture.route[voiture.pos_route+1]
                if not voiture_devant.a_agi:
                    cheminLibre = self.regle184(voiture_devant)
                    if cheminLibre:
                        voiture.avancer()
                        return True
                    else:  # la voiture devant n'a pas bougé
                        voiture.a_agi = True
                        return False
                else:  # la voiture de devant n'a pas la possibilite de bouger
                    voiture.a_agi = True
                    return False

    def gestion_intersection(self, voiture: Voiture, saturation: int = 0) -> bool:
        """Gère les intersections à l'aide de la règle de priorite antihoraire"""

        sommet_intersection = self.dict_intersection[voiture.route.sommets[1].numero]
        if sommet_intersection.numero == voiture.sommet_arrivee.numero:  # si la voiture est arrivée
            voiture.arriver()
            self.circulation.liste_voitures.pop(self.circulation.liste_voitures.index(voiture))
            self.circulation.nb_voitures_arrivees += 1
        else:
            prochain_sommet_numero = voiture.chemin[voiture.chemin.index(sommet_intersection.numero) + 1]
            prochaine_route = self.matrice_route[sommet_intersection.numero][prochain_sommet_numero]
            priorites = sommet_intersection.priorites

            if priorites[-1] != prochain_sommet_numero:  # forme circulaire des priorites
                priorite_a = priorites[priorites.index(prochain_sommet_numero) + 1]
            else:
                priorite_a = priorites[0]

            route_prioritaire = self.matrice_route[priorite_a][sommet_intersection.numero]

            if route_prioritaire[-1] is not None:  # s'il existe une voiture prioritaire
                voiture_prioritaire = route_prioritaire[-1]
                if not voiture_prioritaire.a_agi and saturation != len(priorites)-1:  # si tout le monde n'attend pas que qqn se lance
                    self.gestion_intersection(voiture_prioritaire, saturation+1)

            if prochaine_route[0] is not None:  # s'il existe une voiture là où l'on souhaite aller
                voiture_bouchant_arc = prochaine_route[0]
                if not voiture_bouchant_arc.a_agi:
                    intersection_libre = self.regle184(voiture_bouchant_arc)
                    if not intersection_libre:  # on ne peut pas se lancer
                        voiture.a_agi = True
                        return False
                    else:  # la voiture bouchant s'est déplacée
                        voiture.prendre_nouvelle_route(prochaine_route)
                        return True
                else:  # la voiture bouchant ne peut pas bouger
                    voiture.a_agi = True
                    return False
            else:  # pas de voiture bouchant ou prioritaire
                voiture.prendre_nouvelle_route(prochaine_route)
                return True

    def avancee_reseau(self) -> None:
        """avance le temps d'un cran"""
        self.ajout_circulation_depuis_liste_attente()
        for voiture in self.circulation.liste_voitures:
            if not voiture.a_agi:
                self.regle184(voiture)
        for voiture in self.circulation.liste_voitures:
            voiture.a_agi = False

    def ajout_circulation_depuis_liste_attente(self) -> None:
        """Ajoute des voitures dans le réseau selon les files d'attente"""

        if self.circulation.dict_listes_attente == {}:
            self.circulation.dict_listes_attente = {i: [] for i in range(len(self.liste_sommets))}

        for file in self.circulation.dict_listes_attente.values():  # on traite les voitures en file d'attente
            if len(file) != 0:
                voiture_a_ajouter = file[0]
                premiere_route = self.matrice_route[voiture_a_ajouter.chemin[0]][voiture_a_ajouter.chemin[1]]
                if premiere_route[0] is None:  # s'il y a une place libre, on la prend (les arrivant sont prioritaires)
                    voiture_a_ajouter.route = premiere_route
                    voiture_a_ajouter.pos_route = 0
                    premiere_route[0] = voiture_a_ajouter
                    self.circulation.liste_voitures.append(voiture_a_ajouter)
                    file.pop(0)

        sommets_majeurs = self.get_liste_sommets_majeurs()
        for sommet_majeur_entree in sommets_majeurs:  # on en rajoute de nouvelles de manière aléatoire
            facteur_aleatoire = randrange(100)
            if facteur_aleatoire == 1:
                sommet_majeur_sortie = choice(sommets_majeurs)
                while sommet_majeur_entree == sommet_majeur_sortie:  # Autant ne pas prendre la route si c'est pour rester chez soi
                    sommet_majeur_sortie = choice(sommets_majeurs)
                chm = Dijkstra_Astar(self.matrice_adjacence, sommet_majeur_entree.numero, sommet_majeur_sortie.numero, self.liste_sommets)[0]
                voiture_a_ajouter_en_attente = Voiture(self.circulation.get_nb_voitures_total()+1, None, None, vitesse=1)
                voiture_a_ajouter_en_attente.chemin = chm
                voiture_a_ajouter_en_attente.sommet_depart = sommet_majeur_entree
                voiture_a_ajouter_en_attente.sommet_arrivee = sommet_majeur_sortie
                self.circulation.dict_listes_attente[sommet_majeur_entree.numero].append(voiture_a_ajouter_en_attente)
        return
