from django.shortcuts import render
from django.views import View
from weather.forms import WeatherByCityForm
from django.conf import settings

# Import json data to load JSON Data to Python Dictonary
import json

# To make request to API
import urllib.request

# Create your views here.
class IndexView(View):
    template_name = "weather/index.html"
    
    def get(self, request):
        form = WeatherByCityForm()
        context = {
            'form':form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        get_city = request.POST["city"]
        city = get_city.replace(" ","%20")
        print(city)
        form = WeatherByCityForm()

        try:
            # Get JSON data from API
            api_url = str("https://api.openweathermap.org/data/2.5/weather?q="+ city +"&appid="+ settings.WEATHER_API_KEY)
            source_data = urllib.request.urlopen(api_url).read()
            
            # Convert JSON data to a Python Dictonary
            list_of_data = json.loads(source_data)

            # Convert Kelvin to Celsius
            temperature_c = round(float(list_of_data["main"]["temp"]) - 273.15, 2)
            feels_like = round(float(list_of_data["main"]["feels_like"]) - 273.15, 2)

            # Get data from list_of_data
            weather_data = {
                "temperature":str(temperature_c) + " °C",
                "feels_like":str(feels_like) + " °C",
                "city_id":str(list_of_data["id"]),
                "city_name":str(list_of_data["name"]),
                "country_code":str(list_of_data["sys"]["country"]),
                "latitude":str(list_of_data["coord"]["lat"]),
                "longitude":str(list_of_data["coord"]["lon"]),
                "pressure":str(list_of_data["main"]["pressure"]),
                "humidity":str(list_of_data["main"]["humidity"]),
                "wind_speed":str(list_of_data["wind"]["speed"]),
                "description":str(list_of_data["weather"][0]["description"]),
                "icon":str(list_of_data["weather"][0]["icon"])
            }

            context = {
                "form":form,
                "weather_data":weather_data,
                "weather_api_key":settings.WEATHER_API_KEY    
            }

        except:
            print("City not found")

            weather_data = {
                "error":get_city + " city not found. Please enter a valid city name."
            }

            context = {
                "form":form,
                "weather_data":weather_data
            }

        return render(request, self.template_name, context)