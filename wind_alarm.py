import sys, json, os
from time import localtime, sleep
from bs4 import BeautifulSoup
from urllib2 import urlopen

WUNDERGROUND_KEY = os.environ['WUNDERGROUND_KEY']
FORECAST_KEY = os.environ['FORECAST_KEY']

def get_wind_wunderground():
    f = urlopen('http://api.wunderground.com/api/' + WUNDERGROUND_KEY + '/geolookup/conditions/q/NC/Waves.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    wind_mph = parsed_json['current_observation']['wind_mph']
    f.close()
    return wind_mph

#waves = 35.5775,-75.4672
#avon = 35.3520,-75.5034
def get_wind():
    f = urlopen('https://api.forecast.io/forecast/' + FORECAST_KEY + '/35.3520,-75.5034')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    wind_mph = parsed_json['currently']['windSpeed']
    f.close()
    current_time = localtime()
    print "Wind speed at %s:%02d: %s" % (current_time.tm_hour, current_time.tm_min, wind_mph)
    return wind_mph

argv = sys.argv
if len(sys.argv) != 4:
    print "Usage: [ python ] wind_alarm.py hour minute minimum_wind_speed"
    print "Example: [ python ] alarm_clock.py 8 30 17"
    sys.exit(1)

try:
    target_hour = int(argv[1])
except ValueError:
    print "Invalid numeric value (%s) for hours" % argv[1]
    print "Should be an integer"
    sys.exit(1)

try:
    target_minute = int(argv[2])
except ValueError:
    print "Invalid numeric value (%s) for minutes" % argv[2]
    print "Should be an integer"
    sys.exit(1)

try:
    target_wind = int(argv[3])
except ValueError:
    print "Invalid numeric value (%s) for hours" % argv[3]
    print "Should be an integer"
    sys.exit(1)

if not 0 <= target_hour < 24:
    print "Invalid value, should be 0 <= {hour} < 24"
    sys.exit(1)

if not 0 <= target_minute < 60:
    print "Invalid value, should be 0 <= {minute} < 60"
    sys.exit(1)

if not 0 <= target_wind:
    print "Invalid value, should be 0 <= {wind}"
    sys.exit(1)

try:
    current_time = localtime()
    dif_hours = (target_hour - current_time.tm_hour) % 24
    dif_minutes = (target_minute - current_time.tm_min) % 60
    dif_seconds = (dif_hours * 60 + dif_minutes) * 60

    sleep(dif_seconds)

    current_wind = get_wind()
    while current_wind < target_wind:
        sleep(5 * 60) # sleep for 5m
        current_wind = get_wind()

    for _ in range(5):
        os.system('say "Wake up, it\'s blowing %s miles per hour"' % current_wind)
        sleep(3)

except KeyboardInterrupt:
    print "Interrupted by user"
    sys.exit(1)
