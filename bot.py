import logging
import asyncio
import requests
from telegram import Bot
from telegram.error import TelegramError

# --- КОНСТАНТИ ---
# 1. Замініть на свій токен
TELEGRAM_BOT_TOKEN = "7669729694:AAGEqOJUevQW3ZfDZzCswsfO791bD0RHwHk"
# 2. Замініть на свій API-ключ OpenWeatherMap
OPENWEATHERMAP_API_KEY = "c44a8a089d4f828cd6c46ad0b8a1747f"
# 3. Замініть на ID чату, куди надсилати погоду (це може бути ваш особистий ID)
TARGET_CHAT_ID = "1060933896"
# Місто для запиту
CITY = "Kyiv,UA"
# Інтервал у секундах (30 хвилин = 1800 секунд)
INTERVAL_SECONDS = 10

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- ФУНКЦІЇ ---

def get_weather_data(city: str) -> str:
    """Отримує дані про погоду з OpenWeatherMap і форматує їх."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",  # Температура у Цельсіях
        "lang": "ua"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Викликає HTTPError для поганих відповідей
        data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Помилка при запиті до API погоди: {e}")
        return "Не вдалося отримати дані про погоду."

    # Обробка даних
    main = data.get('main', {})
    weather = data.get('weather', [{}])[0]
    wind = data.get('wind', {})

    # Конвертація
    temp = main.get('temp')
    feels_like = main.get('feels_like')
    description = weather.get('description', 'без опису').capitalize()
    wind_speed = wind.get('speed')
    humidity = main.get('humidity')

    # Форматування повідомлення