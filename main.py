import requests

API_KEY = '37a5e79b03aa263712f652c011fe6282'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Replace 'city_name' with the city you are interested in
city_name = 'Berlin'
complete_url = f"{BASE_URL}appid={API_KEY}&q={city_name}"

response = requests.get(complete_url)
data = response.json()

if data["cod"] != "404":
    main = data["main"]
    kelvin_temp = main["temp"]
    celsius_temp = kelvin_temp - 273.15
    pressure = main["pressure"]
    humidity = main["humidity"]
    weather_description = data["weather"][0]["description"]

    print(f"Temperature: {celsius_temp:.2f}°C")
    print(f"Atmospheric pressure: {pressure} hPa")
    print(f"Humidity: {humidity}%")
    print(f"Description: {weather_description}")
else:
    print("City not found")
