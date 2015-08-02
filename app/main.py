import requests

def main():
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Lewiston,ny&units=imperial")
        data = r.json()

        print(data)
        print(data["weather"])

        print("Current Temperature: " + str(data["main"]["temp"]))
        print("Max Temperature: " + str(data["main"]["temp_max"]))
        print("Min Temperature: " + str(data["main"]["temp_min"]))
        print("Speed: " + str(data["wind"]["speed"]) + " direction: " + str(data["wind"]["deg"]))
        
        for weather_data in data["weather"]:
                print(str(weather_data["main"]) + " " + str(weather_data["id"]))


main()
