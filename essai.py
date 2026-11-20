from automate import construire_automate
from determinisation import determiniser
from reconnaissance import erreur_mot, reconnaitre, afficher_resultat

alphabet = ["a", "b"]

afd, ensembles = determiniser(construire_automate("ab|*a.b.b.", alphabet))
for mot in ["abb", "aabb", "ab", ""]:
    accepte, trace, raison = reconnaitre(afd, mot)
    afficher_resultat(mot, accepte, trace, raison)
    print()

afd2, ensembles2 = determiniser(construire_automate("a*", alphabet))
accepte, trace, raison = reconnaitre(afd2, "ab")
afficher_resultat("ab", accepte, trace, raison)
print()

print(erreur_mot("abc", alphabet))
print(erreur_mot("abab", alphabet) == "")