from weather_dashboard.models import Alert, UserPreference


def check_and_trigger_alerts(weather_update):
    user_preference = UserPreference.objects.first()
    if user_preference and user_preference.alert_enabled:
        # Check if alert condition is met
        if weather_update.temp > user_preference.temp_threshold:
            print("Triggered alert")
            Alert.objects.get_or_create(
                city=weather_update.city,
                alert_type='Temperature Alert',
                threshold_value=user_preference.temp_threshold,
                weather_update=weather_update,
                defaults={'is_triggered': True}
            )
