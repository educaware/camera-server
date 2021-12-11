from typing import Any, List

from fastapi import APIRouter, HTTPException, Response, status

from app import schemas
from app.clients import clients

router = APIRouter()


@router.get("", response_model=List[schemas.ClientBase])
async def read_clients() -> Any:
    """Retrieve all connected clients."""
    return [{"host": client.websocket.client.host, "port": client.websocket.client.port} for client in clients]


@router.get("/{host}/{port}", response_model=schemas.ClientBase)
async def read_client(host: str, port: int) -> Any:
    """Retrieve a specific client."""
    client = clients.get(host, port)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The client with this name does not exist in the system.",
        )

    websocket = client.websocket
    return {"host": websocket.client.host, "port": websocket.client.port}


@router.delete("/{host}/{port}", status_code=status.HTTP_200_OK, response_class=Response)
async def close_client(host: str, port: int) -> Any:
    """Close a specific client."""
    client = clients.get(host, port)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The client with this name does not exist in the system.",
        )

    websocket = client.websocket
    await websocket.send_text("close")


@router.get("/{host}/{port}/camera", response_model=schemas.CameraBase)
async def read_camera_status(host: str, port: int) -> Any:
    """Toggle a specific client's camera."""
    client = clients.get(host, port)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The client with this name does not exist in the system.",
        )

    return {"on": client.camera.on}


@router.post("/{host}/{port}/camera/toggle", status_code=status.HTTP_200_OK, response_class=Response)
async def toggle_client_camera(host: str, port: int) -> Any:
    """Toggle a specific client's camera."""
    client = clients.get(host, port)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The client with this name does not exist in the system.",
        )

    websocket = client.websocket
    if client.camera.on:
        await websocket.send_text("off")
        client.camera.on = False
    else:
        await websocket.send_text("on")
        client.camera.on = True


@router.post("/{host}/{port}/camera/switch", status_code=status.HTTP_200_OK, response_class=Response)
async def switch_client_camera(host: str, port: int, on: bool) -> Any:
    """Switch a specific client's camera to on/off."""
    client = clients.get(host, port)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The client with this name does not exist in the system.",
        )

    websocket = client.websocket

    if on:
        await websocket.send_text("on")
        client.camera.on = True
    else:
        await websocket.send_text("off")
        client.camera.on = False


@router.post("/{host}/{port}/camera/blink", status_code=status.HTTP_200_OK, response_class=Response)
async def blink_client_camera(host: str, port: int, repeat: int, delay: int) -> Any:
    """Blink a specific client's camera."""
    client = clients.get(host, port)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The client with this name does not exist in the system.",
        )

    websocket = client.websocket
    await websocket.send_text(f"blink,{repeat},{delay}")
