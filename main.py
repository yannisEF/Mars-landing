import random
from tkinter import Tk, Canvas, BOTH

from classe_game import Game
from classe_population import Population
from classe_terrain import Terrains
from tk_classes import Toile


fenetre = Tk()


largeur = 800
hauteur = 600
dim_ecran = (largeur, hauteur)

terrain_largeur = 7000
terrain_hauteur = 3000
dim_terrain = (terrain_largeur, terrain_hauteur)

proba_commande = (0.05, 0.2)
proba_mutation = (0.05, 0.02)
proba = (proba_commande, proba_mutation)

choix_terrain = 0

nb_individus = 100
fuel = 500
score_attendu = 100
#None si on attend la solution
generation_convergence = None
param_sim = (nb_individus, fuel, score_attendu, generation_convergence)

dessin_nombre_trajectoires = nb_individus

toile = Toile(fenetre, dim_ecran, dessin_nombre_trajectoires, choix_terrain, dim_terrain, proba, param_sim)

fenetre.mainloop()


