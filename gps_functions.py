from math import *

def getDecimal(coordinate):
    toString = format(coordinate,".6f")
    toString = toString.zfill(12)
    #print(toString)
    degrees = toString[:-9]
    minutes = toString[-9:]

    degreesFloat = float(degrees)
    minutesFloat = float(minutes)

    return degreesFloat + (minutesFloat/60)

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360


    return compass_bearing

def get_dist_to_target(current_location,target_location):
    # function for calculating ground distance between two lat-long locations
    R = 6373.0 # approximate radius of earth in km.

    lat1 = radians( float(current_location[0]) )
    lon1 = radians( float(current_location[1]) )
    lat2 = radians( float(target_location[0]) )
    lon2 = radians( float(target_location[1]) )

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = float(format( R * c , '.5f' )) #rounding. From https://stackoverflow.com/a/28142318/4355695
    return distance
"""
def get_data():
    try:
        data = ser.readline()
        # print(data.decode('utf-8'))

        if data.decode('utf-8') != '':
            test = json.loads(data.decode('utf-8'))
            #if test['data'] == 0:
                #print(test['dir'])
            if test['data'] == 1:
                currentLocation = (getDecimal(test['lat']), getDecimal(test['lon']))
                print(test['satelites'], "\t", format(getDecimal(test['lat']), ".6f"), "\t",
                      format(getDecimal(test['lon']), ".6f"), "\t", format(
                        lat_long_dist(getDecimal(test['lat']), getDecimal(test['lon']), targetLocation[0],
                                      targetLocation[1]) * 1000, ".2f"), "\t",
                      calculate_initial_compass_bearing(currentLocation, targetLocation))
        else:
            print("Timeout - Trying again...")
    except SerialException:
        # Disconnect of USB->UART occured
        print("Device disconnected")
        ser = serial_connect()
    #else:
        # Some data was received // What we want
        #return dataIn
        #print("Some data recieved: ", data)
"""