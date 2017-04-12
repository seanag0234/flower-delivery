# key = d0d251a70ea814756896149ac8bcd3b3
# http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}


def create_url(lat, long):
    return "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(long)