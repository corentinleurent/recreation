import tkinter as tk
import othello as oth

# un petit dictionnaire de couleurs (c'était pas joli noir et blanc)


class Couleurs(dict):   # pour définir une valeur par défaut
    def __missing__(self, key):
        return 'yellow'


couleurs = Couleurs()
couleurs[oth.NOIR] = 'Red'
couleurs[oth.BLANC] = 'Green'
couleurs[oth.VIDE] = 'White'

# quelques valeurs utiles
sizeV = oth.SIZE
sizeH = len(oth.COLONNES)
zoom = 20


class Game(tk.Frame):
    def __init__(self, master=None, table=None, couleur=oth.NOIR):
        tk.Frame.__init__(self, master)
        self.master = master
        self.couleur = couleur
        self.jeu = oth.Othello(table, self.couleur)
        self.create_widgets()

    def jouer(self, event):  # activé par un clic sur la surface de jeu
        if oth.JOUEURS[self.jeu.joueur] == 'Player':
            ligne = int((event.x - zoom)/zoom)
            colonne = int((event.y - zoom)/zoom)
            case = self.jeu.playJoueur((ligne, colonne))
            if case == 'EOG':
                self.end_of_game()
            elif case:
                self.drawtable(self.jeu.jeu)
                self.set_label_case(case)
            else:
                self.set_label_case(
                    f"La case {self.jeu.toString((ligne, colonne))} \nn'est pas jouable...")
        else:
            self.message_box(
                "Ce n'est pas votre tour\n(veuillez cliquer sur le bouton AI)")

    def next(self):  # activé par le bouton 'AI'
        if oth.JOUEURS[self.jeu.joueur] == 'AI':
            case = self.jeu.playAI()
            if case == 'EOG':
                self.end_of_game()
            else:
                self.drawtable(self.jeu.jeu)
                self.set_label_case(case)
        else:
            self.message_box("C'est à vous de jouer...")
            
    def end_of_game(self):
        self.drawtable(self.jeu.jeu)
        if self.gagnant() == self.couleur:
            self.message_box(f"Bravo!!!\nVous avez gagné!\n\
                    \nVotre score: {self.score(self.couleur)}\
                    \n(le score de votre adversaire: {self.score(-self.couleur)})")
        else:
            self.message_box(f"Vous avez perdu\n\
                    \nVotre score: {self.score(self.couleur)}\
                    \n(le score de votre adversaire: {self.score(-self.couleur)})")

    def message_box(self, message):
        """
            pop une fenêtre avec le message à faire passere
            et un bouton ok qui détruit la fenêtre
        """
        m_box_root = tk.Tk()
        m_box = tk.Frame(master=m_box_root)
        m_box.master.title('Message')
        m_box.grid(ipadx=10, ipady=10)
        label_text = tk.Label(m_box, text=message)
        label_text.grid(row=1, column=1)
        bouton_ok = tk.Button(m_box, text='Ok', command=m_box_root.destroy)
        bouton_ok.grid(row=2, column=1)
        m_box.mainloop()

    def nouveau_jeu(self):  # activé par le bouton Nouvelle partie
        """ Commence une nouvelle partie avec l'autre couleur """
        self.label_couleur_couleur.destroy()
        self.label_score_score.destroy()
        self.label_case_case.destroy()
        self.__init__(master=self.master, table=None, couleur=-self.couleur)

    def help(self):
        """ Fait apparaître les cases jouables """
        hilfe = self.jeu.casesJouables(self.jeu.get_couleur(self.jeu.joueur))
        for (l,k) in hilfe:
            cir = self.C.create_oval(
                    (l+1)*zoom, (k+1)*zoom, (l+2)*zoom, (k+2)*zoom, fill=couleurs['help'])

    def set_label_case(self, text):
        self.label_case_case.destroy()
        self.label_case_case = tk.Label(self.master, text=text)
        self.label_case_case.grid(row=6, column=1, rowspan=3, columnspan=2)

    def scoreN(self):
        return self.jeu.score()[0]

    def scoreB(self):
        return self.jeu.score()[1]
    
    def score(self, couleur):
        return self.scoreN() if couleur == oth.NOIR else self.scoreB()

    def gagnant(self):
        return oth.NOIR if self.scoreN() > self.scoreB() else oth.VIDE if self.scoreN() == self.scoreB() else oth.BLANC

    def set_label_score(self):
        self.label_score_score.destroy()
        self.create_label_score()

    def create_label_score(self):
        self.label_score_score = tk.Label(self.master,
                                          text=f'{couleurs[oth.NOIR]}={self.scoreN()}|{couleurs[oth.BLANC]}={self.scoreB()}',
                                          fg=couleurs[self.gagnant()],
                                          bg='White')
        self.label_score_score.grid(row=4, column=1, columnspan=2)

    def drawtable(self, table):
        """
            Dessine la table de jeu dans le canvas,
            et met à jour le score
        """
        for l in range(oth.SIZE):
            for k in range(len(oth.COLONNES)):
                rec = self.C.create_rectangle(
                    (l+1)*zoom, (k+1)*zoom, (l+2)*zoom, (k+2)*zoom, tag='case')
                cir = self.C.create_oval(
                    (l+1)*zoom, (k+1)*zoom, (l+2)*zoom, (k+2)*zoom, fill=couleurs[table[l][k]])
        self.set_label_score()

    def draw_canvas(self, canvas):
        x, y = 3*zoom/2, zoom/2
        for a in oth.COLONNES:
            labelC = canvas.create_text(x, y, text=a)
            labelC2 = canvas.create_text(x, (sizeV+3/2)*zoom, text=a)
            x += zoom
        x, y = zoom/2, 3*zoom/2
        for i in oth.LIGNES:
            labelL = canvas.create_text(x, y, text=i)
            labelL2 = canvas.create_text((sizeH+3/2)*zoom, y, text=i)
            y += zoom
        self.drawtable(self.jeu.jeu)
    
    def create_boutons(self):
        self.bouton_quit = tk.Button(self.master, text='Quitter', fg='red',
            command=self.master.destroy)
        self.bouton_nouveau = tk.Button(
            self.master, text='Nouvelle partie', command=self.nouveau_jeu)
        self.bouton_help = tk.Button(
            self.master, text='Help', command=self.help)
        self.bouton_AI = tk.Button(
            self.master, text='AI', fg=couleurs[-self.couleur], command=self.next)
            
    def create_labels(self):
        self.label_couleur_info = tk.Label(self.master, text='Votre couleur: ')
        self.label_couleur_couleur = tk.Label(self.master,
                                              text=couleurs[self.couleur],
                                              bg=couleurs[self.couleur])
        self.label_score = tk.Label(self.master, text='SCORE: ')
        self.create_label_score()
        self.label_case = tk.Label(self.master, text='Dernière case jouée: ')
        self.label_case_case = tk.Label(self.master)
        
    def griding(self):
        self.C.grid(row=1, column=3, rowspan=sizeV+2,
                    columnspan=sizeH+2, padx=5, pady=5)
        self.bouton_AI.grid(row=sizeV+3, column=3, sticky=tk.W)
        self.label_couleur_info.grid(
                    row=1, column=1, columnspan=2, sticky=tk.W)
        self.label_couleur_couleur.grid(row=2, column=1, columnspan=2)
        self.label_score.grid(row=3, column=1, columnspan=2, sticky=tk.W)
        self.bouton_nouveau.grid(row=sizeV+3, column=sizeH+3, sticky=tk.E)
        self.bouton_help.grid(row=sizeV+4, column=3, sticky=tk.W)
        self.bouton_quit.grid(row=sizeV+4, column=sizeH+3, sticky=tk.E)
        self.label_case.grid(row=5, column=1, columnspan=2, sticky=tk.W)
        self.rowconfigure(sizeV+4, pad=2)
        self.columnconfigure(sizeH+3, pad=2)
    
    def create_widgets(self):
        # Définition des widgets
        self.C = tk.Canvas(self.master, width=(len(oth.COLONNES)+2)*zoom,
                           height=(oth.SIZE+2)*zoom, bg='white')
        self.create_boutons()
        self.create_labels()
        self.draw_canvas(self.C)  # Attention! draw_canvas ne peut apparaître qu'après avec créé les labels

        # Placement des widgets
        self.griding()

        # Events
        self.C.bind('<Button-1>', self.jouer)


# Une classe inutile pour le moment -- en attente de maîtriser les virtual event
class Nouveau_Jeu(tk.Frame):
    def __init__(self, master=None, couleur=oth.NOIR):
        tk.Frame.__init__(self, master)
        self.master = master
        self.grid(ipadx=5, ipady=2)
        self.couleur = couleur
        self.create_widgets()

    def annul(self):
        self.master.destroy()

    def valid(self):  # ICI!!
        self.master.destroy()

    def to_noir(self):
        self.couleur = oth.NOIR

    def to_blanc(self):
        self.couleur = oth.BLANC

    def create_widgets(self):
        # Widgets
        self.label = tk.Label(
            self.master, text=f'Choisissez votre couleur:\n({couleurs[oth.NOIR]} commence)')
        coul = tk.IntVar()
        coul.set(self.couleur)
        self.choix_noir = tk.Radiobutton(self.master, text=couleurs[oth.NOIR],
                                         variable=coul, value=oth.NOIR, fg=couleurs[oth.NOIR],
                                         command=self.to_noir)
        self.choix_blanc = tk.Radiobutton(self.master, text=couleurs[oth.BLANC],
                                          variable=coul, value=oth.BLANC, fg=couleurs[oth.BLANC],
                                          command=self.to_blanc)
        self.annul = tk.Button(self.master, text='Annuler', command=self.annul)
        self.valider = tk.Button(
            self.master, text='Valider', command=self.valid)

        # Grid
        self.label.grid(row=1, column=1, columnspan=2)
        self.choix_noir.grid(row=2, column=1, sticky=tk.W)
        self.choix_blanc.grid(row=3, column=1, sticky=tk.W)
        self.annul.grid(row=4, column=2, padx=2, pady=5)
        self.valider.grid(row=4, column=3, padx=5, pady=5)


##
##root = tk.Tk()
##jeu = Game(master=root)
# jeu.master.title('Othello')
# jeu.mainloop()
