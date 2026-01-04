from game.game import Game

game = Game(["Joueur1", "Joueur2"])

print("Début du jeu")
for p in game.players:
    print(p)

game.save()
print("Partie sauvegardée")
