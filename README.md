﻿# Atmospherix

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![View Demo](https://img.shields.io/badge/View-Demo-blueviolet)]()

Atmospherix is a web application that provides weather forecast information for cities around the world. Users can access current weather conditions, hourly forecasts, and compare weather between two cities.

## Features

- **Weather Forecast**: Get detailed weather forecasts for any city.
- **Hourly Forecast**: View hourly weather forecasts for a specific city.
- **Compare Weather**: Compare weather conditions between two cities.
- **Responsive Design**: The web app is optimized for various screen sizes, including mobile devices.

## Technologies Used

- **Frontend**: HTML, CSS
- **Backend**: Python, Flask
- **APIs**: OpenWeatherMap API
- **Icons**: Ionicons

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Srish0218/atmospherix.git
    ```

2. Navigate to the project directory:

    ```bash
    cd atmospherix
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your OpenWeatherMap API key:
   
    - Sign up for a free account on [OpenWeatherMap](https://openweathermap.org/) and obtain an API key.
    - Create a `.env` file in the root directory of the project.
    - Add your API key to the `.env` file:

        ```plaintext
        API_KEY=your_api_key_here
        ```

5. Run the application:

    ```bash
    python app.py
    ```

6. Access the application in your web browser at `http://localhost:5000`.

## Usage

- Navigate to the desired section using the navigation links provided.
- Enter the name of the city you want to get weather information for.
- Submit the form to view the weather forecast.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or suggestions.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/).
- Icons provided by [Ionicons](https://ionicons.com/).

---
