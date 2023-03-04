from yeelight import Bulb
import datetime
import math
import pytz
from suntime import Sun


def get_current_cct():
    # Düsseldorf-Koordinaten
    lat = 51.2277
    lng = 6.7735

    # Aktuelles Datum und Uhrzeit
    now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    now = now + datetime.timedelta(hours=0)

    # Sonnenaufgang/-untergang-Zeiten berechnen
    sun = Sun(lat, lng)
    sunrise = sun.get_sunrise_time().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Berlin'))
    sunset = sun.get_sunset_time().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Berlin'))

    sunrise_minutes = sunrise.hour * 60 + sunrise.minute
    sunset_minutes = sunset.hour * 60 + sunset.minute

    print(sunset_minutes)

    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    time_of_day = round((now - midnight).total_seconds() / 3600 * 60)

    print(time_of_day)

    # Berechne CCT basierend auf einer Bell-Kurve
    if sunrise_minutes <= time_of_day < sunset_minutes:

        peak_time = (sunrise_minutes + sunset_minutes) / 2
        print("peak: ", peak_time)
        std_dev = (peak_time - sunrise_minutes) / 3
        cct = 1700 + 3800 * math.exp(-0.5 * ((time_of_day - peak_time) / std_dev) ** 2)
    elif time_of_day < sunrise_minutes or time_of_day >= sunset_minutes:
        cct = 2700
    else:
        cct = 5500

    print(cct)
    return round(cct)


def kelvin_to_rgb(temperature):
    # Calculate the CIE chromaticity coordinates
    if temperature <= 4000:
        x = -0.2661239 * ((10 ** 9) / (temperature ** 3)) - 0.2343580 * ((10 ** 6) / (temperature ** 2)) + 0.8776956 * (
                    10 ** 3) / temperature + 0.179910
    else:
        x = -3.0258469 * ((10 ** 9) / (temperature ** 3)) + 2.1070379 * ((10 ** 6) / (temperature ** 2)) + 0.2226347 * (
                    10 ** 3) / temperature + 0.240390
    y = -1.1063814 * x ** 3 - 1.34811020 * x ** 2 + 2.18555832 * x - 0.20219683

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

    return R, G, B


# Output
rgb = kelvin_to_rgb(get_current_cct())
print("old",rgb)


def adjust_color_temperature(rgb, warmth):
    # Convert the RGB value to floats between 0 and 1
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0

    # Calculate the color shift based on the warmth parameter
    shift = warmth * 0.4

    # Adjust the red and green channels based on the shift
    r -= (shift * 0.73)
    g -= (shift * 0.5)
    b += shift

    # Clip the RGB values to the valid range of 0 to 1
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    # Convert the RGB values back to integers between 0 and 255
    r, g, b = int(r * 255), int(g * 255), int(b * 255)

    return (r, g, b)

# Warmer blue color
new_rgb = adjust_color_temperature(rgb, 0.5)
print("new", new_rgb)


# Connect to the Yeelight bulb
bulb = Bulb("192.168.178.42")

# Turn the bulb on
bulb.turn_on()

# Set the brightness to 100%
bulb.set_brightness(100)

# Set the color of the Yeelight bulb using the RGB value
bulb.set_rgb(new_rgb[0], new_rgb[1], new_rgb[2])