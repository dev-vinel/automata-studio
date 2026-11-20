from automate import Automate, EPSILON


def fermeture_epsilon(automate, etats):
    """Renvoie la liste triée des états atteignables depuis etats avec des transitions ε seulement."""
    resultat = list(etats)
    a_traiter = list(etats)
    while len(a_traiter) > 0:
        etat = a_traiter.pop()
        for suivant in automate.destinations(etat, EPSILON):
            if suivant not in resultat:
                resultat.append(suivant)
                a_traiter.append(suivant)
    resultat.sort()
    return resultat


def deplacement(automate, etats, symbole):
    """Renvoie la liste triée des états atteignables depuis etats en lisant symbole."""
    resultat = []
    for etat in etats:
        for suivant in automate.destinations(etat, symbole):
            if suivant not in resultat:
                resultat.append(suivant)
    resultat.sort()
    return resultat


def determiniser(automate):
    """Construit l'automate déterministe équivalent. Renvoie (afd, ensembles)."""
    afd = Automate(automate.alphabet)

    # L'état 0 du nouvel automate correspond à l'ensemble de départ.
    ensembles = [fermeture_epsilon(automate, [automate.initial])]
    afd.ajouter_etat()
    afd.initial = 0

    # On traite les ensembles un par un, dans l'ordre où on les découvre.
    i = 0
    while i < len(ensembles):
        ensemble = ensembles[i]
        for symbole in automate.alphabet:
            suivant = fermeture_epsilon(automate, deplacement(automate, ensemble, symbole))
            if len(suivant) > 0:
                if suivant not in ensembles:
                    ensembles.append(suivant)
                    afd.ajouter_etat()
                afd.ajouter_transition(i, symbole, ensembles.index(suivant))
        i = i + 1

    # Un état est final s'il contient un état final de l'ancien automate.
    for numero in range(len(ensembles)):
        for final in automate.finals:
            if final in ensembles[numero] and numero not in afd.finals:
                afd.finals.append(numero)

    return afd, ensembles