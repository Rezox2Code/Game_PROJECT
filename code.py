from tkinter import *
from PIL import Image, ImageTk
import os
import csv
import random

class JeuCartesMelangees:
    def __init__(self, master):
        self.master = master
        self.master.geometry('1600x900')
        self.master.configure(bg="#115A0E")
        self.master.title("Jeu de cartes à placer")

        # --- Chemins ---
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DOSSIER_IMAGES = os.path.join(self.BASE_DIR, "cardDeck")
        self.CSV_PATH = os.path.join(self.BASE_DIR, "cardDeck.csv")

        # --- Paramètres ---
        self.largeur_carte = 100
        self.hauteur_carte = 150
        self.espacement_x = 10
        self.espacement_y = 10

        # --- Listes de repères ---
        self.valeurs = ["as", "2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi"]
        self.symboles = ["coeur", "pique", "trefle", "carreau"]

        # --- Données ---
        self.cartes = []
        self.emplacements = {}  # (symbole, valeur) -> (x, y)
        self.carte_selectionnee = None

        # --- Initialisation ---
        self.charger_cartes_depuis_csv()
        random.shuffle(self.cartes)  # Mélange complet
        self.dessiner_repères()
        self.creer_emplacements()
        self.melanger_cartes_aleatoire()

    def charger_image(self, symbole, valeur):
        chemin = os.path.join(self.DOSSIER_IMAGES, f"{symbole}_{valeur}.png")
        if os.path.exists(chemin):
            image = Image.open(chemin).resize((self.largeur_carte, self.hauteur_carte))
            return ImageTk.PhotoImage(image)
        else:
            img = Image.new("RGB", (self.largeur_carte, self.hauteur_carte), color="#115A0E")
            return ImageTk.PhotoImage(img)

    def creer_carte(self, symbole, valeur):
        canvas = Canvas(self.master, width=self.largeur_carte, height=self.hauteur_carte,
                        highlightthickness=1, highlightbackground="black", bg="#115A0E")
        canvas.symbole = symbole
        canvas.valeur = valeur
        canvas.photo = self.charger_image(symbole, valeur)
        canvas.create_image(0, 0, anchor=NW, image=canvas.photo)
        canvas.bind("<Button-1>", self.selectionner_carte)
        self.cartes.append(canvas)

    def charger_cartes_depuis_csv(self):
        try:
            with open(self.CSV_PATH, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for ligne in reader:
                    symbole = ligne["Couleur"].strip().lower()
                    valeur = ligne["Valeur"].strip().lower()
                    self.creer_carte(symbole, valeur)
        except FileNotFoundError:
            print("Fichier 'cardDeck.csv' introuvable !")
            self.master.destroy()
            exit()

    def dessiner_repères(self):
        decalage_x = 100
        for i, val in enumerate(self.valeurs):
            x = decalage_x + i * (self.largeur_carte + self.espacement_x) + self.largeur_carte / 2
            label = Label(self.master, text=val.upper(), bg="#115A0E", fg="white",
                          font=("Arial", 14, "bold"))
            label.place(x=x - 20, y=5)

        for j, sym in enumerate(self.symboles):
            y = (j * (self.hauteur_carte + self.espacement_y)) + self.hauteur_carte / 2 + 30
            label = Label(self.master, text=sym.capitalize(), bg="#115A0E", fg="white",
                          font=("Arial", 14, "bold"))
            label.place(x=10, y=y - 30)

    def creer_emplacements(self):
        decalage_x = 100
        decalage_y = 50
        for j, sym in enumerate(self.symboles):
            for i, val in enumerate(self.valeurs):
                x = decalage_x + i * (self.largeur_carte + self.espacement_x)
                y = decalage_y + j * (self.hauteur_carte + self.espacement_y)
                self.emplacements[(sym, val)] = (x, y)

    def melanger_cartes_aleatoire(self):
        """Place les cartes mélangées aléatoirement sur le plateau"""
        positions = [(random.randint(50, 1400), random.randint(100, 700)) for _ in self.cartes]
        for carte, pos in zip(self.cartes, positions):
            carte.place(x=pos[0], y=pos[1])

    def selectionner_carte(self, event):
        carte = event.widget
        if self.carte_selectionnee is None:
            self.carte_selectionnee = carte
            carte.config(highlightbackground="yellow", highlightthickness=3)
        else:
            # Vérifier si l'emplacement cible est libre
            target = self.emplacements[(self.carte_selectionnee.symbole, self.carte_selectionnee.valeur)]
            occupe = any(
                c != self.carte_selectionnee and
                abs(c.winfo_x() - target[0]) < 5 and
                abs(c.winfo_y() - target[1]) < 5
                for c in self.cartes
            )
            if not occupe:
                self.carte_selectionnee.place(x=target[0], y=target[1])
            self.carte_selectionnee.config(highlightbackground="black", highlightthickness=1)
            self.carte_selectionnee = None


if __name__ == "__main__":
    root = Tk()
    app = JeuCartesMelangees(root)
    root.mainloop()
