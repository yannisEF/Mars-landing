from tkinter import Canvas, BOTH

from classe_terrain import Terrains
from classe_population import Population

class Toile(Canvas):
    couleur_fond = 'black'
    couleur_claire, couleur_foncee = 'white', 'darkblue'
    
    def __init__(self, fenetre, dim_ecran, dessin_nombre_trajectoires, choix_terrain, dim_terrain, proba, param_sim):
        self.fenetre = fenetre

        self.largeur, self.hauteur = dim_ecran
        self.dessin_nombre_trajectoires = dessin_nombre_trajectoires
        self.terrain_largeur, self.terrain_hauteur = dim_terrain

        self.proba_commande, self.proba_mutation = proba

        self.nb_individus, self.fuel, self.score_attendu, self.generation_convergence = param_sim
        
        ratio_w = self.largeur/self.terrain_largeur
        ratio_h = self.hauteur/self.terrain_hauteur
        self.ratio = (ratio_w, ratio_h)

        Canvas.__init__(self, self.fenetre, width=self.largeur, height=self.hauteur, bg=Toile.couleur_fond)

        Terrain = Terrains(choix_terrain)
        Terrain.dessiner_terrain(self, self.terrain_hauteur, self.ratio)
        
        self.pack(fill=BOTH, expand=1)


        self.ARG_Game = [Terrain, self.terrain_largeur, self.terrain_hauteur, self.fuel, self.proba_commande]        
        self.Trajectoires = {}


        self._lancer_sim()
        self._dessiner_nouvelles_trajectoires()

    
    def _lancer_sim(self):
        self.Pop = Population(self.ARG_Game, self.nb_individus, self.proba_mutation)

        while self.solution_atteinte() is not True:
            self._deroulement_sim()
            self.maj_affichage()
            
    
    def _deroulement_sim(self):
        self.Pop.nouv_generation()
        self.Pop.muter()

    def solution_atteinte(self):
        for score in self.Pop.Scores:
            if score[1]  <= self.score_attendu:
                print('Solution', self.score_attendu,'atteinte en', self.Pop.generation,'générations, correspondant à :')
                print(score[0])
                return True

        try:
            if self.generation_convergence < self.Pop.generation:
                    print('Simulation de', self.generation_convergence,'générations sans atteindre le score souhaité, correspondant à :')
                    print(self.Pop.Scores[-1][0])
                    return True
        except TypeError: pass

        return False

    def _dessiner_trajectoire(self, individu, couleur):
        ratio_w, ratio_h = self.ratio

        Dessin_trajectoire = []
        for k in range(len(individu.Trajectoire)-1):
            x1, y1 = individu.Trajectoire[k]
            x2, y2 = individu.Trajectoire[k+1]

            y1 = self.terrain_hauteur - y1
            y2 = self.terrain_hauteur - y2

            Dessin_trajectoire.append(self.create_line(x1*ratio_w, y1*ratio_h, x2*ratio_w, y2*ratio_h, fill=couleur))
        self.Trajectoires[individu] = Dessin_trajectoire
    
    def _dessiner_nouvelles_trajectoires(self):
        for k in range(self.dessin_nombre_trajectoires, 0, -1):
            individu = self.Pop.Scores[-k][0]

            if k == 1:
                self._dessiner_trajectoire(individu, Toile.couleur_claire)
            else: self._dessiner_trajectoire(individu, Toile.couleur_foncee)
    
    def maj_affichage(self):
        for dessin_supprime in self.Trajectoires.values():
            for ligne_dessin in dessin_supprime:
                self.delete(ligne_dessin)
        
        self._dessiner_nouvelles_trajectoires()
        self.fenetre.update()
            



