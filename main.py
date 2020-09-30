"""
Fichier principal de la simulation à l'aide d'automates cellulaires
auteur : cmarichal
"""
from classes_traitement_plan import Plan
from classes_graphes import Graphe
from classes_simulation import Reseau
from classes_animation import AnimationPlan

# Programma principal

echelle_carte = 10                           # distance entre les deux pixels violets en mètres
plan = Plan('plans/Test_ligne.png', echelle=echelle_carte)  # importer le plan

graphe = Graphe.graphe_from_plan(plan)  # Fabrique le graphe

reseau = Reseau(graphe)  # construit le réseau de simulation

# création d'un trafic
reseau.init_circulation(nbvoitures=250)
reseau.init_priorites()  # définir les priorités

animation_plan = AnimationPlan(plan.image_255)
animation_plan.animer_reseau(reseau, reseau.avancee_reseau)
