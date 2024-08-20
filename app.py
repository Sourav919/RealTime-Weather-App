from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

def scrape_weather(city, country):
    url = f"https://www.google.com/search?q=weather+{city}+{country}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = bs(response.content, "html.parser")
    
    try:
        temperature = soup.find("span", {"id": "wob_tm"}).text
        weather_condition = soup.find("span", {"id": "wob_dc"}).text
        humidity = soup.find("span", {"id": "wob_hm"}).text
        wind_speed = soup.find("span", {"id": "wob_ws"}).text
        precip_prob = soup.find("span", {"id": "wob_pp"}).text
        
        return {
            "temperature": temperature + "°F",
            "weather_condition": weather_condition,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "precip_prob": precip_prob
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        country = request.form.get("country")
        weather_data = scrape_weather(city, country)
    
    return render_template("index.html", weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
