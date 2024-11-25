class BaseOpenWeatherServiceError(Exception):
    """some"""
    def __init__(self, *args):
        self.message = 'some message'

    def __str__(self):
        return self.message


class APIConnectionError(BaseOpenWeatherServiceError):
    """"""
    def __init__(self, *args):
        self.message = 'Ошибка соединения. Проверьте подключение к Интернету или повторите попытку позже.'


class RemoteAPIAccessError(BaseOpenWeatherServiceError):
    """"""
    def __init__(self, *args):
        self.message = 'Ошибка удаленного доступа к API. Проверьте подключение к Интернету или повторите попытку позже.'


class RequestError(BaseOpenWeatherServiceError):
    """"""
    def __init__(self, message: str, requested_url: str, docs_url: str, *args):
        self.message = (f'Произошла ошибка при выполнении запроса по адресу {requested_url}: "{message}". '
                        f'Для разрешения проблемы обратитесь к доккументации REST API: {docs_url}.')


class APIKeyError(BaseOpenWeatherServiceError):
    """"""
    def __init__(self, message: str, *args):
        self.message = f'Произошла ошибка при выполнении запроса: {message}'


class RequestLimitError(BaseOpenWeatherServiceError):
    """"""
    def __init__(self, *args):
        self.message = "Превышен лимит запросов к API. Пожалуйста попробуйте позже или обновите тарифный план OpenWeather."


class LocationNotFoundError(BaseOpenWeatherServiceError):
    """"""
    def __init__(self, name: str, *args):
        self.message = f'Населенный пункт "{name}" не найден.'


class UnknownError(BaseOpenWeatherServiceError):
    """"""
    def __init__(self, error: str, *args):
        self.message = f'Неизвестная ошибка: {error}'


