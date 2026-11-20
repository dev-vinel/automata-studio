PRIORITE = {"|": 1, ".": 2}

def ajouter_concatenation(expression, alphabet):
    """Insère le symbole « . » partout où une concaténation est sous-entendue."""
    fin_operande = alphabet + ["@", ")", "*"]
    debut_operande = alphabet + ["@", "("]

    resultat = ""
    for i in range(len(expression)):
        courant = expression[i]
        resultat = resultat + courant
        if i + 1 < len(expression):
            suivant = expression[i + 1]
            if courant in fin_operande and suivant in debut_operande:
                resultat = resultat + "."
    return resultat

def vers_postfixe(expression_explicite):
    """Convertit une expression (avec « . » explicites) en forme postfixée."""
    sortie = ""
    pile = []
    for caractere in expression_explicite:
        if caractere == "(":
            pile.append(caractere)
        elif caractere == ")":
            while pile[-1] != "(":
                sortie = sortie + pile.pop()
            pile.pop()
        elif caractere == "|" or caractere == ".":
            while len(pile) > 0 and pile[-1] != "(" and PRIORITE[pile[-1]] >= PRIORITE[caractere]:
                sortie = sortie + pile.pop()
            pile.append(caractere)
        else:
            sortie = sortie + caractere
    while len(pile) > 0:
        sortie = sortie + pile.pop()
    return sortie