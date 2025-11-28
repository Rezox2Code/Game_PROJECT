from tkinter import *
from PIL import Image, ImageTk
import os
import csv

class PlateauCartes:
    def __init__(self, master):
        # --- Configuration de base ---
        self.master = master
        self.master.geometry('1600x900')
        self.master.configure(bg="#115A0E")
        self.master.title("Plateau de cartes (faces cachées avec repères)")

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DOSSIER_IMAGES = os.path.join(self.BASE_DIR, "cardDeck")
        self.CSV_PATH = os.path.join(self.BASE_DIR, "cardDeck.csv")

        # --- Paramètres du plateau ---
        self.largeur_carte = 100
        self.hauteur_carte = 150
        self.espacement_x = 10
        self.espacement_y = 10
        self.nb_colonnes = 13
        self.nb_lignes = 4

        # --- Listes pour repérage ---
        self.valeurs = ["as", "2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi"]
        self.symboles = ["coeur", "pique", "trefle", "carreau"]

        # --- Données ---
        self.cartes = []

        # --- Initialisation ---
        self.charger_cartes_depuis_csv()
        self.dessiner_repères()
        self.placer_cartes_grille()

    # --- Méthodes ---
    def charger_image(self, symbole, valeur, statut="face"):
        """Retourne une image PhotoImage selon la carte"""
        if statut == "dos":
            chemin = os.path.join(self.DOSSIER_IMAGES, "back.png")
        else:
            chemin = os.path.join(self.DOSSIER_IMAGES, f"{symbole}_{valeur}.png")

        if os.path.exists(chemin):
            image = Image.open(chemin).resize((self.largeur_carte, self.hauteur_carte))
            return ImageTk.PhotoImage(image)
        else:
            img = Image.new("RGB", (self.largeur_carte, self.hauteur_carte), color="#115A0E")
            return ImageTk.PhotoImage(img)

    def retourner_carte(self, event):
        """Retourne la carte uniquement si elle est encore face cachée"""
        carte = event.widget
        if getattr(carte, "stat", "dos") == "dos":
            carte.photo = self.charger_image(carte.symbole, carte.valeur, "face")
            carte.stat = "face"
            carte.create_image(0, 0, anchor=NW, image=carte.photo)
        # Sinon, ne fait rien si la carte est déjà face

    def creer_carte(self, symbole, valeur):
        """Crée une carte face cachée (dos visible)"""
        canvas = Canvas(
            self.master, width=self.largeur_carte, height=self.hauteur_carte,
            highlightthickness=1, highlightbackground="black", bg="#115A0E"
        )
        canvas.symbole = symbole
        canvas.valeur = valeur
        canvas.photo = self.charger_image(symbole, valeur, "dos")
        canvas.create_image(0, 0, anchor=NW, image=canvas.photo)
        canvas.stat = "dos"
        canvas.bind("<Button-1>", self.retourner_carte)  # Binding correct
        return canvas

    def charger_cartes_depuis_csv(self):
        """Charge les cartes à partir du fichier CSV"""
        try:
            with open(self.CSV_PATH, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for ligne_csv in reader:
                    symbole = ligne_csv["Couleur"].strip().lower()
                    valeur = ligne_csv["Valeur"].strip().lower()
                    carte = self.creer_carte(symbole, valeur)
                    self.cartes.append(carte)
        except FileNotFoundError:
            print("Fichier 'cardDeck.csv' introuvable !")
            self.master.destroy()
            exit()

    def dessiner_repères(self):
        """Affiche les titres des colonnes et lignes"""
        decalage_x_depart = 100  # Même décalage que les cartes
        # Titres des colonnes (valeurs)
        for i, val in enumerate(self.valeurs):
            x = decalage_x_depart + i * (self.largeur_carte + self.espacement_x) + self.largeur_carte / 2
            label = Label(
                self.master, text=val.upper(), bg="#115A0E", fg="white",
                font=("Arial", 14, "bold")
            )
            label.place(x=x - 20, y=5)

        # Titres des lignes (symboles)
        for j, sym in enumerate(self.symboles):
            y = (j * (self.hauteur_carte + self.espacement_y)) + self.hauteur_carte / 2 + 30
            label = Label(
                self.master, text=sym.capitalize(), bg="#115A0E", fg="white",
                font=("Arial", 14, "bold")
            )
            label.place(x=10, y=y - 30)

    def placer_cartes_grille(self):
        """Dispose les cartes selon les lignes et colonnes logiques"""
        for carte in self.cartes:
            if carte.symbole in self.symboles and carte.valeur in self.valeurs:
                i = self.valeurs.index(carte.valeur)
                j = self.symboles.index(carte.symbole)
                x = (i * (self.largeur_carte + self.espacement_x)) + 100
                y = (j * (self.hauteur_carte + self.espacement_y)) + 50
                carte.place(x=x, y=y)


# --- Exécution ---
if __name__ == "__main__":
    root = Tk()
    app = PlateauCartes(root)
    root.mainloop()
