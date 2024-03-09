from flask import Blueprint, render_template, request
import requests

views = Blueprint('views', __name__)

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "9129a4796b56ca6071d6296a91927c81"

weather_conditions = []

@views.route('/')
def main_page():
    return render_template("base.html")

@views.route('/weather', methods=['POST'])
def weather_page():
    city_name = request.form.get('city')

    condition, temp = get_weather_data(city_name)

    return render_template('weather.html', city=city_name, condition=condition, temp=temp)

def get_weather_data(city_name):
    parameters = {
        "q": city_name,
        "appid": api_key,
        "cnt": 4,
        "units": "metric"
    }
    response = requests.get(url=OWM_Endpoint, params=parameters)

    weather_data = response.json()
    condition = weather_data["list"][0]["weather"][0]["description"]
    temp = weather_data["list"][0]["main"]["temp"]

    return condition, temp
