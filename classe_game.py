import random
import math


class Fusee:

    def __init__(self, position, fuel, Commandes={}):
        self.x, self.y = position
        self.vx, self.vy = 0, 0

        self.fuel = fuel

        self.angle = 0
        self.power = 0

        self.but = (self.angle, self.power)

        self.Commandes = Commandes
    
    def maj(self, compteur, but_power, but_angle, Memoriser_lancement=True):
        if Memoriser_lancement is True:
            if  (but_angle, but_power) != self.but:
                self.Commandes[compteur] = (but_angle, but_power)
            self.but = but_angle, but_power


        if self.fuel == 0:
            self.power = 0
        else:
            if self.power < but_power:
                self.power += 1
            elif self.power > but_power:
                self.power -= 1
            
            if self.angle < but_angle:
                self.angle += 15
                if self.angle > but_angle:  self.angle = but_angle
            elif self.angle > but_angle:
                self.angle -= 15
                if self.angle < but_angle:  self.angle = but_angle

            self.vx -= math.sin(self.angle) * self.power
            self.vy +=  math.cos(self.angle) * self.power


        self.vy += Game.pesanteur
        self.fuel -= self.power

            
class Game:
    next_id = 0
    Vitesse_max = (20, 40)
    pesanteur = -3.711

    def __init__(self, *args, **kwargs):
        if len(args) < 5:
            args = args[0]
        Terrain, terrain_largeur, terrain_hauteur, fuel, proba_commande = args

        self.Terrain = Terrain    
        self.terrain_largeur, self.terrain_hauteur = terrain_largeur, terrain_hauteur

        #self.Trajectoire sert pour l'affichage et l'évaluation seulement
        #  alors que self.fusee.Commandes sert pour les crossover et mutations
        self.Trajectoire = []
        
        self.proba_commande_angle, self.proba_commande_power = proba_commande

        self.fuel = fuel

        if len(kwargs) == 0:
            self.fusee = Fusee(self.Terrain.Pos_depart, self.fuel)
            self.vitesse_arrivee = self._jeu()
        else:
            self.fusee = Fusee(self.Terrain.Pos_depart, self.fuel, kwargs['Commandes'])
            self._init_rejouer()
 
        self.id = Game.next_id
        Game.next_id += 1
    
    def _init_rejouer(self):
        self.Trajectoire = []

        self.fusee.x, self.fusee.y = self.Terrain.Pos_depart
        self.fusee.vx, self.fusee.vy = 0, 0

        self.fusee.fuel = self.fuel

        self.fusee.angle = 0
        self.fusee.power = 0

        self.vitesse_arrivee = self.rejouer() 

    def __str__(self):
        return str(self.vitesse_arrivee) + str(self.Trajectoire)

    def _toucherSol(self):
        if self.fusee.x > self.terrain_largeur or self.fusee.x < 0:
            return False
        
        x = self.fusee.x
        y = self.fusee.y

        for k in range(len(self.Terrain.Points)-1):
            xA, yA = self.Terrain.Points[k]
            xB, yB = self.Terrain.Points[k+1]

            if xA < x and x < xB:
                if y <= (yB - yA) * (x - xA) / (xB-xA) + yA:
                    return True
            elif xA == xB:
                if y < yA or y < yB:
                    if (self.Trajectoire[-2][0] - xA) * (self.Trajectoire[-1][0] - xA) < 0:
                        return True
            
            if x == xA and y <= yA: return True
            if x == xB and y <= yB: return True
                    
        return False
    
    def _piloter(self, but):
        nouv_angle, nouv_power = but

        r_changement_angle = random.random()
        r_changement_power = random.random()
        if self.proba_commande_angle >= r_changement_angle:
            nouv_angle = random.randint(-90, 90)
        if self.proba_commande_power >= r_changement_power:
            nouv_power = random.randint(0, 4)
        
        return (nouv_angle, nouv_power)

    def _jeu(self):
        but_power = random.randint(0,4)
        but_angle = random.randint(-90,90)

        compteur = 0
        while self._toucherSol() is not True:
            self.fusee.y += self.fusee.vy
            self.fusee.x += self.fusee.vx

            but_angle, but_power = self._piloter((but_angle, but_power))
            self.fusee.maj(compteur, but_power, but_angle)            

            self.Trajectoire.append((self.fusee.x, self.fusee.y))
            compteur += 1
        return (self.fusee.vx, self.fusee.vy)

    def rejouer(self):
        but_power = self.fusee.power
        but_angle = self.fusee.angle

        compteur = 0
        while self._toucherSol() is not True:
            self.fusee.y += self.fusee.vy
            self.fusee.x += self.fusee.vx

            try:
                but_angle, but_power = self.fusee.Commandes[compteur]
            except KeyError: pass

            self.fusee.maj(compteur, but_power, but_angle, False)            

            self.Trajectoire.append((self.fusee.x, self.fusee.y))
            compteur += 1
        return (self.fusee.vx, self.fusee.vy)

    def evaluer(self):
        i1, i2 = self.Terrain.Zones

        x1, y1 = self.Terrain.Points[i1]
        x2 = self.Terrain.Points[i2][0]
        x_centre = int((x1 + x2)/2)

        dx = self.fusee.x - x_centre
        dy = self.fusee.y - y1
        distance_centre = math.sqrt(dx**2 + dy**2)

        vx, vy = self.vitesse_arrivee
        max_x, max_y = Game.Vitesse_max

        ratio_x, ratio_y = vx / max_x, vy / max_y
        ratio = (ratio_x + ratio_y) / 2

        #INTERMEDIAIRE PAS DE VITESSE
        return  distance_centre
 
    def mutation(self, proba_mutation):
        proba_mutation_angle, proba_mutation_power = proba_mutation

        une_mutation = False
        for k in self.fusee.Commandes.keys():
            r_muter_angle = random.random()
            r_muter_power = random.random()

            nouv_angle, nouv_power = self.fusee.Commandes[k]
            if proba_mutation_angle >= r_muter_angle:
                    nouv_angle = random.randint(-90, 90)
                    une_mutation = True
            if proba_mutation_power >= r_muter_power:
                    nouv_power = random.randint(0, 4)
                    une_mutation = True

            self.fusee.Commandes[k] = (nouv_angle, nouv_power)

        if une_mutation is True:
            self._init_rejouer()

        return une_mutation
