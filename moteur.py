"""Moteur de l'interface : enchaîne les fonctions du projet sans print ni input.

Ce fichier ne contient aucun code graphique : il peut donc être testé avec pytest.
"""

from dataclasses import dataclass

from automate import EPSILON, construire_automate
from determinisation import determiniser
from postfixe import ajouter_concatenation, vers_postfixe
from reconnaissance import erreur_mot
from saisie import erreur_alphabet, lire_alphabet
from validation import erreur_expression


@dataclass
class Construction:
    """Tout ce que produit la chaîne « expression -> AFN -> AFD »."""

    alphabet: list
    expression: str
    explicite: str
    postfixe: str
    afn: object
    afd: object
    ensembles: list


def construire(texte_alphabet, texte_expression):
    """Construit les automates. Renvoie (construction, "") ou (None, message d'erreur)."""
    alphabet = lire_alphabet(texte_alphabet)
    erreur = erreur_alphabet(alphabet)
    if erreur != "":
        return None, "Alphabet : " + erreur

    expression = texte_expression.replace(" ", "")
    if "ε" not in alphabet:
        expression = expression.replace("ε", EPSILON)  # ε est accepté comme le @
    erreur = erreur_expression(expression, alphabet)
    if erreur != "":
        return None, "Expression : " + erreur

    explicite = ajouter_concatenation(expression, alphabet)
    postfixe = vers_postfixe(explicite)
    afn = construire_automate(postfixe, alphabet)
    afd, ensembles = determiniser(afn)
    return Construction(alphabet, expression, explicite, postfixe, afn, afd, ensembles), ""


def preparer_mot(texte, alphabet):
    """Nettoie le mot tapé. Renvoie (mot, message d'erreur ou texte vide)."""
    mot = texte.replace(" ", "")
    if mot in ("ε", EPSILON) and mot not in alphabet:
        mot = ""  # ε et @ désignent le mot vide
    return mot, erreur_mot(mot, alphabet)


def nom_etat(numero):
    """Nom d'un état : 0 devient q0."""
    return "q" + str(numero)


def table_transitions(automate, avec_epsilon=False):
    """Renvoie (colonnes, lignes) : une ligne par état, une case par symbole.

    Chaque ligne est un dictionnaire : etat, initial, final, cases.
    Une case contient les états d'arrivée (« q1, q2 ») ou « - » s'il n'y en a pas.
    """
    symboles = list(automate.alphabet)
    colonnes = list(symboles)
    if avec_epsilon:
        symboles.append(EPSILON)
        colonnes.append("ε")

    lignes = []
    for etat in range(automate.nombre_etats):
        cases = []
        for symbole in symboles:
            arrivees = automate.destinations(etat, symbole)
            if len(arrivees) == 0:
                cases.append("-")
            else:
                cases.append(", ".join(nom_etat(a) for a in arrivees))
        lignes.append({
            "etat": etat,
            "initial": etat == automate.initial,
            "final": etat in automate.finals,
            "cases": cases,
        })
    return colonnes, lignes


def table_en_texte(automate, avec_epsilon=False):
    """Met la table de transitions en texte aligné (police à chasse fixe)."""
    colonnes, lignes = table_transitions(automate, avec_epsilon)
    cases = [case for ligne in lignes for case in ligne["cases"]]
    largeur = max([len(c) for c in colonnes + cases] + [3]) + 2

    texte = (" " * 9 + "".join(c.ljust(largeur) for c in colonnes)).rstrip() + "\n"
    for ligne in lignes:
        marque = ("→" if ligne["initial"] else " ") + ("*" if ligne["final"] else " ")
        nom = nom_etat(ligne["etat"]).ljust(6)
        corps = "".join(c.ljust(largeur) for c in ligne["cases"]).rstrip()
        texte = texte + marque + " " + nom + corps + "\n"
    texte = texte + "\n→ état initial     * état final\n"
    return texte


def correspondance_en_texte(construction):
    """Dit quels états de Thompson regroupe chaque état de l'AFD."""
    texte = "Correspondance avec l'AFN-ε de Thompson :\n"
    for numero in range(len(construction.ensembles)):
        membres = ", ".join(nom_etat(e) for e in construction.ensembles[numero])
        texte = texte + "  " + nom_etat(numero) + " = {" + membres + "}\n"
    return texte


def resume_en_texte(construction):
    """Résumé des étapes de la construction."""
    afn = construction.afn
    afd = construction.afd
    finals_afn = ", ".join(nom_etat(f) for f in afn.finals)
    finals_afd = ", ".join(nom_etat(f) for f in afd.finals)
    lignes = [
        "Alphabet : " + ", ".join(construction.alphabet),
        "Expression : " + construction.expression,
        "Avec concaténation explicite : " + construction.explicite,
        "Forme postfixée : " + construction.postfixe,
        "",
        "AFN-ε (Thompson) : " + str(afn.nombre_etats) + " états, initial "
        + nom_etat(afn.initial) + ", final " + finals_afn,
        "AFD : " + str(afd.nombre_etats) + " états, initial "
        + nom_etat(afd.initial) + ", finaux " + finals_afd,
    ]
    return "\n".join(lignes) + "\n"