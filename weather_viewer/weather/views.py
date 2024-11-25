import logging
from decimal import Decimal

from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView

from .models import Location
from .schemas import LocationWithWeatherDTO, EmptyWeatherDTO
from .services.open_weather_api_service import OpenWeatherService
from .services.exceptions import BaseOpenWeatherServiceError

# Create your views here.

logger = logging.getLogger('weather_viewer.errors')


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'weather/index.html'
    context_object_name = 'locations'
    paginate_by = 4

    def get_queryset(self):
        locations = Location.objects.filter(user=self.request.user).order_by('-id')

        res = []
        msg = None

        for loc in locations:
            weather = EmptyWeatherDTO()

            if msg is None:
                try:
                    weather = OpenWeatherService.get_weather_by_coords(loc.latitude, loc.longitude)
                except BaseOpenWeatherServiceError as e:
                    logger.error(f'Error getting weather from OpenWeatherService: {e}')
                    msg = str(f'Произошла ошибка при получении данных погоды: {e}')

            res.append(
                LocationWithWeatherDTO(
                    name=loc.name,
                    country=loc.country,
                    latitude=loc.latitude,
                    longitude=loc.longitude,
                    weather=weather
                )
            )

        if msg:
            messages.error(self.request, msg)

        return res

    def post(self, request, *args, **kwargs):
        logger.debug(f'Delete location by coords: latitude: {request.POST["latitude"]}, longitude: '
                     f'{request.POST["longitude"]} for user: {request.user}')

        try:
            location = Location.objects.filter(user=request.user).get(
                latitude=Decimal(request.POST['latitude'].replace(',', '.')),
                longitude=Decimal(request.POST['longitude'].replace(',', '.'))
            )

            location.delete()
            logger.debug(f'Location successfully deleted')
        except Exception as e:
            messages.error(request, message='К сожалению не удалось удалить локацию в связи с непредвиденной ошибкой')
            logger.error(f'Unexpected error while deleting location: {e}')

        return redirect('home')


class SearchView(LoginRequiredMixin, ListView):
    template_name = 'weather/search.html'
    context_object_name = 'locations'

    def get_queryset(self):
        location = self.request.GET.get('location')

        try:
            if location:
                locations = OpenWeatherService.get_locations_by_name(
                    name=location
                )

                return locations
        except BaseOpenWeatherServiceError as e:
            logger.error(f'Error getting locations from OpenWeatherService: {e}')
            msg = str(f'Ошибка при попытке найти населенные пункты: {e}')
            messages.error(self.request, msg)

        return []

    def post(self, request, *args, **kwargs):
        try:
            location = Location.objects.create(
                name=request.POST['name'],
                country=request.POST['country'],
                latitude=Decimal(request.POST['latitude'].replace(',', '.')),
                longitude=Decimal(request.POST['longitude'].replace(',', '.')),
                user=request.user,
            )

            logger.debug(f'Add location {location} for user {request.user}')
            location.save()
            logger.debug(f'Location successfully added')

            return redirect('home')

        except IntegrityError:
            logger.debug(f'Location already added for user')
            messages.error(request, "Выбранная локация уже добавлена в вашу коллекцию")
            return redirect('home')


