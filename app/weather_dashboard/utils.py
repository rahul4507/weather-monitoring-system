from weather_dashboard.models import UserPreference


def convert_temperature(temp, preference):
    if preference == UserPreference.TemperaturePreference.CELSIUS:
        return temp - 273.15
    elif preference == UserPreference.TemperaturePreference.FAHRENHEIT:
        return (temp * 9 / 5) + 32
    return temp  # Kelvin
