import aiohttp
import json
from bs4 import BeautifulSoup
from datetime import datetime

class Tools:
    def __init__(self):
        self.weather_api_key = None

    async def search_web(self, query: str) -> str:
        try:
            url = f"https://html.duckduckgo.com/html/?q={query}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    results = soup.find_all('a', class_='result__a')[:3]
                    if results:
                        return "\n".join([r.text for r in results])
                    return "Ничего не найдено."
        except:
            return "Ошибка поиска."

    async def get_weather(self, city: str) -> str:
        if not self.weather_api_key:
            return "Погода: установи API ключ OpenWeatherMap в .env как WEATHER_API_KEY"
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric&lang=ru"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
                    if data.get("main"):
                        temp = data["main"]["temp"]
                        desc = data["weather"][0]["description"]
                        return f"Погода в {city}: {temp}°C, {desc}"
                    return "Город не найден."
        except:
            return "Ошибка получения погоды."

    async def get_exchange_rate(self, currency: str = "USD") -> str:
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
                    rates = data.get("rates", {})
                    rate = rates.get(currency.upper())
                    if rate:
                        return f"Курс {currency.upper()}: {rate} RUB (примерно)"
                    return "Валюта не найдена."
        except Exception as e:
            return f"Ошибка курса: {str(e)}"

    async def calculate(self, expression: str) -> str:
        try:
            allowed = set("0123456789+-*/() .")
            if all(c in allowed for c in expression):
                result = eval(expression)
                return f"{expression} = {result}"
            return "Некорректное выражение."
        except:
            return "Ошибка вычисления."

    async def get_time(self) -> str:
        now = datetime.now()
        return f"Сейчас {now.strftime('%H:%M:%S')}, {now.strftime('%d.%m.%Y')}"