# Simulation et Analyse des métriques dans un réseau sans 



## Présentation du sujet d'étude


### Objectif de la simulation

Comparer des solutions de routages capables de trouver (et choisir) le meilleur des chemin dans un système simple mais considérant des métriques différentes (parmis lesquels meilleur débit moyen, plus faible encombrement, plus court chemin, etc).

### Consigne

Examiner leurs performance sur différentes scénarii et conlure. Poursuivre en élaborant une solution combinant les différents avantages de chacune des solutions testées.


### Protcoles

Les différentes métriques et protocoles implémentés sont : 


| N° | Nom du protocol         | Description de l'algorithme |
| :- |:-----------------------:| ---------------------------:|
| 0  | OLSR                    | le meilleur débit moyen     |
| 1  | SHORTEST_PATH           | le plus court chemin        |
| 2  | LSOR                    | le meilleur débit moyen (conditions radio) |
| 3  | MAX_BOTTLENECK          | le plus grand goulot d'étranglement        |
| 4  | FASTEST_BUFFER          | le buffer le plus rapide    |
| 5  | EMPTIEST_BUFFER         | le buffer le moins rempli   |
| 6  | HYDRBID | la moyenne des élections avec SHORTEST_PATH, LSOR, MAX_BOTTLENECK, FASTEST_BUFFER |


### Modélisation

Simplifications

Nous considérons que tous les paquets sont de même taille pour faciliter les statistiques (afin de ne pas avoir à  faire de moyenne pondérée).
De même, les paquets sont rangés dans des files FIFO de capacité infinie.


## Résultats

## Analyse

## Conclusion
