#Prévision des congestions en milieu urbain

##Présentation

Ce petit projet a pour objectif de modéliser un réseau urbain très simplement à l'aide d'automates cellulaires afin de pouvoir prédire les arcs urbains propices à la formation de congestions routières.

##Fonctionnement

Le programme prend une image PNG d'un plan pré-formaté en entrée puis crée un graphe non-orienté correspondant au réseau étudié. Ensuite il place un certain de nombre de véhicules sur le réseau dont les itinéraires sont estimés à l'aide de l'algorithme du plus court de chemin de Dijkstra (variante A*). Enfin une petite simulation sur une minute est jouée grâce au module animation de matplotlib.

