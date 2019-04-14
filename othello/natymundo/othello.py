# Othello

import numpy as np


VIDE = 0
NOIR = 1
BLANC = -1
SIZE = 8
COLONNES = 'ABCDEFGH'
LIGNES = [str(i+1) for i in range(SIZE)]
DIRECTIONS = {(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)}


class Othello:
    """
        Le jeu du même nom
    """

    def __init__(self, jeu=None):
        self.log = 'LOG: \n'
        if jeu:
            self.jeu = jeu
        else:
            self.jeu = np.zeros((SIZE, len(COLONNES)), dtype=np.int8)
            self.jeu[3][4], self.jeu[4][3] = NOIR, NOIR
            self.jeu[3][3], self.jeu[4][4] = BLANC, BLANC
        self.joueur = NOIR
        self.brouillon = None
        self.update()  # une copie du jeu sur laquelle on écrit plein d'infos utiles

    def __str__(self):
        return '\n'.join(';'.join(str(i) for i in ligne) for ligne in self.jeu)

    def write(self, file):
        with open(file, 'w', encoding='utf8') as f:
            f.write(str(self))
        
    def read(self, file):
        array = []
        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                for i in line.split(';'):
                    array.append(int(i))
        jeu = np.array((array), dtype=np.int8)
        return jeu.reshape((SIZE, len(COLONNES)))

    def next(self):
        self.joueur = -self.joueur

    def adversaire(self, couleur):
        return -couleur
                  
    def update(self):
        if not self.brouillon:
            self.brouillon = []
            for l in range(SIZE):
                self.brouillon.append([])
                for c in range(len(COLONNES)):
                    self.brouillon[l].append(self.jeu[l][c])
        for l in range(SIZE):
            for c in range(len(COLONNES)):
                pos = self.isJouable(l, c, self.joueur)
                if pos:
                    self.brouillon[l][c] = pos
    
   
    def casesAdjacentes(self, ligne, colonne, couleur):
        """ renvoie les couleurs des cases adjacentes """
        couleurs = []
        for (a, b) in DIRECTIONS:
            if a == b or a == -b:
                pass
            else:
                if 0 <= ligne+a < SIZE and 0 <= colonne+b < len(COLONNES):
                    couleurs.append(self.jeu[ligne+a][colonne+b])
        return couleurs

    def retournera(self, ligne, colonne, couleur):
        """ renvoie un tableau des jetons à retourner """
        t = []
        for (a, b) in DIRECTIONS:
            if a == b == 0:
                pass
            else:
                A = a
                B = b
                tmp = []
                while 0 <= ligne+A < SIZE and 0 <= colonne+B < SIZE:
                    if self.jeu[ligne+A][colonne+B] == VIDE:
                        A = SIZE
                        B = SIZE
                        pass
                    elif self.jeu[ligne+A][colonne+B] == couleur:
                        if (A, B) in DIRECTIONS:  # 1er passage
                            A = SIZE
                            B = SIZE
                            pass
                        else:
                            for (l, c) in tmp:
                                t.append((l, c))
                            break
                    else:
                        tmp.append((ligne+A, colonne+B))
                        A += a
                        B += b
        return t

    def isJouable(self, ligne, colonne, couleur):
        """
            renvoie un tableau des cases qui seront retournées ou VIDE si le tableau est vide
        """
        pos = VIDE
        if self.jeu[ligne][colonne] not in (NOIR, BLANC):
            if self.adversaire(couleur) in self.casesAdjacentes(ligne, colonne, couleur):
                pos = self.retournera(ligne, colonne, couleur)
                if not pos:
                    pos = VIDE
        return pos

    def meilleurCoup(self, couleur):
        """ renvoie le couple (ligne, colonne) correspondant à la case qui retourne le plus de jetons """
        maxSize = 0
        for l in range(SIZE):
            for c in range(len(COLONNES)):
                if not isinstance(self.brouillon[l][c], (int, np.int8)):
                    if len(self.brouillon[l][c])>maxSize:
                        maxSize = len(self.brouillon[l][c])
                        meilleureCase = (l, c)
        return meilleureCase

    def score(self):
        """ renvoie le score (NOIR, BLANC) """
        totN = 0
        totB = 0
        for l in range(SIZE):
            for c in range(len(COLONNES)):
                if self.jeu[l][c] == NOIR:
                    totN += 1
                elif self.jeu[l][c] == BLANC:
                    totB += 1
        return (totN, totB)

    def jouer(self, ligne, colonne, casesARetourner):
        """
            ajoute le jeton de couleur sur la case,
            retourne les pions à retourner
            efface les autres cases jouables
        """
        self.jeu[ligne][colonne] = self.joueur
        for (l, c) in casesARetourner:
            self.jeu[l][c] = -self.jeu[l][c]
        self.next()
        self.update()

    def toString(self, case):
        c = COLONNES[case[0]]
        l = LIGNES[case[1]]
        return ''.join((c, l))

    def playAI(self):
        """ Détermine la case que jouera l'AI """
        case = self.meilleurCoup(self.joueur)
        self.jouer(case[0], case[1], self.brouillon[case[0]][case[1]])
        return self.toString(case)

    def playJoueur(self, ligne, colonne):
        """ Verifie la jouablilité de la case """
        if not isinstance(self.brouillon[ligne][colonne], (int, np.int8)):
            self.jouer(ligne, colonne, self.brouillon[ligne][colonne])
            return self.toString((ligne, colonne))
        else:
            return False
    
    
