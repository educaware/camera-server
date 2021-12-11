from typing import Any

import cv2
import numpy as np
from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from app.clients import clients
from app.stream import stream

router = APIRouter()


@router.websocket("")
async def accept_websocket(websocket: WebSocket) -> Any:
    """Endpoint for accepting incoming websocket connections."""
    await websocket.accept()

    # Save the websocket session.
    client = clients.add_client(websocket)

    while True:
        try:
            data = await websocket.receive()
            if data["type"] == "websocket.disconnect":
                raise WebSocketDisconnect

            if data.get("bytes"):
                # Receiving video frames and write them to the stream.
                nparr = np.fromstring(data["bytes"], np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                stream.write(frame)

            elif data.get("text"):
                print(data["text"])

        except WebSocketDisconnect:
            # Remove the client from `clients` if it disconnects.
            clients.remove(client)
            break
