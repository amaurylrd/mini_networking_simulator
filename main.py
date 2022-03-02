#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy.random as random

# loop
# plot graphique
# scenario / graph


# mean
# scale

def generate_packages():
    packages = []
    package_size = 10
    
    x = random.randint(0, 5)
    for i in range(x):
        package = { "data": random.randint(0, 2, size=(package_size)) } # generate an n-dimensional array of random bits
        packages.append(package)
    
    return packages


# taille des paquets, fixe ? ou autour d'une moyenne
# nombre de paquets


# https://fr.khanacademy.org/computing/computer-programming/programming-natural-simulations/programming-randomness/a/normal-distribution-of-random-numbers
# https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html

#contraintes
#128 porteuses
#5timeslot sur une trame


# graph -> node chainé à X node

# Sujet 5

# chercher les différents algorithmes
# proposer les scénarios


# chemin métriques
# moyenne, somme ?
# source qui interfaire avec la vraie source/destination pour contrer le meilleur débit
# bottleneck, delai, le plus court
# pathloss... contraintes basiques

# loop
# update simulation cycle = 0 scheduling
# afficher simulation

# generation des sources
# tick en temps discret

# generation paquet (hypothèse taille fixe ou ponderer la stat en fonction de la taille)
# nombre random > Variable Bit Rate

# table routage / node

# statistics permanente

def test():
    print(generate_packages())
    return 0

def init():
    # init les packages graphiques (matplotlib ?)
    pass

def start():
    # generations paquets
    # simulation
    plt.show()
    pass

def stop():
    # affiche le graph
    # affiche les stats
    pass

def main(argc, argv):
    init()
    start()
    stop()
    test()

if __name__ == '__main__':
    print("début de projet :)")
    sys.exit(main(len(sys.argv), sys.argv))
    