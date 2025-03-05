# CSI Data Collection and Labelling

This project consists of three main components:

- [React-based web application](./frontend/README.md) for sending data collection requests to a FastAPI service and displaying the progress of the data collection process.
- [FastAPI-based service](./backend/README.md) for collecting data from an ESP32 device connected to a serial port and storing it in CSV files.
- [ESP32 firmware](https://github.com/nipunchamikara/csi-data-collection-firmware) for collecting Channel State Information (CSI) data from Wi-Fi packets and logging it to the serial port.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
