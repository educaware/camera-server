from typing import List

from fastapi import WebSocket

from app.schemas import CameraBase


class Client:
    """Represents a session object."""

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.camera = CameraBase(on=False)


class Clients:
    """Stores the connected sessions."""

    def __init__(self):
        self._clients: List[Client] = []

    def __iter__(self):
        for client in self._clients:
            yield client

    def add_client(self, websocket: WebSocket):
        """Add a session to `_sessions`"""
        client = Client(websocket)

        self._clients.append(client)
        return client

    def remove(self, client: Client):
        self._clients.remove(client)

    def get(self, host: str, port: int):
        """Get a specific session from its host and port."""
        for client in self:
            websocket = client.websocket
            if host == websocket.client.host and port == websocket.client.port:
                return client


clients = Clients()
