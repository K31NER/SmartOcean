import os
import json
import requests
from dotenv import load_dotenv

load_dotenv() # Cargamos las variables de entorno

# Obtenemos la api key para realizar solicitudes
KEY = os.getenv("API_KEY_CLIMA")

# Definimos la ruta base
URL_BASE = f"http://api.weatherapi.com/v1/current.json?key={KEY}"

# Dicionario de playas con sus coordenadas 
playas = {
    "bocagrande": (10.3989, -75.5512),
    "playa_blanca_baru": (10.2605, -75.5745),
    "la_boquilla": (10.4567, -75.4863),
    "marbella": (10.4342, -75.5333),
    "cholon_baru": (10.2687, -75.5890),
    "manzanillo_del_mar": (10.5005, -75.4813),
    "playa_azul": (10.5022, -75.4760),
    "laguito": (10.3964, -75.5582),
    "castillogrande": (10.3903, -75.5530)
}

def get_weather(playa:str):
    # Validamos que la playa exista 
    if playa not in playas:
        return {"error": "Playa no encontrada"}
    
    # Obtenemos sus coordenadad
    lat, lon = playas[playa]
    
    # Personalizamos la url
    url = f"{URL_BASE}&q={lat},{lon}&aqi=no"
    
    # Hacemos l solicitud
    response = requests.get(url)
    
    # Validamos que sea exitosa
    if response.status_code != 200:
        return {"error": "Solicitud no completada"}
    
    # Obtenemos los datos
    data = response.json()
    current_data = data.get("current","NOT FOUND")
    grados_celcius = current_data.get("temp_c","NOT FOUND")
    viento = current_data.get("wind_kph","NOT FOUND")
    is_day = current_data.get("is_day", "NOT FOUND")
    clima_data = current_data.get("condition", "NOT FOUND")
    clima = clima_data.get("text","NOT FOUND")
    clima_icon = clima_data.get("icon", "NOT FOUND")
    humedad = current_data.get("humidity","NOT FOUND")
    nubes = current_data.get("cloud","NOT FOUND")
    
    # Preparamos el diccionario
    weather_data = {
        "Playa": playa,
        "Temperatura": grados_celcius,
        "Viento": viento,
        "Es_dia": is_day,
        "Clima": clima,
        "Icono_clima": clima_icon,
        "Humedad": humedad,
        "Nubes": nubes
    }
    return weather_data

def update_weather():
    climas = [get_weather(playa) for playa in playas.keys()]
    with open("Clima_playas.json","w",encoding="utf-8") as file:
        json.dump(climas,file,indent=4,ensure_ascii=False)
    return {"mensaje":"Json creado con exito"}

if __name__ == "__main__":
    print(update_weather())