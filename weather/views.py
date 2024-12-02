import requests
from django.http import HttpResponse


def get_weather(request):
    """
    Получаем реальный IP-адрес пользователя, определяем город и погоду,
    возвращаем результат в виде красивой HTML-страницы.
    """
    # 1. Попытка получить реальный IP-адрес пользователя
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip:
        user_ip = user_ip.split(',')[0]  # Берем первый IP из списка
    else:
        user_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

    # Подставляем тестовый IP, если запрос идет с локального или внутреннего адреса
    if user_ip == '127.0.0.1' or user_ip.startswith('10.'):
        user_ip = '8.8.8.8'  # Тестовый публичный IP

    # 2. Определяем местоположение пользователя через API ipinfo.io
    location_response = requests.get(f"https://ipinfo.io/{user_ip}/json")
    if location_response.status_code != 200:
        return HttpResponse("Не удалось определить местоположение", status=500)

    location_data = location_response.json()
    city = location_data.get('city', 'Неизвестный город')  # Если город не найден, подставляем заглушку

    # 3. Получаем погоду через API OpenWeatherMap
    API_KEY = '2cd0264bc6306db8e7c70bc61ad22d73'  #  ключ OpenWeatherMap
    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": API_KEY, "units": "metric", "lang": "ru"}
    )

    if weather_response.status_code != 200:
        return HttpResponse("Не удалось получить данные о погоде", status=500)

    weather_data = weather_response.json()

    # Округляем температуру до целого числа
    temperature = round(weather_data['main']['temp'])

    # 4. Формируем HTML-страницу
    html_response = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Погода в вашем городе</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f8ff;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }}
            .weather-container {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 300px;
            }}
            .weather-container h1 {{
                font-size: 24px;
                margin-bottom: 10px;
            }}
            .weather-container p {{
                margin: 5px 0;
                font-size: 18px;
            }}
            .weather-container .temperature {{
                font-size: 36px;
                font-weight: bold;
                color: #007BFF;
            }}
        </style>
    </head>
    <body>
        <div class="weather-container">
            <h1>Погода в вашем городе</h1>
            <p><strong>Ваш IP-адрес:</strong> {user_ip}</p>
            <p><strong>Ваш город:</strong> {city}</p>
            <p class="temperature">{temperature}°C</p>
            <p><strong>Описание:</strong> {weather_data['weather'][0]['description']}</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_response)
