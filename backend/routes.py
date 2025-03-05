import asyncio
import logging
import threading

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from serial import Serial, SerialException

from utils import state, SERIAL_PORT, BAUD_RATE, write_data, reset_state

router = APIRouter()


class DataCollectionRequest(BaseModel):
    label: str
    duration: int


@router.post("/collect", status_code=status.HTTP_201_CREATED)
async def collect(request: DataCollectionRequest) -> dict:
    if state["collecting"]:
        raise HTTPException(
            status_code=400, detail="Data collection already in progress"
        )

    try:
        ser = Serial(SERIAL_PORT, BAUD_RATE, bytesize=8, parity="N", stopbits=1)
    except SerialException as e:
        logging.error(f"Could not open serial port: {e}")
        reset_state()
        raise HTTPException(status_code=500, detail="Error opening serial port")

    thread = threading.Thread(target=asyncio.run, args=(write_data(request, ser),))
    thread.start()

    return {"message": "Data collection started"}


@router.get("/status")
async def get_status():
    return state
