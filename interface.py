
"""Interface graphique moderne — Automata Studio."""

import customtkinter as ctk
import moteur
import theme
import dessin
from PIL import Image


class Application(ctk.CTk):

    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()

        self.title("Automata Studio")
        self.geometry("1400x850")
        self.minsize(1100, 700)
        self.configure(fg_color="#091521")

        self.construction = None
        self.images = {}
        self.pages = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._creer_navigation()
        self._creer_espace_principal()

        self.afficher_page("Accueil")
        self.bind("<Control-Return>", lambda e: self.construire())

    # ---------------- NAVIGATION ----------------

    def _creer_navigation(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color="#101F30"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="◈  AUTOMATA",
            font=("Segoe UI", 24, "bold"),
            text_color="#42D6CF"
        ).pack(pady=(35, 4))

        ctk.CTkLabel(
            self.sidebar,
            text="STUDIO",
            font=("Segoe UI", 12, "bold"),
            text_color="#8B9CAF"
        ).pack(pady=(0, 35))

        self.boutons_navigation = {}

        elements = [
            ("⌂", "Accueil"),
            ("◇", "Constructeur"),
            ("✓", "Reconnaissance"),
            ("▦", "Transitions"),
            ("◷", "Historique"),
            ("⇧", "Exportation"),
            ("?", "Aide"),
            ("⚙", "Paramètres"),
        ]

        for symbole, nom in elements:

            bouton = ctk.CTkButton(
                self.sidebar,
                text=f"   {symbole}    {nom}",
                anchor="w",
                height=45,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#20384D",
                text_color="#DCE8F2",
                font=("Segoe UI", 14),
                command=lambda n=nom: self.afficher_page(n)
            )

            bouton.pack(fill="x", padx=16, pady=4)
            self.boutons_navigation[nom] = bouton

        ctk.CTkLabel(
            self.sidebar,
            text="VERSION 1.0",
            text_color="#647A8F",
            font=("Segoe UI", 11)
        ).pack(side="bottom", pady=20)

    # ---------------- ESPACE PRINCIPAL ----------------

    def _creer_espace_principal(self):

        self.espace = ctk.CTkFrame(
            self,
            fg_color="#091521",
            corner_radius=0
        )
        self.espace.grid(row=0, column=1, sticky="nsew")
        self.espace.grid_rowconfigure(1, weight=1)
        self.espace.grid_columnconfigure(0, weight=1)

        self.entete = ctk.CTkFrame(
            self.espace,
            fg_color="#101F30",
            corner_radius=0,
            height=75
        )
        self.entete.grid(row=0, column=0, sticky="ew")
        self.entete.grid_columnconfigure(0, weight=1)

        self.titre_page = ctk.CTkLabel(
            self.entete,
            text="Accueil",
            font=("Segoe UI", 23, "bold"),
            text_color="#F0F6FC"
        )
        self.titre_page.grid(
            row=0, column=0, sticky="w", padx=30, pady=20
        )

        self.zone_pages = ctk.CTkFrame(
            self.espace,
            fg_color="transparent"
        )
        self.zone_pages.grid(
            row=1, column=0, sticky="nsew", padx=25, pady=25
        )
        self.zone_pages.grid_columnconfigure(0, weight=1)
        self.zone_pages.grid_rowconfigure(0, weight=1)

        self._creer_pages()

    # ---------------- OUTILS GRAPHIQUES ----------------

    def _nouvelle_page(self, nom):

        page = ctk.CTkFrame(
            self.zone_pages,
            fg_color="transparent"
        )
        page.grid(row=0, column=0, sticky="nsew")
        self.pages[nom] = page
        return page

    def _titre(self, parent, texte, taille=22):

        ctk.CTkLabel(
            parent,
            text=texte,
            font=("Segoe UI", taille, "bold"),
            text_color="#EAF2F8"
        ).pack(anchor="w", pady=(5, 12))

    def _carte(self, parent):

        return ctk.CTkFrame(
            parent,
            fg_color="#14283B",
            corner_radius=16,
            border_width=1,
            border_color="#25445C"
        )

    # ---------------- CRÉATION DES PAGES ----------------

    def _creer_pages(self):

        self._page_accueil()
        self._page_constructeur()
        self._page_reconnaissance()
        self._page_transitions()
        self._page_historique()
        self._page_exportation()
        self._page_aide()
        self._page_parametres()

    # ---------------- ACCUEIL ----------------

    def _page_accueil(self):

        page = self._nouvelle_page("Accueil")

        self._titre(page, "Bienvenue dans Automata Studio", 27)

        ctk.CTkLabel(
            page,
            text="Construisez, visualisez et testez vos automates finis.",
            font=("Segoe UI", 15),
            text_color="#91A9BE"
        ).pack(anchor="w", pady=(0, 25))

        statistiques = ctk.CTkFrame(
            page, fg_color="transparent"
        )
        statistiques.pack(fill="x")
        statistiques.grid_columnconfigure((0, 1, 2), weight=1)

        donnees = [
            ("01", "Constructeur"),
            ("02", "Types d'automates"),
            ("03", "Reconnaissance")
        ]

        for i, (nombre, titre) in enumerate(donnees):

            carte = self._carte(statistiques)
            carte.grid(
                row=0, column=i, sticky="ew", padx=7, pady=7
            )

            ctk.CTkLabel(
                carte,
                text=nombre,
                font=("Segoe UI", 32, "bold"),
                text_color="#42D6CF"
            ).pack(pady=(20, 5))

            ctk.CTkLabel(
                carte,
                text=titre,
                font=("Segoe UI", 14),
                text_color="#DCE8F2"
            ).pack(pady=(0, 20))

        carte = self._carte(page)
        carte.pack(fill="x", padx=7, pady=25)

        self._titre(carte, "Commencer rapidement")

        ctk.CTkLabel(
            carte,
            text=(
                "1. Saisissez votre alphabet.\n"
                "2. Entrez une expression régulière.\n"
                "3. Construisez votre automate.\n"
                "4. Visualisez les résultats."
            ),
            font=("Segoe UI", 15),
            text_color="#B7C9D9",
            justify="left"
        ).pack(anchor="w", padx=25, pady=(0, 20))

        ctk.CTkButton(
            page,
            text="Ouvrir le constructeur →",
            height=48,
            fg_color="#168F9C",
            hover_color="#20AEB3",
            font=("Segoe UI", 15, "bold"),
            command=lambda: self.afficher_page("Constructeur")
        ).pack(anchor="w", padx=7)

    # ---------------- CONSTRUCTEUR ----------------

    def _page_constructeur(self):

        page = self._nouvelle_page("Constructeur")
        page.grid_columnconfigure(1, weight=1)
        page.grid_rowconfigure(0, weight=1)

        gauche = self._carte(page)
        gauche.grid(
            row=0, column=0, sticky="ns", padx=(0, 15)
        )
        gauche.configure(width=350)
        gauche.grid_propagate(False)

        self._titre(gauche, "Paramètres de construction")

        ctk.CTkLabel(
            gauche,
            text="Alphabet",
            text_color="#C8D8E7"
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.champ_alphabet = ctk.CTkEntry(
            gauche,
            placeholder_text="Exemple : a b",
            height=43,
            font=("Consolas", 15),
            fg_color="#0C1B2A",
            border_color="#31536C"
        )
        self.champ_alphabet.pack(fill="x", padx=20)

        ctk.CTkLabel(
            gauche,
            text="Expression régulière",
            text_color="#C8D8E7"
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.champ_expression = ctk.CTkEntry(
            gauche,
            placeholder_text="Exemple : (a|b)*abb",
            height=43,
            font=("Consolas", 15),
            fg_color="#0C1B2A",
            border_color="#31536C"
        )
        self.champ_expression.pack(fill="x", padx=20)

        ctk.CTkLabel(
            gauche,
            text="Union : |     Étoile : *\nMot vide : @ ou ε",
            text_color="#829CB1",
            font=("Segoe UI", 12)
        ).pack(anchor="w", padx=20, pady=15)

        ctk.CTkButton(
            gauche,
            text="CONSTRUIRE L'AUTOMATE",
            height=48,
            fg_color="#168F9C",
            hover_color="#20AEB3",
            font=("Segoe UI", 14, "bold"),
            command=self.construire
        ).pack(fill="x", padx=20, pady=15)

        self.etiquette_erreur = ctk.CTkLabel(
            gauche,
            text="",
            text_color="#FF7777",
            wraplength=300
        )
        self.etiquette_erreur.pack(padx=20)

        droite = self._carte(page)
        droite.grid(row=0, column=1, sticky="nsew")
        droite.grid_columnconfigure(0, weight=1)
        droite.grid_rowconfigure(0, weight=1)

        self.onglets = ctk.CTkTabview(
            droite,
            fg_color="#14283B",
            segmented_button_selected_color="#168F9C",
            segmented_button_selected_hover_color="#20AEB3"
        )
        self.onglets.grid(
            row=0, column=0, sticky="nsew", padx=12, pady=12
        )

        self.zones = {}

        for nom in ("Résumé", "AFN-ε", "AFD"):

            onglet = self.onglets.add(nom)

            zone = ctk.CTkTextbox(
                onglet,
                fg_color="#0C1B2A",
                text_color="#DCE8F2",
                font=("Consolas", 14),
                corner_radius=12
            )
            zone.pack(fill="both", expand=True, padx=5, pady=5)

            self.zones[nom] = zone
            self._afficher_texte(nom, "En attente de construction...")

        self._afficher_texte(
            "Résumé",
            "Saisissez les paramètres pour commencer."
        )

    # ---------------- RECONNAISSANCE ----------------

    def _page_reconnaissance(self):

        page = self._nouvelle_page("Reconnaissance")

        self._titre(page, "Reconnaissance des mots")

        carte = self._carte(page)
        carte.pack(fill="x", pady=10)

        ctk.CTkLabel(
            carte,
            text="Cette fonction sera disponible après la construction d'un automate.",
            text_color="#AFC4D5",
            font=("Segoe UI", 15)
        ).pack(padx=20, pady=25)

        self.champ_mot = ctk.CTkEntry(
            carte,
            placeholder_text="Entrez un mot à tester",
            height=45,
            font=("Consolas", 15)
        )
        self.champ_mot.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            carte,
            text="Tester le mot",
            height=43,
            fg_color="#168F9C",
            command=self.reconnaitre_mot
        ).pack(anchor="w", padx=20, pady=(5, 20))

        self.resultat_mot = ctk.CTkTextbox(
            page,
            height=200,
            fg_color="#0C1B2A",
            text_color="#DCE8F2",
            font=("Consolas", 14)
        )
        self.resultat_mot.pack(fill="both", expand=True, pady=10)

    # ---------------- TRANSITIONS ----------------

    def _page_transitions(self):

        page = self._nouvelle_page("Transitions")
        self._titre(page, "Tables de transitions")

        self.table_texte = ctk.CTkTextbox(
            page,
            fg_color="#0C1B2A",
            text_color="#DCE8F2",
            font=("Consolas", 14)
        )
        self.table_texte.pack(fill="both", expand=True)

        self.table_texte.insert(
            "1.0", "Construisez un automate pour afficher sa table."
        )

    # ---------------- HISTORIQUE ----------------

    def _page_historique(self):

        page = self._nouvelle_page("Historique")
        self._titre(page, "Historique des constructions")

        self.historique_texte = ctk.CTkTextbox(
            page,
            fg_color="#0C1B2A",
            text_color="#DCE8F2",
            font=("Consolas", 14)
        )
        self.historique_texte.pack(fill="both", expand=True)

        self.historique_texte.insert("1.0", "Aucune construction pour le moment.")

    # ---------------- EXPORTATION ----------------

    def _page_exportation(self):

        page = self._nouvelle_page("Exportation")
        self._titre(page, "Exporter les automates")

        ctk.CTkLabel(
            page,
            text="L'exportation sera activée après la construction d'un automate.",
            text_color="#AFC4D5",
            font=("Segoe UI", 15)
        ).pack(anchor="w", pady=15)

        ctk.CTkButton(
            page,
            text="Exporter l'AFN-ε en PNG",
            height=45,
            fg_color="#168F9C",
            command=lambda: self.exporter("AFN")
        ).pack(anchor="w", pady=10)

        ctk.CTkButton(
            page,
            text="Exporter l'AFD en PNG",
            height=45,
            fg_color="#7255B5",
            command=lambda: self.exporter("AFD")
        ).pack(anchor="w", pady=10)

    # ---------------- AIDE ----------------

    def _page_aide(self):

        page = self._nouvelle_page("Aide")
        self._titre(page, "Centre d'aide")

        texte = (
            "AUTOMATA STUDIO\n\n"
            "Cette application permet de transformer une expression "
            "régulière en automate.\n\n"
            "NOTIONS PRINCIPALES\n\n"
            "• Alphabet : ensemble des symboles autorisés.\n"
            "• Union : opérateur |.\n"
            "• Étoile : opérateur *.\n"
            "• Mot vide : @ ou ε.\n"
            "• AFN-ε : automate non déterministe avec transitions epsilon.\n"
            "• AFD : automate fini déterministe.\n\n"
            "UTILISATION\n\n"
            "1. Ouvrir le constructeur.\n"
            "2. Saisir l'alphabet.\n"
            "3. Saisir l'expression régulière.\n"
            "4. Cliquer sur Construire.\n"
            "5. Consulter les résultats."
        )

        zone = ctk.CTkTextbox(
            page,
            fg_color="#14283B",
            text_color="#DCE8F2",
            font=("Segoe UI", 15)
        )
        zone.pack(fill="both", expand=True)
        zone.insert("1.0", texte)
        zone.configure(state="disabled")

    # ---------------- PARAMÈTRES ----------------

    def _page_parametres(self):

        page = self._nouvelle_page("Paramètres")
        self._titre(page, "Paramètres de l'application")

        ctk.CTkLabel(
            page,
            text="Apparence",
            font=("Segoe UI", 16, "bold"),
            text_color="#DCE8F2"
        ).pack(anchor="w", pady=15)

        self.theme_switch = ctk.CTkSwitch(
            page,
            text="Activer le thème clair",
            command=self.changer_theme
        )
        self.theme_switch.pack(anchor="w", pady=10)

        ctk.CTkLabel(
            page,
            text="Automata Studio — Version 1.0",
            text_color="#829CB1"
        ).pack(anchor="w", pady=30)

    # ---------------- AFFICHAGE DES PAGES ----------------

    def afficher_page(self, nom):

        self.titre_page.configure(text=nom)

        for page in self.pages.values():
            page.grid_remove()

        self.pages[nom].grid()

        for titre, bouton in self.boutons_navigation.items():
            bouton.configure(
                fg_color="#168F9C" if titre == nom else "transparent"
            )

    # ---------------- CONSTRUCTION ----------------

    def _afficher_texte(self, nom, texte):

        zone = self.zones[nom]
        zone.configure(state="normal")
        zone.delete("1.0", "end")
        zone.insert("1.0", texte)
        zone.configure(state="disabled")

    def _afficher_automate(self, nom, automate, chemin, avec_epsilon=False):

        image_path = dessin.dessiner(
            automate, chemin, avec_epsilon
        )

        image = Image.open(image_path)

        largeur, hauteur = image.size
        facteur = min(850 / largeur, 550 / hauteur, 1)

        taille = (
            max(1, int(largeur * facteur)),
            max(1, int(hauteur * facteur))
        )

        photo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=taille
        )

        onglet = self.onglets.tab(nom)

        for widget in onglet.winfo_children():
            widget.destroy()

        affichage = ctk.CTkLabel(
            onglet,
            text="",
            image=photo
        )
        affichage.pack(fill="both", expand=True, padx=10, pady=10)

        self.images[nom] = photo

    def construire(self):

        construction, erreur = moteur.construire(
            self.champ_alphabet.get(),
            self.champ_expression.get()
        )

        if construction is None:
            self.etiquette_erreur.configure(text=erreur)
            return

        try:
            self.etiquette_erreur.configure(text="")
            self.construction = construction

            self._afficher_texte(
                "Résumé",
                moteur.resume_en_texte(construction)
            )

            self._afficher_automate(
                "AFN-ε", construction.afn,
                "automate_afn", True
            )

            self._afficher_automate(
                "AFD", construction.afd,
                "automate_afd"
            )

            self.onglets.set("Résumé")

            self.table_texte.configure(state="normal")
            self.table_texte.delete("1.0", "end")
            self.table_texte.insert(
                "1.0",
                "TABLE DE L'AFD\n\n" +
                moteur.table_en_texte(construction.afd)
            )
            self.table_texte.configure(state="disabled")

            self.historique_texte.configure(state="normal")
            self.historique_texte.insert(
                "1.0",
                construction.expression + "\n"
            )
            self.historique_texte.configure(state="disabled")

            self.afficher_page("Constructeur")

        except Exception as erreur:
            self.etiquette_erreur.configure(
                text=f"Erreur d'affichage : {erreur}"
            )

    # ---------------- TEST DES MOTS ----------------

    def reconnaitre_mot(self):

        if self.construction is None:
            self.resultat_mot.delete("1.0", "end")
            self.resultat_mot.insert(
                "1.0", "Construisez d'abord un automate."
            )
            return

        from reconnaissance import reconnaitre

        mot, erreur = moteur.preparer_mot(
            self.champ_mot.get(),
            self.construction.alphabet
        )

        self.resultat_mot.delete("1.0", "end")

        if erreur:
            self.resultat_mot.insert("1.0", erreur)
            return

        accepte, trace, raison = reconnaitre(
            self.construction.afd, mot
        )

        resultat = "MOT ACCEPTÉ" if accepte else "MOT REJETÉ"

        self.resultat_mot.insert(
            "1.0",
            resultat + "\n\n" + str(raison) +
            "\n\nTrace :\n" + str(trace)
        )

    # ---------------- EXPORTATION PNG ----------------

    def exporter(self, type_automate):

        if self.construction is None:
            self.etiquette_erreur.configure(
                text="Construisez d'abord un automate."
            )
            return

        from tkinter import filedialog
        import shutil

        if type_automate == "AFN":
            source = "automate_afn.png"
        else:
            source = "automate_afd.png"

        destination = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Image PNG", "*.png")],
            initialfile=f"{type_automate.lower()}.png"
        )

        if destination:
            shutil.copyfile(source, destination)

    # ---------------- THÈME ----------------

    def changer_theme(self):

        mode = "light" if self.theme_switch.get() == 1 else "dark"
        ctk.set_appearance_mode(mode)


def lancer():
    Application().mainloop()


if __name__ == "__main__":
    lancer()
