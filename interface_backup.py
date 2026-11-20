
"""Interface graphique du reconnaisseur de langage régulier."""

import customtkinter as ctk
import moteur
import theme
import dessin
from PIL import Image


EXEMPLES = [
    ("ab", "(a|b)*abb"),
    ("ab", "a*b"),
    ("ab", "(ab)*"),
    ("ab", "a|b*"),
]

MESSAGE_ACCUEIL = (
    "Tape un alphabet et une expression, puis clique sur Construire.\n"
    "(ou appuie sur Ctrl+Entrée).\n"
)


class Application(ctk.CTk):
    """Fenêtre principale."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()

        self.title("Reconnaisseur de langage régulier")
        self.geometry("1200x760")
        self.minsize(1100, 700)
        self.configure(fg_color=theme.FOND)

        self.construction = None
        self.images = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._creer_entete()
        self._creer_panneau_saisie()
        self._creer_resultats()

        self.bind("<Control-Return>", lambda _e: self.construire())
        self.champ_alphabet.focus()

    def _creer_entete(self):
        entete = ctk.CTkFrame(
            self, fg_color=theme.PANNEAU, corner_radius=0
        )
        entete.grid(row=0, column=0, columnspan=2, sticky="ew")
        entete.grid_columnconfigure(0, weight=1)

        titres = ctk.CTkFrame(entete, fg_color="transparent")
        titres.grid(row=0, column=0, sticky="w", padx=24, pady=14)

        ctk.CTkLabel(
            titres,
            text="Reconnaisseur de langage régulier",
            font=theme.police(22, "bold"),
            text_color=theme.TEXTE,
        ).pack(anchor="w")

        ctk.CTkLabel(
            titres,
            text="De l'expression à l'automate, puis au mot testé",
            font=theme.police(13),
            text_color=theme.TEXTE_DOUX,
        ).pack(anchor="w")

        self.interrupteur = ctk.CTkSwitch(
            entete,
            text="Thème clair",
            command=self._changer_theme,
            progress_color=theme.ACCENT,
            text_color=theme.TEXTE,
            font=theme.police(14),
        )
        self.interrupteur.grid(row=0, column=1, padx=24)

    def _creer_panneau_saisie(self):
        panneau = ctk.CTkFrame(
            self,
            fg_color=theme.PANNEAU,
            corner_radius=16,
            border_width=1,
            border_color=theme.BORD,
            width=380,
        )
        panneau.grid(
            row=1, column=0, sticky="ns",
            padx=(24, 12), pady=24
        )
        panneau.pack_propagate(False)

        self.champ_alphabet = self._creer_champ(
            panneau, "Alphabet", "par exemple : a b"
        )

        self.champ_expression = self._creer_champ(
            panneau,
            "Expression régulière",
            "par exemple : (a|b)*abb"
        )

        ctk.CTkLabel(
            panneau,
            text="Union : |     Étoile : *     Mot vide : @ ou ε",
            font=theme.police(12),
            text_color=theme.TEXTE_DOUX,
            wraplength=330,
            justify="left",
        ).pack(anchor="w", padx=22, pady=(10, 0))

        ctk.CTkLabel(
            panneau,
            text="Exemples",
            font=theme.police(14, "bold"),
            text_color=theme.TEXTE,
        ).pack(anchor="w", padx=22, pady=(22, 6))

        grille = ctk.CTkFrame(
            panneau, fg_color="transparent"
        )
        grille.pack(fill="x", padx=18)
        grille.grid_columnconfigure((0, 1), weight=1)

        for i, (alphabet, expression) in enumerate(EXEMPLES):
            ctk.CTkButton(
                grille,
                text=expression,
                height=34,
                corner_radius=10,
                fg_color=theme.CHAMP,
                hover_color=theme.BORD,
                text_color=theme.TEXTE,
                font=theme.police_code(14),
                command=lambda a=alphabet, e=expression:
                    self._charger_exemple(a, e),
            ).grid(
                row=i // 2, column=i % 2,
                padx=4, pady=4, sticky="ew"
            )

        ctk.CTkButton(
            panneau,
            text="Construire",
            height=46,
            corner_radius=12,
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_SURVOL,
            text_color=theme.TEXTE_SUR_ACCENT,
            font=theme.police(16, "bold"),
            command=self.construire,
        ).pack(fill="x", padx=22, pady=(26, 8))

        self.etiquette_erreur = ctk.CTkLabel(
            panneau,
            text="",
            font=theme.police(13),
            text_color=theme.ERREUR,
            wraplength=330,
            justify="left",
        )
        self.etiquette_erreur.pack(
            anchor="w", padx=22, pady=(4, 0)
        )

    def _creer_champ(self, parent, titre, indication):
        ctk.CTkLabel(
            parent,
            text=titre,
            font=theme.police(14, "bold"),
            text_color=theme.TEXTE,
        ).pack(anchor="w", padx=22, pady=(22, 6))

        champ = ctk.CTkEntry(
            parent,
            placeholder_text=indication,
            height=42,
            corner_radius=10,
            fg_color=theme.CHAMP,
            border_color=theme.BORD,
            text_color=theme.TEXTE,
            placeholder_text_color=theme.TEXTE_DOUX,
            font=theme.police_code(16),
        )
        champ.pack(fill="x", padx=22)
        champ.bind("<Return>", lambda _e: self.construire())

        return champ

    def _creer_resultats(self):
        self.onglets = ctk.CTkTabview(
            self,
            fg_color=theme.PANNEAU,
            corner_radius=16,
            border_width=1,
            border_color=theme.BORD,
            segmented_button_fg_color=theme.ONGLET_BARRE,
            segmented_button_selected_color=theme.ONGLET_ACTIF,
            segmented_button_selected_hover_color=theme.ONGLET_ACTIF_SURVOL,
            segmented_button_unselected_color=theme.ONGLET_INACTIF,
            segmented_button_unselected_hover_color=theme.ONGLET_INACTIF_SURVOL,
            text_color=theme.TEXTE_ONGLET,
        )

        self.onglets.grid(
            row=1, column=1, sticky="nsew",
            padx=(12, 24), pady=24
        )

        self.zones = {}

        for nom in ("Résumé", "AFN-ε", "AFD"):
            onglet = self.onglets.add(nom)

            zone = ctk.CTkTextbox(
                onglet,
                fg_color=theme.CHAMP,
                text_color=theme.TEXTE,
                corner_radius=12,
                font=theme.police_code(15),
                wrap="none",
            )
            zone.pack(
                fill="both", expand=True, padx=6, pady=6
            )

            self.zones[nom] = zone
            self._afficher_texte(nom, "")

        self._afficher_texte("Résumé", MESSAGE_ACCUEIL)

    def _afficher_texte(self, nom, texte):
        zone = self.zones[nom]
        zone.configure(state="normal")
        zone.delete("1.0", "end")
        zone.insert("1.0", texte)
        zone.configure(state="disabled")

    def _afficher_automate(
        self, nom, automate, chemin, avec_epsilon=False
    ):
        """Génère et affiche le dessin de l'automate."""

        image_path = dessin.dessiner(
            automate, chemin, avec_epsilon
        )

        image = Image.open(image_path)

        largeur, hauteur = image.size
        facteur = min(850 / largeur, 550 / hauteur, 1)

        taille = (
            max(1, int(largeur * facteur)),
            max(1, int(hauteur * facteur)),
        )

        photo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=taille,
        )

        onglet = self.onglets.tab(nom)

        for widget in onglet.winfo_children():
            widget.destroy()

        affichage = ctk.CTkLabel(
            onglet,
            text="",
            image=photo,
        )
        affichage.pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.images[nom] = photo

    def _charger_exemple(self, alphabet, expression):
        self.champ_alphabet.delete(0, "end")
        self.champ_alphabet.insert(0, alphabet)

        self.champ_expression.delete(0, "end")
        self.champ_expression.insert(0, expression)

        self.construire()

    def _changer_theme(self):
        if self.interrupteur.get() == 1:
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    def construire(self):
        """Construit et affiche les deux automates."""

        construction, erreur = moteur.construire(
            self.champ_alphabet.get(),
            self.champ_expression.get(),
        )

        if construction is None:
            self.etiquette_erreur.configure(text=erreur)
            return

        try:
            self.etiquette_erreur.configure(text="")
            self.construction = construction

            self._afficher_texte(
                "Résumé",
                moteur.resume_en_texte(construction),
            )

            self._afficher_automate(
                "AFN-ε",
                construction.afn,
                "automate_afn",
                True,
            )

            self._afficher_automate(
                "AFD",
                construction.afd,
                "automate_afd",
            )

            self.onglets.set("Résumé")

        except Exception as erreur:
            self.etiquette_erreur.configure(
                text=f"Erreur d'affichage : {erreur}"
            )


def lancer():
    """Ouvre la fenêtre."""
    Application().mainloop()


if __name__ == "__main__":
    lancer()
