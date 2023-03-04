from yeelight import Bulb
import datetime
import math
import astral.sun
import pytz
from suntime import Sun

def get_current_cct():
    # Düsseldorf-Koordinaten
    lat = 51.2277
    lng = 6.7735
    
    # Aktuelles Datum und Uhrzeit
    now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    now = now + datetime.timedelta(hours=-7)

    # Sonnenaufgang/-untergang-Zeiten berechnen
    sun = Sun(lat, lng)
    sunrise = sun.get_sunrise_time().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Berlin'))
    sunset = sun.get_sunset_time().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Berlin'))

    print(sunrise)
    print(sunset)

    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    time_of_day = (now - midnight).total_seconds() / 3600
    

    # Berechne CCT basierend auf einer Bell-Kurve
    if sunrise.time() <= now.time() < sunset.time():
        peak_time = (sunrise.hour + sunset.hour) / 2
        std_dev = (peak_time - sunrise.hour) / 3
        cct = 2700 + 3800 * math.exp(-0.5 * ((time_of_day - peak_time) / std_dev) ** 2)
    elif now.time() < sunrise.time() or now.time() >= sunset.time():
        cct = 3200
    else:
        cct = 5500
        
    print(cct)
    return cct

def kelvin_to_rgb(temperature):
    # Calculate the CIE chromaticity coordinates
    if temperature <= 4000:
        x = -0.2661239 * ((10**9) / (temperature**3)) - 0.2343580 * ((10**6) / (temperature**2)) + 0.8776956 * (10**3) / temperature + 0.179910
    else:
        x = -3.0258469 * ((10**9) / (temperature**3)) + 2.1070379 * ((10**6) / (temperature**2)) + 0.2226347 * (10**3) / temperature + 0.240390
    y = -1.1063814 * x**3 - 1.34811020 * x**2 + 2.18555832 * x - 0.20219683
    
    # Calculate the XYZ tristimulus values
    z = 1 - x - y
    Y = 1
    X = (Y / y) * x
    Z = (Y / y) * z
    
    # Calculate the RGB values
    R = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
    G = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
    B = 0.0557 * X - 0.2040 * Y + 1.0570 * Z
    
    # Convert the RGB values to the range [0, 255]
    R = max(0, min(255, int(R * 255)))
    G = max(0, min(255, int(G * 255)))
    B = max(0, min(255, int(B * 255)))
    
    return (R, G, B)

# Ausgabe
rgb = kelvin_to_rgb(get_current_cct())
print(rgb)

# Connect to the Yeelight bulb
bulb = Bulb("192.168.178.42")

# Turn the bulb on
bulb.turn_on()

# Set the brightness to 50%
bulb.set_brightness(100)

# Set the color of the Yeelight bulb using the RGB value
bulb.set_rgb(rgb[0], rgb[1], rgb[2])
