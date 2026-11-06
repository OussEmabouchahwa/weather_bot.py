import os
import requests
from google import genai

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
CITY, LAT, LON = "Tunis", 36.8065, 10.1815  # beddel l blasetek

# 1. Taqs
url = (
    f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
    "&daily=temperature_2m_max,temperature_2m_min,"
    "precipitation_probability_max,wind_speed_10m_max"
    "&timezone=auto&forecast_days=1"
)
daily = requests.get(url, timeout=30).json()["daily"]
data = {k: v[0] for k, v in daily.items()}

# 2. Gemini yekteb el molakhas
client = genai.Client()  # yeqra GEMINI_API_KEY men environment
prompt = (
    f"Ekteb b darija tounsia molakhas9sir lel ta9s lyoum fi {CITY} "
    f"m3a nasa7 3la kifech nelbes. El data: {data}"
)
text = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
).text

# 3. Ab3ath l Telegram
requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": f"🌤️ {CITY}\n\n{text}"},
    timeout=30,
)