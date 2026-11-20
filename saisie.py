SYMBOLES_RESERVES = ["*", "|", "(", ")", "@", "."]


def lire_alphabet(texte):
    """Transforme le texte tapé en liste de symboles, sans les espaces."""
    texte = texte.replace(" ", "")
    return list(texte)


def erreur_alphabet(alphabet):
    """Renvoie un message d'erreur, ou un texte vide si l'alphabet est valide."""
    if len(alphabet) == 0:
        return "L'alphabet est vide."
    for symbole in alphabet:
        if symbole in SYMBOLES_RESERVES:
            return "Le symbole " + symbole + " est réservé."
        if alphabet.count(symbole) > 1:
            return "Le symbole " + symbole + " est en double."
    return ""


def saisir_alphabet():
    """Demande l'alphabet jusqu'à ce qu'il soit valide, puis le renvoie."""
    while True:
        texte = input("Alphabet (ex. ab ou a b) : ")
        alphabet = lire_alphabet(texte)
        erreur = erreur_alphabet(alphabet)
        if erreur == "":
            return alphabet
        print("Erreur :", erreur)


def saisir_expression():
    """Demande l'expression régulière et enlève les espaces."""
    texte = input("Expression régulière : ")
    return texte.replace(" ", "")