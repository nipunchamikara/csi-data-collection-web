# ESP32 CSI Data Collection Project using FastAPI

This project is a FastAPI-based service for collecting data from an ESP32 device connected to a serial port and storing
it in CSV files. The service provides endpoints to start data collection and check the status of the collection process.

## Features

- Start data collection from a serial port
- Store collected data in CSV files
- Check the status of the data collection process

## Requirements

- Python 3.8+
- FastAPI
- Pydantic
- PySerial
- Python-dotenv

## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>/backend
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Modify the .env file in the project root and set the following environment variables:

    ```dotenv
    SERIAL_PORT=<your_serial_port>
    BAUD_RATE=<your_baud_rate>
    BUFFER_SIZE=<your_buffer_size>
    ```

## Usage

Start the FastAPI server:

```bash
uvicorn routes:router --reload --host=0.0.0.0
```

The host parameter is set to `0.0.0.0` to allow connections from other devices on the same network.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
