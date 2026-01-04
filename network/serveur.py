import socket
import json
from game.game import Game

HOST = "0.0.0.0"
PORT = 5555

class GameServer:
    def __init__(self):
        self.game = Game(["Host", "Client"])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)

        print("Serveur LAN démarré")

    def start(self):
        conn, addr = self.sock.accept()
        print(f"Connexion de {addr}")

        while True:
            data = conn.recv(4096).decode()
            if not data:
                break

            message = json.loads(data)
            self.handle_action(message)

            conn.send(json.dumps(self.serialize()).encode())

    def handle_action(self, msg):
        if msg["action"] == "draw":
            player = self.game.players[self.game.current_player]
            player.draw_tile(self.game.deck.draw())
            self.game.next_turn()

    def serialize(self):
        return {
            "players": [p.to_dict() for p in self.game.players],
            "table": self.game.table.to_dict(),
            "current_player": self.game.current_player
        }

if __name__ == "__main__":
    GameServer().start()
