def erreur_mot(mot, alphabet):
    """Renvoie un message d'erreur si le mot contient une lettre hors alphabet, sinon un texte vide."""
    for i in range(len(mot)):
        if mot[i] not in alphabet:
            return "La lettre « " + mot[i] + " » (position " + str(i + 1) + ") n'est pas dans l'alphabet."
    return ""


def saisir_mot(alphabet):
    """Demande un mot jusqu'à ce qu'il soit valide. Une saisie vide est le mot vide."""
    while True:
        texte = input("Mot à tester (Entrée seule = mot vide) : ")
        mot = texte.replace(" ", "")
        erreur = erreur_mot(mot, alphabet)
        if erreur == "":
            return mot
        print("Erreur :", erreur)


def reconnaitre(automate, mot):
    """Lit le mot dans l'automate déterministe. Renvoie (accepte, trace, raison)."""
    etat = automate.initial
    trace = [(etat, mot)]
    for i in range(len(mot)):
        lettre = mot[i]
        arrivees = automate.destinations(etat, lettre)
        if len(arrivees) == 0:
            raison = "Aucune transition depuis q" + str(etat) + " avec la lettre « " + lettre + " »."
            return False, trace, raison
        etat = arrivees[0]
        trace.append((etat, mot[i + 1:]))
    if etat in automate.finals:
        return True, trace, ""
    raison = "Le mot est entièrement lu, mais q" + str(etat) + " n'est pas un état final."
    return False, trace, raison


def texte_configuration(configuration):
    """Met une configuration (état, reste du mot) en forme : (q1, bb)."""
    etat, reste = configuration
    if reste == "":
        reste = "ε"
    return "(q" + str(etat) + ", " + reste + ")"


def afficher_resultat(mot, accepte, trace, raison):
    """Affiche le calcul (suite de configurations) puis la conclusion."""
    if mot == "":
        print("Mot : ε (mot vide)")
    else:
        print("Mot :", mot)

    ligne = texte_configuration(trace[0])
    for i in range(1, len(trace)):
        ligne = ligne + " ⊢ " + texte_configuration(trace[i])
    print("Calcul :", ligne)

    if accepte:
        dernier_etat = trace[-1][0]
        print("Résultat : le mot est RECONNU, car q" + str(dernier_etat) + " est un état final.")
    else:
        print("Résultat : le mot est REJETÉ.")
        print("Raison :", raison)