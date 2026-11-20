from automate import EPSILON


def afficher_table(automate):
    """Affiche la table de transitions d'un automate déterministe."""
    print("État initial :", automate.initial)
    print("États finaux :", automate.finals)
    print()

    # Ligne d'en-tête : une colonne par symbole de l'alphabet.
    ligne = "       "
    for symbole in automate.alphabet:
        ligne = ligne + symbole.ljust(5)
    print(ligne.rstrip())

    # Une ligne par état.
    for etat in range(automate.nombre_etats):
        if etat == automate.initial:
            marque_initial = "->"
        else:
            marque_initial = "  "
        if etat in automate.finals:
            marque_final = "*"
        else:
            marque_final = " "
        ligne = marque_initial + marque_final + str(etat).ljust(4)
        for symbole in automate.alphabet:
            arrivees = automate.destinations(etat, symbole)
            if len(arrivees) == 0:
                case = "-"
            else:
                case = str(arrivees[0])
            ligne = ligne + case.ljust(5)
        print(ligne.rstrip())


def afficher_correspondance(ensembles):
    """Affiche l'ensemble d'états de Thompson représenté par chaque état de l'AFD."""
    print("Correspondance avec l'automate de Thompson :")
    for numero in range(len(ensembles)):
        print("  état", numero, "=", ensembles[numero])


def texte_dot(automate):
    """Renvoie le texte DOT (Graphviz) qui décrit l'automate."""
    texte = "digraph automate {\n"
    texte = texte + "    rankdir=LR;\n"
    texte = texte + "    node [shape=circle];\n"
    texte = texte + "    entree [shape=point];\n"
    for etat in automate.finals:
        texte = texte + f"    q{etat} [shape=doublecircle];\n"
    texte = texte + f"    entree -> q{automate.initial};\n"
    for cle in automate.transitions:
        origine, symbole = cle
        if symbole == EPSILON:
            symbole = "ε"
        for arrivee in automate.transitions[cle]:
            texte = texte + f'    q{origine} -> q{arrivee} [label="{symbole}"];\n'
    texte = texte + "}\n"
    return texte


def ecrire_dot(automate, nom_fichier):
    """Écrit le texte DOT de l'automate dans un fichier."""
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        fichier.write(texte_dot(automate))