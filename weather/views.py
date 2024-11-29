import requests  # Для отправки HTTP-запросов
from django.http import JsonResponse

def get_weather(request):
    """
    Получаем IP-адрес, город, погоду и возвращаем результат с описаниями.
    """
    # 1. Получаем IP-адрес пользователя
    user_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    if user_ip == '127.0.0.1':  # Если локальный IP, используем тестовый
        user_ip = '8.8.8.8'

    # 2. Определяем местоположение пользователя через API ipinfo.io
    location_response = requests.get(f"https://ipinfo.io/{user_ip}/json")
    if location_response.status_code != 200:
        return JsonResponse({"error": "Не удалось определить местоположение"}, status=500)

    location_data = location_response.json()
    city = location_data.get('city', 'Москва')  # Если город не найден, используем "Москва"

    # 3. Получаем погоду через API OpenWeatherMap
    API_KEY = '2cd0264bc6306db8e7c70bc61ad22d73'  # мой ключ OpenWeatherMap
    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": API_KEY, "units": "metric", "lang": "ru"}
    )

    if weather_response.status_code != 200:
        return JsonResponse({"error": "Не удалось получить данные о погоде"}, status=500)

    weather_data = weather_response.json()

    # 4. Формируем результат с подписями
    result = {
        "Ваш IP-адрес": user_ip,
        "Ваш город": city,
        "Температура (°C)": weather_data['main']['temp'],  # Температура
        "Описание погоды": weather_data['weather'][0]['description'],  # Описание погоды
    }

    return JsonResponse(result)
