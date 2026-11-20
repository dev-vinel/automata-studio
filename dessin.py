
"""Génération graphique des automates avec Graphviz."""

from graphviz import Digraph
from automate import EPSILON


def dessiner(automate, chemin, avec_epsilon=False):
    """Génère une image PNG de l'automate et renvoie son chemin."""

    graphe = Digraph(format="png")
    graphe.attr(rankdir="LR")
    graphe.attr("node", shape="circle")

    # État de départ
    graphe.node("depart", shape="none", label="")
    graphe.edge("depart", str(automate.initial))

    # États
    for etat in range(automate.nombre_etats):
        forme = (
            "doublecircle"
            if etat in automate.finals
            else "circle"
        )
        graphe.node(str(etat), shape=forme, label=f"q{etat}")

    # Transitions
    symboles = list(automate.alphabet)

    if avec_epsilon:
        symboles.append(EPSILON)

    transitions = {}

    for etat in range(automate.nombre_etats):
        for symbole in symboles:
            destinations = automate.destinations(etat, symbole)

            for destination in destinations:
                cle = (etat, destination)
                transitions.setdefault(cle, []).append(
                    "ε" if symbole == EPSILON else symbole
                )

    for (depart, arrivee), labels in transitions.items():
        graphe.edge(
            str(depart),
            str(arrivee),
            label=", ".join(labels)
        )

    return graphe.render(chemin, cleanup=True)
