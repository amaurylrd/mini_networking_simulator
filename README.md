# Simulation et Analyse des métriques dans un réseau sans 



## Présentation du sujet d'étude


### Objectif de la simulation

Comparer des solutions de routages capables de trouver (et choisir) le meilleur des chemin dans un système simple mais considérant des métriques différentes (parmis lesquels meilleur débit moyen, plus faible encombrement, plus court chemin, etc).

### Consigne

Examiner leurs performance sur différentes scénarii et conlure. <br>
Poursuivre en élaborant une solution combinant les différents avantages de chacune des solutions testées.


### Protcoles

Les différentes métriques et protocoles implémentés sont : 


| N° | Nom du protocol         | Description de l'algorithme |
| :- |:----------------------: | :-------------------------- |
| 0  | OLSR                    | le meilleur débit moyen     |
| 1  | SHORTEST_PATH           | le plus court chemin        |
| 2  | LSOR                    | le meilleur débit moyen (en fonction des conditions radio) |
| 3  | MAX_BOTTLENECK          | le plus grand goulot d'étranglement |
| 4  | FASTEST_BUFFER          | le buffer le plus rapide (dont le premier paquet est le plus récent)   |
| 5  | EMPTIEST_BUFFER         | le buffer le moins rempli   |
| 6  | HYDRBID | la moyenne des élections avec SHORTEST_PATH, LSOR, MAX_BOTTLENECK, FASTEST_BUFFER |


### Modélisation

Le programme lance autant de simulations qu'il y a de  protocoles, toutes sur la même topologie initiale. Donc chaque protocole a son instance du réseau dédiée dans laquelle à chaque tick sont générés des paquets depuis les sources vers leur destination. Le nombre de paquets créés varie selon la charge moyenne – ce nombre est tiré aléatoirement entre zero et deux fois la charge.

La simulation est temps discret, elle dure un nombre pré-déterminé de ticks. En principe, un tick représente la variation entre deux états consécutifs mais, ici, c'est l'unité de temps de la simulation. En effet, le nombre de tick de la simulation correspond au nombre de générations. Plus concrètement, un tick représente aussi le temps d'un saut entre deux noeuds du réseau. C'est aussi un outil de mesure, par exemple, les paquets sont estampilés à leur création afin de calculer de délai une fois à destination.

La route que vont emprunter les paquets est décidée en fonction du protocole de routage, soit au début de la simulation, soit depuis les noeuds pour chaque couple (source, destination). Les buffers des noeuds sont des files FIFO dont l'ordre est respecté inconditionnellement.

Les débits sont tirés suivant une loi normale, autour d'une moyenne liée à la topologie pour prendre en compte les conditions radio dans le réseau. Ces tirges aléatoires sont indépendents entre les différents réseaux de la simulation.

#### Simplifications

- Nous considérons que tous les paquets sont de même taille pour faciliter les statistiques (afin de ne pas avoir à  faire de moyenne pondérée).
- De même, les paquets sont rangés dans des files FIFO de capacité infinie.

## Résultats

## Analyse

## Conclusion
