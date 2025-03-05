# CSI Data Collection React App

This is a React-based application for labelling and collecting data for a person located in a particular voxel.
The app allows users to select a voxel, set a duration, and start the data collection process.
The progress of the data collection is displayed using a progress bar.

## Features

- Select a voxel for data collection
- Set a custom duration for data collection
- Add a custom label to the data collection
- Display progress of data collection
- Show alerts for various statuses (e.g., errors, completion)

## Technologies Used

- React
- Axios
- React Bootstrap

## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>/frontend
    ```

2. Install the dependencies:

    ```bash
    npm install
    ```

3. Modify the .env file in the root directory and add the following:

    ```dotenv
    VITE_BASE_URL=http://your-server-ip:port
    ```

## Usage

1. Start the development server:

    ```bash
    npm run dev -- --host
    ```

    Adding the `--host` flag will allow the server to be accessible from other devices on the same network.

2. Open your browser and navigate to http://localhost:5173/.

3. Select a voxel, set the duration, and optionally add a custom label (e.g., "Resting", "Walking", "Center", etc.).

4. Click the "Submit" button to start the data collection process.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
