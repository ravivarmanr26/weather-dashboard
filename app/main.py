import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

llm = ChatGroq(model='llama-3.2-11b-vision-preview')

@llm.tool
def get_weather(location: str) -> str:
    print(f"Fetching weather for {location}")
    try:
        weather_url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
        response = requests.get(weather_url)
        weather_data = response.json()
        
        if "current" in weather_data:
            condition = weather_data["current"]["condition"]["text"]
            temperature = weather_data["current"]["temp_k"]
            pressure = weather_data["current"]["pressure_mb"]
            humidity = weather_data["current"]["humidity"]
            return f"Weather in {location}: {condition}, Temperature: {temperature}K, Pressure: {pressure} hPa, Humidity: {humidity}%"
        else:
            return f"Could not retrieve weather data for {location}."
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Error fetching weather data."

from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

prompt = hub.pull("hwchase17/openai-functions-agent")
tools = [get_weather]
agent = create_tool_calling_agent(llm, tools, prompt)
Agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

@app.get("/weather")
async def weather(location: str):
    response = Agent_executor.invoke({'input': location})
    return JSONResponse(content={"weather": response['output']})
