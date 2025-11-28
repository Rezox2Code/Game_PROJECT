from tkinter import *
from PIL import Image, ImageTk
import os
import csv
import random

# --- Configuration de base ---
root = Tk()
root.geometry('1600x900')
root.configure(bg="#115A0E")
root.title("Plateau de cartes (faces cachées avec repères)")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOSSIER_IMAGES = os.path.join(BASE_DIR, "cardDeck")
CSV_PATH = os.path.join(BASE_DIR, "cardDeck.csv")

# --- Paramètres du plateau ---
largeur_carte = 100
hauteur_carte = 150
espacement_x = 10
espacement_y = 10
nb_colonnes = 13
nb_lignes = 4

# --- Listes pour repérage ---
valeurs = ["as", "2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi"]
symboles = ["coeur", "pique", "trefle", "carreau"]

# --- Données globales ---
cartes = []


def charger_image(symbole, valeur, statut="face"):
    """Retourne une image PhotoImage selon la carte"""
    if statut == "dos":
        chemin = os.path.join(DOSSIER_IMAGES, "back.png")
    else:
        chemin = os.path.join(DOSSIER_IMAGES, f"{symbole}_{valeur}.png")

    if os.path.exists(chemin):
        image = Image.open(chemin).resize((largeur_carte, hauteur_carte))
        return ImageTk.PhotoImage(image)
    else:
        img = Image.new("RGB", (largeur_carte, hauteur_carte), color="#115A0E")
        return ImageTk.PhotoImage(img)


def retourner_carte(event):
    """Inverse l'image (face <-> dos) lors du clic"""
    carte = event.widget
    if getattr(carte, "stat", "dos") == "dos":
        # Montre la face
        carte.photo = charger_image(carte.symbole, carte.valeur, "face")
        carte.stat = "face"
    else:
        # Cache la carte (dos)
        carte.photo = charger_image(carte.symbole, carte.valeur, "dos")
        carte.stat = "dos"
    carte.create_image(0, 0, anchor=NW, image=carte.photo)


def creer_carte(parent, symbole, valeur):
    """Crée une carte face cachée (dos visible)"""
    canvas = Canvas(
        parent, width=largeur_carte, height=hauteur_carte,
        highlightthickness=1, highlightbackground="black", bg="#115A0E"
    )
    canvas.symbole = symbole
    canvas.valeur = valeur
    canvas.photo = charger_image(symbole, valeur, "dos")
    canvas.create_image(0, 0, anchor=NW, image=canvas.photo)
    canvas.stat = "dos"
    canvas.bind("<Button-1>", retourner_carte)
    return canvas


def charger_cartes_depuis_csv():
    """Charge les cartes à partir du fichier CSV"""
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for ligne_csv in reader:
                symbole = ligne_csv["Couleur"].strip().lower()
                valeur = ligne_csv["Valeur"].strip().lower()
                carte = creer_carte(root, symbole, valeur)
                cartes.append(carte)
    except FileNotFoundError:
        print("Fichier 'cardDeck.csv' introuvable !")
        root.destroy()
        exit()


def dessiner_repères():
    """Affiche les titres des colonnes et lignes"""
    # Titres des colonnes (valeurs)
    for i, val in enumerate(valeurs):
        x = (i * (largeur_carte + espacement_x)) + largeur_carte / 2
        label = Label(
            root, text=val.upper(), bg="#115A0E", fg="white",
            font=("Arial", 14, "bold")
        )
        label.place(x=x - 25, y=5)

    # Titres des lignes (symboles)
    for j, sym in enumerate(symboles):
        y = (j * (hauteur_carte + espacement_y)) + hauteur_carte / 2 + 30
        label = Label(
            root, text=sym.capitalize(), bg="#115A0E", fg="white",
            font=("Arial", 14, "bold")
        )
        label.place(x=10, y=y - 30)


def placer_cartes_grille():
    """Dispose les cartes selon les lignes et colonnes logiques"""
    for carte in cartes:
        if carte.symbole in symboles and carte.valeur in valeurs:
            i = valeurs.index(carte.valeur)
            j = symboles.index(carte.symbole)
            x = (i * (largeur_carte + espacement_x)) + 100
            y = (j * (hauteur_carte + espacement_y)) + 50
            carte.place(x=x, y=y)


# --- Exécution ---
charger_cartes_depuis_csv()
dessiner_repères()
placer_cartes_grille()

root.mainloop()
