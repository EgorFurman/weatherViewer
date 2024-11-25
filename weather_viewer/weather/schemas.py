from dataclasses import dataclass
from decimal import Decimal
from typing import Union


@dataclass
class WeatherDTO:
    temperature: Decimal
    temperature_feels_like: Decimal
    weather_desc: str
    humidity: float
    wind_speed: float
    icon_id: str


@dataclass
class EmptyWeatherDTO(WeatherDTO):
    temperature: None = None
    temperature_feels_like: None = None
    weather_desc: None = None
    humidity: None = None
    wind_speed: None = None
    icon_id: None = None

    def __bool__(self):
        return False


@dataclass
class LocationDTO:
    name: str
    country: str
    latitude: Decimal
    longitude: Decimal


@dataclass
class LocationWithWeatherDTO(LocationDTO):
    weather: Union["WeatherDTO", "EmptyWeatherDTO"]
