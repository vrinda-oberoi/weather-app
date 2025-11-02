from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# ✅ PUT YOUR API KEY HERE - Get from https://openweathermap.org/appid
API_KEY = "ff844bb695fcbedaec0c6e1cfb29d23d"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

@app.route('/')
def home():
    return render_template('weather.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        data = request.get_json()
        city = data.get('city', 'Bengaluru')
        units = data.get('units', 'metric')
        
        if API_KEY == "YOUR_API_KEY_HERE":
            return jsonify({'error': 'Please setup your API key first'}), 400
        
        # Get current weather
        params = {
            'q': city,
            'appid': API_KEY,
            'units': units
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            current_data = response.json()
            
            # Get forecast
            forecast_response = requests.get(FORECAST_URL, params=params, timeout=10)
            forecast_data = None
            
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
            
            return jsonify({
                'success': True,
                'current': current_data,
                'forecast': forecast_data
            })
        elif response.status_code == 404:
            return jsonify({'error': 'City not found'}), 404
        elif response.status_code == 401:
            return jsonify({'error': 'Invalid API key'}), 401
        else:
            return jsonify({'error': f'Error: {response.status_code}'}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌤️  MODERN WEATHER APP STARTING...")
    print("="*60)
    print("📍 Open browser: http://localhost:5000")
    print("🔑 Add API key from: https://openweathermap.org/appid")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)