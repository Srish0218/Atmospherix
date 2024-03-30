import os
from datetime import datetime, timedelta
import plotly.express as px
import openai
import pandas as pd
import requests
import plotly.graph_objects as go
import streamlit as st

# Import API keys
# Set OpenAI API key
OPENAI_API_KEY = "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"
WEATHER_API_KEY = "646824f2b7b86caffec1d0b16ea77f79"


def get_weather_data(weather_key):
    """
    Function to fetch weather data from OpenWeatherMap API.

    Parameters:
        weather_key (str): API key for OpenWeatherMap.

    Returns:
        dict: Weather data in JSON format.
    """
    try:
        response = requests.get(weather_key)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("Error fetching weather data. Please check your internet connection.")
        return None
    except Exception as e:
        st.error("An unexpected error occurred while fetching weather data.")
        return None


def generate_description(data, city):
    """
    Function to generate weather description using OpenAI API.

    Parameters:
        data (dict): Weather data.
        city (str): Name of the city.

    Returns:
        str: Generated weather description.
    """
    try:
        temp = data['main']['temp'] - 273.15
        descrip = data['weather'][0]['description']
        prompt = f'The current weather in {city} is {descrip} with a temperature of {temp:.1f}°C'

        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=60
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)


def get_weekly(city, lat, lon):
    """
    Function to fetch weekly weather forecast data.

    Parameters:
        city (str): Name of the city.
        lat (float): Latitude of the city.
        lon (float): Longitude of the city.

    Returns:
        dict: Weekly weather forecast data in JSON format.
    """
    weather_key = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
    response = requests.get(weather_key)
    return response.json()


def display_weekly(data):
    """
    Function to display weekly weather forecast.

    Parameters:
        data (dict): Weekly weather forecast data.
    """
    try:
        st.markdown('---')
        st.write("### Weekly Weather Forecast")

        weekly_data = []

        for day in data['list']:
            date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')
            min_temp = day['main']['temp_min'] - 273.15
            max_temp = day['main']['temp_max'] - 273.15
            humidity = day['main']['humidity']
            pressure = day['main']['pressure']
            wind_speed = day['wind']['speed']

            weekly_data.append({'Date': date, 'Humidity': humidity,
                                'Pressure': pressure, 'Wind Speed': wind_speed,
                                'Min_Temp (°C)': min_temp, 'Max_Temp (°C)': max_temp})

        df = pd.DataFrame(weekly_data)
        # Group by Date and take the average of Min_Temp and Max_Temp
        df_agg = df.groupby('Date').agg({'Humidity': 'mean', 'Pressure': 'mean',
                                         'Wind Speed': 'mean',
                                         'Min_Temp (°C)': 'mean', 'Max_Temp (°C)': 'mean'}).reset_index()

        st.write(df_agg)

        # Plotly bar chart for weekly forecast
        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=df_agg['Date'], y=df_agg['Min_Temp (°C)'], name='Min Temperature (°C)', marker_color='blue'))
        fig.add_trace(
            go.Bar(x=df_agg['Date'], y=df_agg['Max_Temp (°C)'], name='Max Temperature (°C)', marker_color='red'))
        fig.add_trace(
            go.Scatter(x=df_agg['Date'], y=df_agg['Humidity'], mode='lines+markers', name='Humidity', yaxis='y2'))
        fig.add_trace(
            go.Scatter(x=df_agg['Date'], y=df_agg['Pressure'], mode='lines+markers', name='Pressure', yaxis='y3'))
        fig.add_trace(
            go.Scatter(x=df_agg['Date'], y=df_agg['Wind Speed'], mode='lines+markers', name='Wind Speed', yaxis='y4'))

        fig.update_layout(title='Weekly Weather Forecast',
                          xaxis_title='Date',
                          yaxis_title='Temperature (°C)',
                          barmode='group',
                          yaxis2=dict(title='Humidity', overlaying='y', side='right'),
                          yaxis3=dict(title='Pressure', overlaying='y', side='right', anchor='free', position=0.9),
                          yaxis4=dict(title='Wind Speed', overlaying='y', side='right', anchor='free', position=0.95))

        st.plotly_chart(fig)

    except Exception as e:
        st.error("Error in displaying weekly forecast: " + str(e))


def compare_weather():
    city1 = st.text_input("Enter City 1: ", "Ludhiana")
    city2 = st.text_input("Enter City 2: ", "Kharar")

    openai_key = "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"
    weather_key1 = f"https://api.openweathermap.org/data/2.5/weather?q={city1}&appid={WEATHER_API_KEY}"
    weather_key2 = f"https://api.openweathermap.org/data/2.5/weather?q={city2}&appid={WEATHER_API_KEY}"

    submit = st.button("Get Weather")

    if submit:
        # Fetch weather data for city 1
        with st.spinner(f"Fetching weather data for {city1}..."):
            weather_data1 = get_weather_data(weather_key1)

        # Fetch weather data for city 2
        with st.spinner(f"Fetching weather data for {city2}..."):
            weather_data2 = get_weather_data(weather_key2)

        if weather_data1.get('cod') != 404 and weather_data2.get('cod') != 404:

            col3, col4 = st.columns(2)
            with col3:
                st.title(f"Weather in {city1}")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Temperature 🌡️", f"{weather_data1['main']['temp'] - 273.15:.2f} °C")
                    st.metric("Humidity  💧️", f"{weather_data1['main']['humidity']}%")
                with c2:
                    st.metric("Pressure 🗜", f"{weather_data1['main']['pressure']} hPa")
                    st.metric("Wind Speed 🌬️", f"{weather_data1['wind']['speed']}m/s")

                lat = weather_data1['coord']['lat']
                lon = weather_data1['coord']['lon']

                weather_desc = generate_description(weather_data1, city1)
                st.write(weather_desc)

                forecast_data = get_weekly(city1, lat, lon)

                if forecast_data.get("cod") != '404':
                    display_weekly(forecast_data)
                else:
                    st.error("Error fetching weekly forecast data!", icon="🌩️")

            with col4:
                st.title(f"Weather in {city2}")
                c3, c4 = st.columns(2)
                with c3:
                    st.metric("Temperature 🌡️", f"{weather_data2['main']['temp'] - 273.15:.2f} °C")
                    st.metric("Humidity  💧️", f"{weather_data2['main']['humidity']}%")
                with c4:
                    st.metric("Pressure 🗜", f"{weather_data2['main']['pressure']} hPa")
                    st.metric("Wind Speed 🌬️", f"{weather_data2['wind']['speed']}m/s")

                lat = weather_data2['coord']['lat']
                lon = weather_data2['coord']['lon']

                weather_desc = generate_description(weather_data2, city2)
                st.write(weather_desc)

                forecast_data = get_weekly(city2, lat, lon)

                if forecast_data.get("cod") != '404':
                    display_weekly(forecast_data)
                else:
                    st.error("Error fetching weekly forecast data!", icon="🌩️")





        else:
            st.error("One or both cities not found or error occurred!!", icon="🌩️")


def weather_forecast():
    """
    Function to display current weather forecast.
    """
    city = st.text_input("Enter City: ", "Ludhiana")

    weather_key = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"

    submit = st.button("Get Weather")

    if submit:
        st.title(f"Weather Updates for {city} is: ")
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(weather_key)

            if weather_data.get('cod') != 404:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature 🌡️", f"{weather_data['main']['temp'] - 273.15:.2f} °C")
                    st.metric("Humidity  💧️", f"{weather_data['main']['humidity']}%")
                with col2:
                    st.metric("Pressure 🗜", f"{weather_data['main']['pressure']} hPa")
                    st.metric("Wind Speed 🌬️", f"{weather_data['wind']['speed']}m/s")

                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']

                weather_desc = generate_description(weather_data, city)
                st.write(weather_desc)

                forecast_data = get_weekly(city, lat, lon)

                if forecast_data.get("cod") != '404':
                    display_weekly(forecast_data)
                else:
                    st.error("Error fetching weekly forecast data!", icon="🌩️")

            else:
                st.error("City not found or error occurred!!", icon="🌩️")


def hourly_forecast():
    """
    Function to display hourly weather forecast with a line chart and date navigation feature.
    """
    st.title("Hourly Weather Forecast")
    city = st.text_input("Enter City: ", "Ludhiana")

    weather_key = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}"

    submit = st.button("Get Forecast")

    if submit:
        st.spinner("Fetching forecast data...")
        forecast_data = get_weather_data(weather_key)

        if forecast_data and forecast_data.get('cod') == '200':
            columns = ['dt', 'main.temp', 'main.feels_like', 'weather']
            hourly_forecast_df = pd.json_normalize(forecast_data['list'])
            hourly_forecast_df = hourly_forecast_df[columns]

            hourly_forecast_df['Description'] = hourly_forecast_df['weather'].apply(lambda x: x[0]['description'])

            hourly_forecast_df.drop(columns=['weather'], inplace=True)

            ist_time = []
            for ts in hourly_forecast_df['dt']:
                utc_time = datetime.utcfromtimestamp(ts)
                ist_time.append(utc_time + timedelta(hours=5, minutes=30))

            hourly_forecast_df['Timestamp (IST)'] = ist_time

            hourly_forecast_df['Date'] = hourly_forecast_df['Timestamp (IST)'].dt.date
            hourly_forecast_df['Time'] = hourly_forecast_df['Timestamp (IST)'].dt.time

            # Convert temperature from Kelvin to Celsius
            hourly_forecast_df['Temperature (°C)'] = hourly_forecast_df['main.temp'] - 273.15
            hourly_forecast_df['Feels Like (°C)'] = hourly_forecast_df['main.feels_like'] - 273.15

            hourly_forecast_df.drop(columns=['main.temp', 'main.feels_like', 'Timestamp (IST)', 'dt'], inplace=True)

            hourly_forecast_df.rename(columns={'Description': 'Description'}, inplace=True)

            hourly_forecast_df_final = hourly_forecast_df.loc[:,
                                       ['Date', 'Time', 'Temperature (°C)', 'Feels Like (°C)', 'Description']]

            st.write(hourly_forecast_df_final)

            # Line chart
            fig = px.line(hourly_forecast_df_final, x='Time', y='Temperature (°C)', color='Date',
                          title=f'Hourly Temperature Forecast for {city}',
                          labels={'Temperature (°C)': 'Temperature (°C)', 'Time': 'Time', 'Date': 'Date'})

            st.plotly_chart(fig, use_container_width=True)


        else:
            st.error("Forecast data not available or error occurred!!", icon="🌩️")


def main():
    """
    Main function to run the application.
    """
    st.title("Atmospherix")

    feature = st.selectbox("Select Feature", (
        "Weather Forecast", "Compare Weather", "Hourly Forecast"))

    if feature == "Weather Forecast":
        weather_forecast()
    elif feature == "Compare Weather":
        compare_weather()
    elif feature == "Hourly Forecast":
        hourly_forecast()


if __name__ == "__main__":
    main()
