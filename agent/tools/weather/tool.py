# agent/tools/weather/tool.py
import os
import requests
from typing import Dict, Any
from agent.base_tool import BaseTool
from agent.schemas import TOOL_SCHEMAS, ToolType

class WeatherTool(BaseTool):
    """Weather tool for getting weather information."""
    
    def __init__(self):
        super().__init__(TOOL_SCHEMAS[ToolType.WEATHER])
    
    def execute(self, args: Dict[str, Any], question: str = "") -> str:
        city = args["city"]
        api_key = os.getenv("WEATHER_API_KEY")
        
        if not api_key:
            raise Exception("WEATHER_API_KEY not set in .env file")
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"].lower(),
            "city": city
        }
        
        # Generate natural response using question context
        if question:
            try:
                import google.generativeai as genai
                response_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                prompt = (
                    f"User asked: '{question}'. Weather data for {city}: "
                    f"temperature is {weather_data['temp']}°C, description is '{weather_data['description']}'. "
                    f"Generate a natural response addressing the user's prompt using this weather data."
                )
                
                weather_response = response_model.generate_content(prompt)
                return getattr(weather_response, "text", None) or (
                    f"The temperature in {city.title()} is {weather_data['temp']}°C with {weather_data['description']}."
                )
            except Exception as e:
                print(f"DEBUG: Error generating weather response: {str(e)}")
                return f"The temperature in {city.title()} is {weather_data['temp']}°C with {weather_data['description']}."
        
        # Fallback to simple response
        return f"The temperature in {city.title()} is {weather_data['temp']}°C with {weather_data['description']}."