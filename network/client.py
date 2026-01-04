import socket
import json

class GameClient:
    def __init__(self, host_ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host_ip, 5555))

    def send(self, action):
        self.sock.send(json.dumps(action).encode())
        return json.loads(self.sock.recv(4096).decode())
