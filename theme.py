"""Thème de l'interface : palette « pétrole et laiton ».

Chaque couleur est un couple (thème clair, thème sombre), que CustomTkinter
choisit tout seul selon le mode d'affichage.
"""

import customtkinter as ctk

# Surfaces
FOND = ("#EDF3F4", "#0B2530")
PANNEAU = ("#FFFFFF", "#123646")
CHAMP = ("#E3EEF0", "#0E2C3A")
BORD = ("#C2D6DB", "#25596D")

# Texte
TEXTE = ("#12313D", "#E6F1F2")
TEXTE_DOUX = ("#4F6F7A", "#8FB3BD")

# Accent (bouton principal, interrupteur)
ACCENT = ("#0F6E8C", "#D9A441")
ACCENT_SURVOL = ("#0B5870", "#E8B95A")
TEXTE_SUR_ACCENT = ("#FFFFFF", "#0B2530")

# États
SUCCES = ("#1E8E5A", "#5FD3B0")
ERREUR = ("#C23B3B", "#FF7A70")

# Onglets (texte blanc sur tous les fonds)
TEXTE_ONGLET = "#FFFFFF"
ONGLET_BARRE = ("#DCE8EB", "#0B2530")
ONGLET_ACTIF = ("#0F6E8C", "#1B8AA6")
ONGLET_ACTIF_SURVOL = ("#0B5870", "#2399B6")
ONGLET_INACTIF = ("#557A86", "#2B5567")
ONGLET_INACTIF_SURVOL = ("#466975", "#35677D")


def police(taille, graisse="normal"):
    """Police de l'interface (à appeler une fois la fenêtre créée)."""
    return ctk.CTkFont(family="Segoe UI", size=taille, weight=graisse)


def police_code(taille=15):
    """Police à chasse fixe pour les tables et les traces."""
    return ctk.CTkFont(family="Consolas", size=taille)