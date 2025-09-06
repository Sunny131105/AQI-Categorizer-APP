# prediction_helper.py
def prediction_helper(aqi_value, pm25=None, pm10=None, no2=None, so2=None, co=None, o3=None):
    """
    Categorize AQI and optionally consider pollutant values.
    """

    # Simple AQI category rules (you can refine this logic)
    if aqi_value <= 50:
        category = "Good"
    elif aqi_value <= 100:
        category = "Moderate"
    elif aqi_value <= 200:
        category = "Unhealthy for Sensitive Groups"
    elif aqi_value <= 300:
        category = "Unhealthy"
    elif aqi_value <= 400:
        category = "Very Unhealthy"
    else:
        category = "Hazardous"

    # Example: if PM2.5 is very high, override category
    if pm25 is not None and pm25 > 250:
        category = "Hazardous"
    if o3 is not None and o3 > 180 and category != "Hazardous":
        category = "Very Unhealthy"

    return {
        "AQI Value": aqi_value,
        "Predict": category
    }

