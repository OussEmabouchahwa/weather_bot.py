import os
import requests
from google import genai

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
CITY, LAT, LON = "Tunis", 36.8065, 10.1815

# Taqs
url = (
    f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
    "&daily=temperature_2m_max,temperature_2m_min,"
    "precipitation_probability_max,wind_speed_10m_max"
    "&timezone=auto&forecast_days=1"
)
d = requests.get(url, timeout=30).json()["daily"]
tmax, tmin = d["temperature_2m_max"][0], d["temperature_2m_min"][0]
rain, wind = d["precipitation_probability_max"][0], d["wind_speed_10m_max"][0]

header = (
    f"🌤️ Ta9s {CITY} lyoum\n"
    f"🌡️ {tmin:.0f}° → {tmax:.0f}°\n"
    f"🌧️ Chta: {rain}%\n"
    f"💨 Rih: {wind} km/h\n\n"
)

# Models: jarreb wa7ed wara wa7ed. Beddelhom ken Google beddel el asemi.
MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.8-flash",
    "gemini-3.1-flash-lite",
]

def ai_advice():
    client = genai.Client()  # yeqra GEMINI_API_KEY
    prompt = (
        f"Ekteb b darija tounsia (3 jomal maximum) nasa7 mo7aded 3la chnoua "
        f"nelbes lyoum fi {CITY} (khfif wala thkil, jacket, mdhalla...). "
        f"El 7ara mel {tmin:.0f}° l {tmax:.0f}°, ihtimal el chta {rain}%, "
        f"rih {wind} km/h."
    )
    last_err = None
    for m in MODELS:
        try:
            text = client.models.generate_content(model=m, contents=prompt).text
            print("Used model:", m)
            return text.strip()
        except Exception as e:
            print(f"{m} failed: {e}")
            last_err = e
    raise last_err

def basic_advice():
    if tmax >= 32:
        tip = "🥵 Sakhoun barcha: lbes khfif w echrab ma barcha."
    elif tmax >= 24:
        tip = "😎 Jaw behi: t-shirt wala khfif."
    elif tmax >= 16:
        tip = "🧥 Mo3tadel: 7ot jacket khfifa."
    else:
        tip = "🥶 Bard: lbes thkil."
    if rain >= 50:
        tip += "\n☔ Khoudh mdhalla."
    return tip

try:
    advice = ai_advice()
except Exception as e:
    print("All AI models failed:", e)
    advice = basic_advice()

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": header + advice},
    timeout=30,
)
