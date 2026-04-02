from src.weather_api import get_current_weather
from src.utils import transform_api_to_model_input
from src.predict import predict_rain

city = "Berlin"

weather = get_current_weather(city)
model_input = transform_api_to_model_input(weather)
prediction = predict_rain(model_input)

print("City:", city)
print("Model input:", model_input)
print("Prediction:", "Rain" if prediction == 1 else "No Rain")