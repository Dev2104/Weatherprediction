def transform_api_to_model_input(api_data: dict) -> dict:
    """
    Convert OpenWeather API response into the feature format expected by the model.
    """

    main = api_data["main"]
    wind = api_data.get("wind", {})

    return {
        "MinTemp": main["temp_min"],
        "MaxTemp": main["temp_max"],
        "Humidity9am": main["humidity"],
        "Humidity3pm": main["humidity"],
        "Pressure9am": main["pressure"],
        "Pressure3pm": main["pressure"],
        "WindSpeed9am": wind.get("speed", 0),
        "WindSpeed3pm": wind.get("speed", 0),
    }