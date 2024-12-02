import logging
from decimal import Decimal

import requests
import requests_cache

from weather.services.iso_country_codes import countries
from weather.services.exceptions import (
    APIConnectionError, RemoteAPIAccessError, RequestError, UnknownError, RequestLimitError, APIKeyError
)
from weather.schemas import LocationDTO, WeatherDTO
from weather_viewer.settings import WEATHER_API_KEY


api_logger = logging.getLogger('weather_viewer.api')


class OpenWeatherService:
    _EXCEPTIONS = {
        '400': RequestError,
        '401': APIKeyError,
        '404': RequestError,
        '429': RequestLimitError,
        '500': UnknownError
    }

    _OPEN_WEATHER_API_ENDPOINTS = {
        'get_location_by_name': 'https://ru.api.openweathermap.org/geo/1.0/direct',
        'get_weather_by_coords': 'https://ru.api.openweathermap.org/data/2.5/weather'
    }

    API_KEY = WEATHER_API_KEY

    @classmethod
    def get_locations_by_name(cls, name: str) -> list[LocationDTO]:
        docs_url: str = 'https://openweathermap.org/api/geocoding-api'

        api_logger.debug(f'Fetch locations by name: {name}')

        response = cls._execute_request(
            request_url=cls._OPEN_WEATHER_API_ENDPOINTS['get_location_by_name'],
            params={
                'q': name,
                'limit': 5,
                'appid': cls.API_KEY,
            }
        )

        data = response.json()

        if response.status_code == 200:
            api_logger.debug(f'Location by name fetched successfully for {name}')
            return [cls._location_response_to_dto(location) for location in data]
        else:
            api_logger.error(f'OpenWeather API Error upon request location by name {name}: '
                             f'{response.status_code} {data}')
            raise cls._EXCEPTIONS.get(str(data['cod']), UnknownError)(data['message'], response.url, docs_url)

    @classmethod
    def get_weather_by_coords(cls, lat: float | Decimal, lon: float | Decimal):
        docs_url: str = 'https://openweathermap.org/current#one'

        api_logger.debug(f'Fetch weather by coords: (latitude: {lat}, longitude: {lon})')

        response = cls._execute_request(
            request_url=cls._OPEN_WEATHER_API_ENDPOINTS['get_weather_by_coords'],
            params={
                'lat': lat,
                'lon': lon,
                'appid': cls.API_KEY,
                'units': 'metric',
                'lang': 'ru'
            }
        )

        data = response.json()

        if response.status_code == 200:
            api_logger.debug(f'Fetch weather by coords successfully for (latitude: {lat}, longitude: {lon})')
            if data:
                return cls._weather_response_to_dto(data)
        else:
            api_logger.error(f'OpenWeather API Error upon request weather by coordinates '
                             f'(latitude: {lat}, longitude: {lon}): {response.status_code} {data}')
            raise cls._EXCEPTIONS.get(str(data['cod']), UnknownError)(data['message'], response.url, docs_url)

    @classmethod
    def _execute_request(cls, request_url: str, params: dict) -> requests.Response:
        requests_cache.install_cache(
            cache_name='weather/services/weather_cache',
            backend='sqlite',
            expire_after=900  # Время жизни кеша в секундах (15 минут)
        )

        try:
            response = requests.get(request_url, params=params, timeout=4)
            return response
        except OSError as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                api_logger.error(f'Connection Error: {e}')
                raise APIConnectionError()
            elif isinstance(e, requests.exceptions.ReadTimeout):
                api_logger.error(f'ReadTimeout Error: {e}')
                raise RemoteAPIAccessError()
            else:
                api_logger.error(f'Unknown Error: {e}')
                raise UnknownError(error=str(e))

    @staticmethod
    def _location_response_to_dto(location: dict) -> LocationDTO:
        try:
            name = location['local_names']['ru']
        except KeyError:
            name = location['name']

        try:
            return LocationDTO(
                name=name,
                country=countries[location['country']],
                latitude=Decimal(str(location['lat'])).quantize(Decimal('1.000000')),
                longitude=Decimal(str(location['lon'])).quantize(Decimal('1.000000'))
            )
        except KeyError as e:
            print('Не локация..')

    @classmethod
    def _weather_response_to_dto(cls, weather: dict) -> WeatherDTO:
        try:
            return WeatherDTO(
                temperature=Decimal(weather['main']['temp']).quantize(Decimal('1')),
                temperature_feels_like=Decimal(weather['main']['feels_like']).quantize(Decimal('1')),
                weather_desc=weather['weather'][0]['description'].capitalize(),
                humidity=weather['main']['humidity'],
                wind_speed=weather['wind']['speed'],
                icon_id=weather['weather'][0]['icon']
            )
        except KeyError as e:
            print('Не погода..')

    @staticmethod
    def _get_icon_url(icon_id: str) -> str:
        return f"https://openweathermap.org/img/wn/{icon_id}@4x.png"
