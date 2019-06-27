from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    key = 'd943582f82892a326fb685f3f71bf5a5'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + key

    if request.method == 'POST':
        # Получение информации из формы
        form = CityForm(request.POST)
        # Сохранение информации в базу данных
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon']
        }
        all_cities.append(city_info)

    context = {
        'all_info': all_cities[::-1],
        'form': form
    }

    return render(request, 'weather/index.html', context)
