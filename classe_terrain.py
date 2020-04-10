from tkinter import Canvas


class Terrains:
    couleur = 'red'
    #Chaque carte comporte les coordonnées:
    #  des points de niveau, du point de départ et des indices des points délimitant les zones
    Cartes = [
        ([(0, 100), (1000, 500), (1500, 100), (3000, 100), (5000, 1500), (6999, 1000)], (5000, 2500), (2,3)),
        ([(0, 1000), (300, 1500), (350, 1400), (500, 2100), (1500, 2100), (2000, 200), (2500, 500), (2900, 300), (3000, 200), (3200, 1000), (3500, 500), (3800, 800), (4000, 200), (4200, 800), (4800, 600), (5000, 1200), (5500, 900), (6000, 500), (6500, 300), (6999, 500)], (6500, 2700), (3,4))
        ]

    def __init__(self, choix):
        carte = Terrains.Cartes[choix]

        self.Points = carte[0]
        self.Pos_depart = carte[1]
        self.Zones = carte[2]


    def dessiner_terrain(self, canvas, terrain_hauteur, ratio):
        ratio_w = ratio[0]
        ratio_h = ratio[1]

        for k in range(len(self.Points)-1):
            x1, y1 = self.Points[k]
            x2, y2 = self.Points[k+1]

            y1 = terrain_hauteur - y1
            y2 = terrain_hauteur - y2

            canvas.create_line(x1*ratio_w, y1*ratio_h, x2*ratio_w, y2*ratio_h, fill=Terrains.couleur)