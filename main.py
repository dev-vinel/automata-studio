from saisie import saisir_alphabet, saisir_expression
from validation import erreur_expression
from postfixe import ajouter_concatenation, vers_postfixe
from automate import construire_automate
from determinisation import determiniser
from affichage import afficher_table, afficher_correspondance, ecrire_dot
from reconnaissance import saisir_mot, reconnaitre, afficher_resultat

alphabet = saisir_alphabet()

while True:
    expression = saisir_expression()
    erreur = erreur_expression(expression, alphabet)
    if erreur == "":
        break
    print("Erreur :", erreur)
    print("Essaie une autre expression.")

print("L'expression est bien écrite :", expression)

explicite = ajouter_concatenation(expression, alphabet)
print("Avec concaténation explicite :", explicite)

postfixe = vers_postfixe(explicite)
print("Forme postfixée :", postfixe)

automate = construire_automate(postfixe, alphabet)
print("Automate de Thompson :", automate.nombre_etats, "états")

afd, ensembles = determiniser(automate)
print()
print("Automate déterministe :")
afficher_table(afd)
afficher_correspondance(ensembles)

ecrire_dot(afd, "automate.dot")
print()
print("Fichier automate.dot créé dans le dossier du projet.")

print()
print("=== Test de mots ===")
while True:
    mot = saisir_mot(alphabet)
    accepte, trace, raison = reconnaitre(afd, mot)
    afficher_resultat(mot, accepte, trace, raison)
    print()
    reponse = input("Tester un autre mot ? (o/n) : ")
    if reponse != "o":
        break