import random

from classe_game import Game

class Population:

    def __init__(self, ARG_Game, nb_individu, proba_mutation):
        self.ARG_Game = ARG_Game

        self.Indivs = [Game(*self.ARG_Game) for k in range(nb_individu)]
        self.Scores = [[indiv, indiv.evaluer()] for indiv in self.Indivs]

        self.proba_mutation = proba_mutation
        self.generation = 0

        self.Scores = self._ordonner()

    def _ordonner(self):
        return sorted(self.Scores, key=lambda x:x[1], reverse=True)

    def _selection(self):
        couple1 = (self.Scores[-1][0], self.Scores[-3][0])
        couple2 = (self.Scores[-2][0], self.Scores[-4][0])
        
        
        Couple = (couple1, couple2)

        return Couple
    
    def _crossover(self, couple):
        Commandes1 = couple[0].fusee.Commandes
        Commandes2 = couple[1].fusee.Commandes

        #On prend la plus petite des plus grandes clées puis inversement.
        Commandes_moins_instructions = min(Commandes1, Commandes2, key=lambda x:max(x.keys()))
        Commandes_plus_instructions = max(Commandes1, Commandes2, key=lambda x:max(x.keys()))

        nouv_Commandes = {}        

        Clees_commandes_moins = list(Commandes_moins_instructions)
        point_coupe = random.choice(Clees_commandes_moins)
        for k, v in Commandes_moins_instructions.items():
            if k <= point_coupe:
                nouv_Commandes[k] = v
            else: break
        for k, v in Commandes_plus_instructions.items():
            if k > point_coupe:
                nouv_Commandes[k] = v
        
        return Game(self.ARG_Game, Commandes=nouv_Commandes)

    def nouv_generation(self):
        self.generation += 1

        for couple in self._selection():
            enfant = self._crossover(couple)
            
            self.Indivs.append(enfant)
            self.Scores.append([enfant, enfant.evaluer()])
        
        Indivs_supprime = self.Scores[:2]
        self.Scores = self.Scores[2:]
        
        self.Scores = self._ordonner()

        for supprime in Indivs_supprime:
            self.Indivs.remove(supprime[0])
    
    def muter(self):
        Liste_indivs = [k[0] for k in self.Scores]

        for indiv in self.Indivs:
            if indiv.mutation(self.proba_mutation) is True:
                self.Scores[Liste_indivs.index(indiv)][1] = indiv.evaluer()
        
        self.Scores = self._ordonner()

        





        


