import decimal
import unittest
from unittest.mock import MagicMock, patch, Mock

from weather.services.open_weather_api_service import OpenWeatherService
from weather.schemas import LocationDTO, WeatherDTO


class LocationResponseMock(MagicMock):
    status_code = 200

    @staticmethod
    def json():
        return [
            {
                'name': 'Весёлая Жизнь',
                'country': 'RU',
                'lat': 46.224373,
                'lon': 39.830135
            },
        ]


class WeatherResponseMock(MagicMock):
    status_code = 200

    @staticmethod
    def json():
        return {
            'main': {
                'temp': 12,
                'feels_like': 10,
                'humidity': 60
            },
            'weather': [
                {
                    'description': 'Солнышко светит, птички поют, ветерок веет',
                    'icon': '01d'
                }
            ],
            'wind': {
                'speed': 4,
            }

        }


class WeatherServiceTest(unittest.TestCase):
    @patch('requests.get')
    def test_get_location_by_name(self, mock_get):
        mock_get.return_value = LocationResponseMock()

        expected_res = LocationDTO(
            name='Весёлая Жизнь',
            country='Россия',
            latitude=decimal.Decimal('46.224373'),
            longitude=decimal.Decimal('39.830135')
        )

        self.assertIn(expected_res, OpenWeatherService.get_locations_by_name('Весёлая Жизнь'))  # sdfsdf

    @patch('requests.get')
    def test_get_weather_by_coords(self, mock_get):
        mock_get.return_value = WeatherResponseMock()

        expected_res = WeatherDTO(
            temperature=decimal.Decimal('12'),
            temperature_feels_like=decimal.Decimal('10'),
            weather_desc='Солнышко светит, птички поют, ветерок веет',
            humidity=60,
            wind_speed=4,
            icon_id='01d'
        )

        self.assertEqual(expected_res, OpenWeatherService.get_weather_by_coords(46.224373, 39.830135))  # sdf

    @patch('requests.get')
    def test_get_location_by_name_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        mock_get.return_value = mock_response

        self.assertListEqual(OpenWeatherService.get_locations_by_name(''), [])  # sdfsdf


