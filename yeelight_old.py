from yeelight import Bulb
import datetime
import pytz
import pvlib
from color_temperature import CCT_to_RGB


# Breite und Länge von Düsseldorf
lat = 51.2277
lng = 6.7735

# Aktuelle lokale Zeit
now = datetime.datetime.now(pytz.timezone('Europe/Berlin'))

# Sonnenposition
sun_position = pvlib.solarposition.get_solarposition(now, lat, lng)

# Luftmasse
air_mass = pvlib.atmosphere.get_relative_airmass(sun_position['apparent_zenith'])

cct = -2713 * air_mass + 5320

# CCT to RGB
rgb = temp.CCT_to_RGB(cct)

# RGB values
r = int(rgb[0] * 255)
g = int(rgb[1] * 255)
b = int(rgb[2] * 255)

# RGB values ausgeben
print(f"R: {r}, G: {g}, B: {b}")


# Connect to the Yeelight bulb
bulb = Bulb("192.168.178.42")

# Turn the bulb on
bulb.turn_on()

# Set the brightness to 50%
bulb.set_brightness(100)

# Set the color of the Yeelight bulb using the RGB value
bulb.set_rgb(rgb[0], rgb[1], rgb[2])
