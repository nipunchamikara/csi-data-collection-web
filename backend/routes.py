import asyncio
import os
import threading

from fastapi import APIRouter, status, HTTPException
from serial import Serial

from collect import collect_state, write_data
from models import DataCollectionRequest

SERIAL_PORT = os.getenv("SERIAL_PORT")
BAUD_RATE = int(os.getenv("BAUD_RATE"))
router = APIRouter()

ser = Serial(SERIAL_PORT, BAUD_RATE, bytesize=8, parity="N", stopbits=1)


@router.post("/collect", status_code=status.HTTP_201_CREATED)
async def collect(request: DataCollectionRequest) -> dict:
    if collect_state["collecting"]:
        raise HTTPException(
            status_code=400, detail="Data collection already in progress"
        )

    thread = threading.Thread(target=asyncio.run, args=(write_data(request, ser),))
    thread.start()

    return {"message": "Data collection started"}


@router.get("/collect/status")
async def get_collect_status():
    return collect_state
