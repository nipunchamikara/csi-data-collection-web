import logging
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from serial.serialutil import SerialException

load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT")
BAUD_RATE = int(os.getenv("BAUD_RATE"))
BUFFER_SIZE = int(os.getenv("BUFFER_SIZE"))

HEADER = (
    "type,time_index,device_id,recv_device_id,mac,rssi,rate,sig_mode,mcs,cwb,"
    "smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,"
    "channel,secondary_channel,timestamp,ant,sig_len,rx_state,len,csi_data\n"
)

# Global state
state = {
    "timeElapsed": 0.0,
    "totalTime": 0.0,
    "linesCollected": 0,
    "collecting": False,
    "error": "",
}


async def write_data(request, ser) -> None:
    """
    Write serial data to a CSV file.
    Args:
        request: DataCollectionRequest object
        ser: Serial object to read data from

    Returns:
        None
    """
    folder_name = "data"
    os.makedirs(folder_name, exist_ok=True)

    logging.info(
        f"Starting '{request.label}' data collection for {request.duration} seconds."
    )
    with open(
            f"{folder_name}/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}_{request.label}.csv",
            "w",
            newline="",
    ) as file:
        file.write(HEADER)
        state["collecting"] = True
        state["totalTime"] = request.duration
        start_time = time.time()
        buffer = []

        while time.time() - start_time < request.duration:
            try:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
            except SerialException as e:
                reset_state()
                logging.error(f"Serial exception: {e}")
                state["error"] = "Error reading from serial port"
                ser.close()
                return

            if line.startswith("CSI_DATA,"):
                buffer.append(line)
                state["linesCollected"] += 1

            if len(buffer) >= BUFFER_SIZE:
                try:
                    file.write("\n".join(buffer) + "\n")
                except Exception as e:
                    logging.error(f"Error writing to file: {e}")
                    reset_state()
                    state["error"] = "Error writing to file"
                    ser.close()
                    return
                finally:
                    buffer.clear()

            state["timeElapsed"] = time.time() - start_time

        if buffer:
            try:
                file.write("\n".join(buffer) + "\n")
            except Exception as e:
                logging.error(f"Error writing to file: {e}")
                reset_state()
                state["error"] = "Error writing to file"
                ser.close()
                return
            finally:
                buffer.clear()

        ser.close()

        logging.info(f"Data collection complete.")

        reset_state()


def reset_state() -> None:
    """
    Reset the global state.
    Returns: None
    """
    state["timeElapsed"] = 0.0
    state["totalTime"] = 0.0
    state["linesCollected"] = 0
    state["collecting"] = False
    state["error"] = ""
