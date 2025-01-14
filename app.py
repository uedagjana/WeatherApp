from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API Key
API_KEY = "e14deac269557548179b845f0b33d7da"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/onecall"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.json.get("city")
    lang = request.json.get("lang", "sq")

    if not city:
        return jsonify({"error": "Ju lutem, jepni një emër qyteti."}), 400

    # Marrim të dhënat për qytetin nga OpenWeatherMap API
    response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric", "lang": lang})

    if response.status_code != 200:
        return jsonify({"error": "Qyteti nuk u gjet. Ju lutem provoni përsëri."}), 404

    city_data = response.json()
    lat = city_data['coord']['lat']
    lon = city_data['coord']['lon']

    # Marrim parashikimin për 7 ditët e ardhshme
    forecast_response = requests.get(FORECAST_URL, params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric",
                                                           "exclude": "current,minutely,hourly", "lang": lang})

    if forecast_response.status_code != 200:
        return jsonify({"error": "Nuk mund të merrni të dhëna të parashikimit."}), 500

    forecast_data = forecast_response.json()

    return jsonify({
        "city": city_data['name'],
        "weather": city_data['weather'][0]['description'],
        "temperature": city_data['main']['temp'],
        "feels_like": city_data['main']['feels_like'],
        "wind_speed": city_data['wind']['speed'],
        "humidity": city_data['main']['humidity'],
        "forecast": forecast_data['daily'],
    })

if __name__ == "__main__":
    app.run(debug=True)