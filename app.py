from flask import Flask, redirect, url_for, render_template, request
import requests

app = Flask(__name__)

# Get your OpenWeather API key from environment variables
OPENAI_API_KEY = "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"
WEATHER_API_KEY = "646824f2b7b86caffec1d0b16ea77f79"


# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather_forecast', methods=['GET', 'POST'])
def weather_forecast():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather_data(city)
        if weather_data:
            return render_template('weather_forecast.html', weather_data=weather_data)
        else:
            return render_template('error.html')
    return render_template('weather_forecast_form.html')

@app.route('/compare_weather', methods=['GET', 'POST'])
def compare_weather():
    if request.method == 'POST':
        city1 = request.form['city1']
        city2 = request.form['city2']
        weather_data1 = get_weather_data(city1)
        weather_data2 = get_weather_data(city2)
        if weather_data1 and weather_data2:
            return render_template('compare_weather.html', city1=city1, city2=city2, weather_data1=weather_data1, weather_data2=weather_data2)
        else:
            return render_template('error.html')
    return render_template('compare_weather_form.html')

@app.route('/hourly_forecast', methods=['GET', 'POST'])
def hourly_forecast():
    if request.method == 'POST':
        city = request.form['city']
        forecast_data = get_hourly_forecast(city)
        if forecast_data:
            return render_template('hourly_forecast.html', city=city, forecast_data=forecast_data)
        else:
            return render_template('error.html')
    return render_template('hourly_forecast_form.html')

# Helper functions
def get_weather_data(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': city.capitalize(),
                'temperature': round(data['main']['temp'] - 273.15, 2),  # Convert Kelvin to Celsius
                'description': data['weather'][0]['description'].capitalize(),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed']
            }
            return weather_data
        else:
            return None
    except Exception as e:
        print(e)
        return None

def get_hourly_forecast(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast_data = []
            for item in data['list']:
                forecast_data.append({
                    'date': item['dt_txt'].split()[0],
                    'time': item['dt_txt'].split()[1],
                    'temperature': round(item['main']['temp'] - 273.15, 2),  # Convert Kelvin to Celsius
                    'description': item['weather'][0]['description']
                })
            return forecast_data
        else:
            return None
    except Exception as e:
        print(e)
        return None

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
