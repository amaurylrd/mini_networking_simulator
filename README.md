# Simulation et Analyse des métriques dans un réseau 5G

## Note developpeur

### Intégration

Version de python utilisé : `Python 3.10.2`

Ci-dessous, la liste des principales librairies utilisées :
1. [numpy](https://numpy.org/) pour la génération de nombre pseudo-aléatoire ;
2. [pandas](https://pandas.pydata.org/) pour la lecture des scénarii au format csv ;
3. [network](https://networkx.org/) pour la manpilation de graph ;
4. [matplotlib.pyplot](https://matplotlib.org/) pour la visualisation des données sous formes de graphiques.


### Démarrage

La méthode main est contenue dans le fichier [sources/main.py](./sources/main.py). C'est le fichier d'entrée pour lancer l'applicaton : `Usage: python sources/main.py <scenario> <options*>`.


*scenario*: Le nom du fichier csv (sans extension). Le graph est construit à partir des données de la topolgie fournies via cet argument. Le fichier doit être dans le repertoire ressources/dataframes/.

*options*: Pour le moment, seule l'option *time* est impactante qui indique la durée des simulations. (Si pas renseignée, la boucle tourne à l'infini).

exemple: `python sources/main.py scenario_test2 time=500`

### Architecture

Ci-dessous, la décomposition en liste des dossiers pour une meilleure compréhension de l'architecture du projet.

1. sources/ : encapsule les fichiers de code ;
2. ressources/dataframes : répertorie toutes les topologies pour les différentes simulations ;
3. ressources/results : les graphiques sont rendus sous la forme d'image placées dans ce repertoire.

-----------------

## Présentation du sujet d'étude

### Objectif de la simulation

Comparer des solutions de routages capables de trouver (et choisir) le meilleur des chemins dans un système simple mais considérant des métriques différentes (parmis lesquels meilleur débit moyen, plus faible encombrement, plus court chemin, etc).

### Consigne

- Examiner leurs performance sur différents scénarii et conlure.
- Poursuivre en élaborant une solution combinant les différents avantages de chacune des solutions testées.

<br>

### Modélisation

Le programme lance **autant de simulations qu'il y a de  protocoles, toutes sur la même topologie initiale**. Donc chaque protocole a son instance du réseau dédiée dans laquelle à **chaque tick sont générés des paquets depuis les sources vers leur destination**. Le nombre de paquets créés varie selon la charge moyenne – ce nombre est tiré aléatoirement entre zero et deux fois la charge. En somme, **la production de paquets varie autour de cette moyenne afin de recréer des problèmes de congestion temporaire**.

La simulation est temps discret, elle dure un nombre pré-déterminé de ticks (cf. Démarrage). En principe, un tick représente la variation entre deux états consécutifs mais, ici, c'est l'unité de temps de la simulation. En effet, le nombre de tick de la simulation correspond au nombre de générations de paquets. Plus concrètement, un tick représente aussi le temps d'un saut entre deux noeuds du réseau. C'est aussi un outil de mesure, par exemple, les paquets sont estampilés à leur création afin de calculer le délai une fois à destination.

La **route que vont emprunter les paquets est décidée en fonction du protocole de routage**, soit au début de la simulation, soit depuis les noeuds à chaque tick, pour chaque couple (source, destination). Les buffers des noeuds sont des files FIFO dont l'ordre est respecté inconditionnellement.

Les **débits sont tirés suivant une loi normale, autour d'une moyenne** fournie dans les données de la topologie pour imiter naïvement les conditions radio dans le réseau. À noter que ces tirges aléatoires sont indépendents entre les différents réseaux de la simulation.

#### Simplifications

En contraste avec le routage dans le vie réelle, on est obligé de faire plusieurs simplifications pour facilitier les simulations :
- Nous considérons que tous les paquets sont de même taille pour faciliter les statistiques (afin de ne pas avoir à faire de moyenne pondérée) ;
- De même, les paquets sont rangés dans des files FIFO de capacité infinie.

### Protocoles

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

## Résultats

Les résultats sont présentés sur des images découpées en quatre parties :
1. (en haut à gauche) la topologie du réseau avec quand le protocole le permet les routes décidées à l'initialisation ;
2. (en haut à droite) un graphique qui montre le délai moyen par utilisateur (la ligne bleue représente la limite de satisfaction) ;
3. (en bas à gauche) un graphique qui montre le pourcentage de paquets à destination par utilisateur ;
4. (en bas à droite) un graphique qui montre la moyenne de paquets dans les buffers.

![TEST3_FASTEST_BUFFER](./ressources/results/test3_FASTEST_BUFFER.png)

## Analyse

Toutes les simulations comme ci-dessus, tournent sur 500 ticks et la génération de paquets va de 10 à 100 avec un pas de 5.

### OLSR

Innocemment, le protocole OLSR est le premier qui nous vient en tête. Il a l'avantage d'être très simple à comprendre et très évoquant. En réalité, bien qu'il ne prenne pas en compte les débits réels ou les goulots d'étranglement, il maintient une certaine stabilité face à la surchage pour les topologies simples. En revanche, dès qu'on introduit plusieurs émetteurs, il est vite dépassé. Le défaut majeur de mon implémentation pour ce protocole et lié à son fonctionnement : il peut favoriser un chemin très long car il a une meilleur moyenne. Aussi, OLSR fait partie des protocoles qui doivent retenir leur route dans une table de routage, ces protocoles sont très statiques.

![TEST3_OLSR](./ressources/results/test3_OLSR.png)

On peut voir dans cette simulation, que les deux émetteurs vont prendre quasiment le même chemin, ce qui conduit à congestioner très rapidement le réseau.
On remarque aussi que la simpliciter du protocole et son routage mono-route, le rend plus enclin aux situations de congestion.
Sur une variante du même scénario avec une seule source, on peut voir que le protocole a de meilleurs résulats.

![TEST4_OLSR](./ressources/results/test4_OLSR.png)

### SHORTEST_PATH

Prendre la route la plus courte est aussi un protocole simple à réfléchir. Dans notre cas, les distances sont directement liées au nombre de sauts, puisque tous les noeuds sont distants d'un tick. Néanmoins, ce protocole ne prend pas du tout en considération les débits. Il serait donc très facile de le même en défaut sur une topologie qui associe le plus court chemin à un débit ridiculement faible.

![TEST4_OLSR](./ressources/results/test4_SHORTEST_PATH.png)

### LSOR

Le protocole LSOR, pour rappel, s'appuie sur les débits à l'instant t, pour choisir la meilleure route. Pour choisir, cette route, il dispose d'une valeur qui représente la portée, arbitrairement fixée à 1 (avec une portée de 0, il choisirait de manière random). Cette sélection est réitérée à chaque tick, ce qui le rend un peu plus lent. Néanmoins, il présente de meilleur résultat qu'OLSR puisqu'il peut changer de route en fonction des conditions radios. Malheureusement, il ne prend pas en compte les débits sur toute la route, ce qui le rend facile à fausser, ni de l'occupation des buffeurs.

Ci-dessous, les résultats pour les protocoles OLSR (la première image) et LSOR (la seconde image) en vis à vis. 

![SCENARIO_TEST2_OLSR](./ressources/results/scenario_test2_OLSR.png)

![SCENARIO_TEST2_LSOR](./ressources/results/scenario_test2_LSOR.png)

### MAX_BOTTLENECK

Ce protocole s'appuie sur les valeurs des débits pour choisir son chemin. On pourrait donc imaginer deux versions de ce protocoles, une sur les débits moyens et une autre sur les débits réels. En pratique, il sélectionne la route à qui a le plus grand goulot d'étranglement pour maximiser le flux. Dans son implémentation, cette route est décidée à l'initialisation de la connexion. Cet algortihme est très fluide et permet d'utiliser au mieux les débits de la topologie. Il montre de très bon résultats sur le taux d'occupation des buffers.

![SCENARIO_TEST2_MAX_BOTTLENECK](./ressources/results/scenario_test2_MAX_BOTTLENECK.png)

### FASTEST_BUFFER

Ce protocole est intéressant car il équilibre la charge dans le réseau. Il va choisir la route qui est la plus rapide en regardant l'ancienneté des paquets dans les buffers (plus précisément, le tick de création du premier paquet en tête de file). En effet, quand un noeud est trop long à faire le relai, il est laissé le temps qu'il évacue les paquets encombrants. Le protocole propose ainsi une solution avec du multi-path, et une réponse à la congestion. On pourrait pourquoi pas imaginer une variante qui prendrait en compte le temps passer dans le buffer.

![TEST3_FASTEST_BUFFER](./ressources/results/test3_FASTEST_BUFFER.png)

En réalité, ce protocole peut certes répondre à des problème de surcharge, mais il est vite dépassé quand il manque de chemins ou dans des topologies avec plusieurs sources.

### EMPTIEST_BUFFER

Ce protocole propose lui aussi une approche basé sur le taux d'occupation dans les buffers. Dans ce protocole particulier, la route est choisie directement en fonction de ce taux d'occupation des buffers. En théorie, plus un buffer est vide, plus il est efficace donc il cible les voisins qui ont les buffers les plus vides. En conclusion, il s'adapte en fonction des conditions du réseau en temps réel pour essayer d'équilibrer la charge sur plusieurs routes.

![TEST3_EMPTIEST_BUFFER](./ressources/results/test3_EMPTIEST_BUFFER.png)

<br>
## Conclusion

### SOLUTION HYBRIDE

```python
def __hybrid_solution(self, src, dst):
        funcs = {
            lambda src, dst, paths: self.__lsor(src, dst, 2, paths),
            self.__path_max_bottleneck,
            self.__path_fastest_buffer
        }
        
        paths = sorted(nx.all_simple_paths(self._graph, src, dst), key=len)
        ranks = [ i for i in range(len(paths)) ] # for the shortest path
        
        for func in funcs:
            tmp = paths[:]
            for i in range(len(ranks)):
                path = func(src, dst, tmp)
                ranks[paths.index(path)] += i
                tmp.remove(path)
            
        return paths[ranks.index(min(ranks))]
```

Pour la solution hybride, on peut essayer de fusionner les protocoles qui donnent les meilleurs résultats. On peut même pousser leur performances, par exemple, en fixant la portée du protocole LSOR à deux voisins ou en implémentant le protocole MAX_BOTTLENECK à chaque tick. Logiquement, cet algorithme est bien plus complexe, et demande beaucoup plus de ressource à mettre en oeuvre. Néanmoins, il n'est pas meilleur que les autres algorithmes aux statistiques.

![SCENARIO_TEST2_HYBRID](./ressources/results/scenario_test2_HYBRID.png)

![SCENARIO_TEST2_ALL](./ressources/results/scenario_test2_ALL.png)

En conclusion, on peut dire qu'il est très difficile de choisir un protocole pour un réseau. Tout dépend de la topologie et du contexte. Il faut prendre en compte le nombre d'émetteurs, le nombre de noeuds, les débits, la charge dans le réseau... Il serait peut-être intéressant en pratique de changer de protocole en fonction de la charge.
Enfin, on a pu voir que proposer une solution hybride n'est pas des plus simples, les algortihmes les plus simples sont parfois aussi bons.
