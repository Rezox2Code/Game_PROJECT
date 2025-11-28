import pandas as pd
import random

# Définir les couleurs et valeurs (sans accents)
couleurs = ["carreau", "pique", "trefle", "coeur"]
valeurs = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi"]

# Créer la liste complète des cartes
cartes = [{"Couleur": couleur, "Valeur": valeur} for couleur in couleurs for valeur in valeurs]

# Mélanger aléatoirement les cartes
random.shuffle(cartes)

# Convertir en DataFrame
df = pd.DataFrame(cartes)

# Sauvegarder en CSV
df.to_csv("projet1/cardDeck.csv", index=False, encoding="utf-8")

print("Fichier CSV généré : cardDeck.csv")