# Atmospherix

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Atmospherix is a weather forecast application built with Streamlit, utilizing data from the OpenWeatherMap API and generating weather descriptions using the OpenAI API. It provides users with current weather updates, weekly forecasts, and hourly forecasts for specified cities.

## Features

- **Weather Forecast**: Users can get current weather updates for a specified city, including temperature, humidity, pressure, wind speed, and a weekly forecast.
  
- **Compare Weather**: Users can compare weather between two cities, viewing current weather updates and weekly forecasts side by side.
  
- **Hourly Forecast**: Users can view hourly weather forecasts for a specified city, displayed in a line chart format.

## Technologies Used

- **Streamlit**: Used for building the user interface and interactive elements of the application.
  
- **OpenWeatherMap API**: Provides weather data such as current conditions, forecasts, and historical data.
  
- **OpenAI API**: Generates weather descriptions based on provided weather data and city names.
  
- **Plotly**: Used for creating interactive plots and visualizations for displaying weather forecast data.

## Setup

To run Atmospherix locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Srish0218/Atmospherix.git
   ```

2. Install the required dependencies:

   ```bash
   cd atmospherix
   pip install -r requirements.txt
   ```

3. Obtain API keys:

   - **OpenWeatherMap API**: [Sign up](https://home.openweathermap.org/users/sign_up) for an account and obtain an API key.
   
   - **OpenAI API**: [Sign up](https://platform.openai.com/signup) for an account and obtain an API key.

4. Replace the placeholder API keys in the `app.py` file with your actual API keys.

5. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

6. Access the application in your web browser at `http://localhost:8501`.

## Usage

1. Select the desired feature from the dropdown menu: Weather Forecast, Compare Weather, or Hourly Forecast.

2. Enter the city name(s) and click the "Get Weather" or "Get Forecast" button to retrieve weather data.

3. View the current weather updates, weekly forecasts, or hourly forecasts based on your selection.

## Contributing

Contributions are welcome! If you'd like to contribute to Atmospherix, please follow these steps:

1. Fork the repository.

2. Create a new branch:

   ```bash
   git checkout -b feature/new-feature
   ```

3. Make your changes and commit them:

   ```bash
   git commit -am 'Add new feature'
   ```

4. Push to the branch:

   ```bash
   git push origin feature/new-feature
   ```

5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
