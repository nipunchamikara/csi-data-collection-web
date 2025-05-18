import logging
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from serial.serialutil import SerialException

from utils import HEADER

load_dotenv()

BUFFER_SIZE = int(os.getenv("BUFFER_SIZE"))

collect_state = {
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
    folder_name = "data/" + request.experiment
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
        collect_state["collecting"] = True
        collect_state["totalTime"] = request.duration
        start_time = time.time()
        buffer = []

        while time.time() - start_time < request.duration:
            try:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
            except SerialException as e:
                reset_state()
                logging.error(f"Serial exception: {e}")
                collect_state["error"] = "Error reading from serial port"
                return

            if line.startswith("CSI_DATA,"):
                buffer.append(line)
                collect_state["linesCollected"] += 1

            if len(buffer) >= BUFFER_SIZE:
                try:
                    file.write("\n".join(buffer) + "\n")
                except Exception as e:
                    logging.error(f"Error writing to file: {e}")
                    reset_state()
                    collect_state["error"] = "Error writing to file"
                    return
                finally:
                    buffer.clear()

            collect_state["timeElapsed"] = time.time() - start_time

        if buffer:
            try:
                file.write("\n".join(buffer) + "\n")
            except Exception as e:
                logging.error(f"Error writing to file: {e}")
                reset_state()
                collect_state["error"] = "Error writing to file"
                return
            finally:
                buffer.clear()

        logging.info(f"Data collection complete.")

        reset_state()


def reset_state() -> None:
    """
    Reset the global state.
    Returns: None
    """
    collect_state["timeElapsed"] = 0.0
    collect_state["totalTime"] = 0.0
    collect_state["linesCollected"] = 0
    collect_state["collecting"] = False
    collect_state["error"] = ""
