"""Tests du moteur de l'interface (aucun code graphique)."""

from moteur import (
    construire,
    preparer_mot,
    table_en_texte,
    table_transitions,
)


def test_construire_valide():
    construction, erreur = construire("ab", "(a|b)*abb")
    assert erreur == ""
    assert construction.postfixe == "ab|*a.b.b."


def test_construire_alphabet_en_double():
    construction, erreur = construire("a a", "a")
    assert construction is None
    assert "double" in erreur


def test_construire_parenthese_manquante():
    construction, erreur = construire("ab", "(a|b")
    assert construction is None
    assert "parenthèse" in erreur


def test_epsilon_accepte_comme_arobase():
    construction, erreur = construire("a", "aε")
    assert erreur == ""
    assert construction.expression == "a@"


def test_afd_de_aa():
    construction, _ = construire("a", "aa")
    assert construction.afd.nombre_etats == 3
    assert construction.afd.finals == [2]


def test_table_de_aa():
    construction, _ = construire("a", "aa")
    colonnes, lignes = table_transitions(construction.afd)
    assert colonnes == ["a"]
    assert len(lignes) == 3
    assert lignes[0]["initial"] is True
    assert lignes[0]["cases"] == ["q1"]
    assert lignes[2]["final"] is True
    assert lignes[2]["cases"] == ["-"]


def test_table_afn_contient_colonne_epsilon():
    construction, _ = construire("a", "a*")
    colonnes, _ = table_transitions(construction.afn, avec_epsilon=True)
    assert colonnes == ["a", "ε"]
    assert "ε" in table_en_texte(construction.afn, avec_epsilon=True)


def test_mot_vide():
    assert preparer_mot("", ["a"]) == ("", "")
    assert preparer_mot("ε", ["a"]) == ("", "")


def test_mot_hors_alphabet():
    mot, erreur = preparer_mot("ab", ["a"])
    assert mot == "ab"
    assert "position 2" in erreur