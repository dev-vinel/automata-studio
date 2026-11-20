EPSILON = "@"


class Automate:
    """Un automate fini : états numérotés, transitions, état initial, états finaux."""

    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.nombre_etats = 0
        self.initial = None
        self.finals = []
        self.transitions = {}

    def ajouter_etat(self):
        """Crée un nouvel état et renvoie son numéro."""
        numero = self.nombre_etats
        self.nombre_etats = self.nombre_etats + 1
        return numero

    def ajouter_transition(self, depart, symbole, arrivee):
        """Enregistre la transition depart --symbole--> arrivee."""
        cle = (depart, symbole)
        if cle not in self.transitions:
            self.transitions[cle] = []
        self.transitions[cle].append(arrivee)

    def destinations(self, etat, symbole):
        """Renvoie la liste des états atteignables depuis etat avec symbole."""
        cle = (etat, symbole)
        if cle in self.transitions:
            return self.transitions[cle]
        return []


def morceau_symbole(automate, symbole):
    """Crée le morceau « debut --symbole--> fin » et renvoie (debut, fin)."""
    debut = automate.ajouter_etat()
    fin = automate.ajouter_etat()
    automate.ajouter_transition(debut, symbole, fin)
    return debut, fin


def morceau_vide(automate):
    """Crée le morceau du mot vide « debut --ε--> fin » et renvoie (debut, fin)."""
    return morceau_symbole(automate, EPSILON)


def morceau_union(automate, morceau1, morceau2):
    """Relie deux morceaux par une union (|) et renvoie le nouveau morceau (debut, fin)."""
    debut1, fin1 = morceau1
    debut2, fin2 = morceau2
    debut = automate.ajouter_etat()
    fin = automate.ajouter_etat()
    automate.ajouter_transition(debut, EPSILON, debut1)
    automate.ajouter_transition(debut, EPSILON, debut2)
    automate.ajouter_transition(fin1, EPSILON, fin)
    automate.ajouter_transition(fin2, EPSILON, fin)
    return debut, fin


def morceau_concatenation(automate, morceau1, morceau2):
    """Relie la fin du morceau 1 au début du morceau 2 et renvoie (debut1, fin2)."""
    debut1, fin1 = morceau1
    debut2, fin2 = morceau2
    automate.ajouter_transition(fin1, EPSILON, debut2)
    return debut1, fin2


def morceau_etoile(automate, morceau):
    """Applique l'étoile de Kleene (*) à un morceau et renvoie le nouveau morceau (debut, fin)."""
    debut1, fin1 = morceau
    debut = automate.ajouter_etat()
    fin = automate.ajouter_etat()
    automate.ajouter_transition(debut, EPSILON, debut1)  # entrer dans le morceau
    automate.ajouter_transition(fin1, EPSILON, fin)      # sortir du morceau
    automate.ajouter_transition(fin1, EPSILON, debut1)   # boucler : recommencer le morceau
    automate.ajouter_transition(debut, EPSILON, fin)     # contourner : zéro répétition
    return debut, fin


def construire_automate(postfixe, alphabet):
    """Construit l'automate (méthode de Thompson) à partir de la forme postfixée."""
    automate = Automate(alphabet)
    pile = []
    for caractere in postfixe:
        if caractere == "*":
            morceau = pile.pop()
            pile.append(morceau_etoile(automate, morceau))
        elif caractere == "." or caractere == "|":
            morceau2 = pile.pop()  # le premier dépilé est le second opérande
            morceau1 = pile.pop()
            if caractere == ".":
                pile.append(morceau_concatenation(automate, morceau1, morceau2))
            else:
                pile.append(morceau_union(automate, morceau1, morceau2))
        elif caractere == EPSILON:
            pile.append(morceau_vide(automate))
        else:
            pile.append(morceau_symbole(automate, caractere))
    debut, fin = pile.pop()
    automate.initial = debut
    automate.finals = [fin]
    return automate