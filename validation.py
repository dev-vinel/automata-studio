CARACTERES_SPECIAUX = ["|", "*", "(", ")", "@"]


def erreur_caracteres(expression, alphabet):
    """Renvoie un message d'erreur si un caractère est inconnu, sinon un texte vide."""
    """  if len(expression) == 0:
        return "L'expression est vide."   """
    for i in range(len(expression)):
        caractere = expression[i]
        if caractere not in alphabet and caractere not in CARACTERES_SPECIAUX:
            return "Caractère inconnu « " + caractere + " » à la position " + str(i + 1) + "."
    return ""

def erreur_parentheses(expression):
    """Renvoie un message d'erreur si les parenthèses sont mal placées, sinon un texte vide."""
    niveau = 0
    for i in range(len(expression)):
        caractere = expression[i]
        if caractere == "(":
            niveau += 1
        elif caractere == ")":
            niveau -= 1
            if niveau < 0:
                return "Parenthèse fermante sans ouvrante à la position " + str(i + 1) + "."
    if niveau > 0:
        return "Il manque " + str(niveau) + " parenthèse(s) fermante(s)."
    return ""

def erreur_operateurs(expression, alphabet):
    """Renvoie un message d'erreur si un opérateur est mal placé, sinon un texte vide."""
    if len(expression) == 0:
        return "L'expression est vide."

    fin_operande = alphabet + ["@", ")", "*"]
    debut_operande = alphabet + ["@", "("]

    if expression[0] not in debut_operande:
        return "L'expression ne peut pas commencer par « " + expression[0] + " »."
    if expression[-1] not in fin_operande:
        return "L'expression ne peut pas se terminer par « " + expression[-1] + " »."

    for i in range(1, len(expression)):
        courant = expression[i]
        precedent = expression[i - 1]
        if courant in ["*", "|", ")"] and precedent not in fin_operande:
            return ("Le caractère « " + courant + " » est mal placé à la position "
                    + str(i + 1) + " (après « " + precedent + " »).")
    return ""

def erreur_expression(expression, alphabet):
    """Lance les trois contrôles dans l'ordre et renvoie la première erreur trouvée."""
    erreur = erreur_caracteres(expression, alphabet)
    if erreur != "":
        return erreur
    erreur = erreur_parentheses(expression)
    if erreur != "":
        return erreur
    return erreur_operateurs(expression, alphabet)