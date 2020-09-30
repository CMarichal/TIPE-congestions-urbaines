# Prévision des congestions en milieu urbain

## Présentation

Ce petit projet a pour objectif de modéliser un réseau urbain très simplement à l'aide d'automates cellulaires afin de pouvoir prédire les arcs urbains propices à la formation de congestions routières.

## Fonctionnement

Le programme prend une image PNG d'un plan pré-formaté en entrée puis crée un graphe non-orienté correspondant au réseau étudié. Ensuite il place un certain de nombre de véhicules sur le réseau dont les itinéraires sont estimés à l'aide d'un algorithme du plus court de chemin. Enfin une petite simulation sur une minute est jouée grâce au module animation de matplotlib.

### Analyse du plan

Le plan doit comporter un réseau connexe par arcs. Il doit être une image PNG de taille relativement faible (plus petite que 1200x780 pixels). Les arcs sont modélisés par des traits noirs, les sommets par des pixels rouges présents dans des zones bleues. L'échelle du plan est prise graçe à deux pixels violets. Les codes RGB de ces couleurs sont disponibles dans l'énumération des couleurs dans _"classes_traitement_plan.py"_.

Un graphe non-orienté est alors recréé par le programme. Pour cela, pour chaque sommet le programme vérifie qu'il n'y a que des pixels bleus et noirs sur le chemin en ligne droite vers un autre sommet.

### Construction du réseau

Un réseau est ensuite construit à partir de ce graphe. Ce réseau contient des routes qui sont des listes modélisant un pavage de 1m pour chaque emplacement de la liste. Aux intersections, la priorité est donnée dans le sens anti-horaire.

### Simulation

Une circulation est ensuite générée. Une circulation est un ensemble de véhicule circulant sur le réseau. Chaque véhicule ayant une intersection de départ et une d'arrivée. Son trajet étant estimé au plus court à l'aide de l'algorithme du plus court chemun de Dijkstra, ou plus précisément sa variante A*, en prenant comme heuristique la distance à vol d'oiseau entre les sommets considérés et celui d'arrivé.

A chaque incrément temporel, les véhicules avancent selon la règle 184 des automates cellulaires qui consiste principalement à avancer chaque véhicule d'un cran quand la case devant lui est libre.

Les véhicules sont ensuites affichés sur le plan d'origine, permettant la visualisation des lieux de congestion possible.