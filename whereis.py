#-*-coding: cp1251-*-
import googlemaps

#credentials: googlemaps - grip-key: AIzaSyBv9aZckFBbPa0wOx_jYDps_8Uou13TGdk <--use this wan, fagt
#credentials: googlemaps - randomtripkey: AIzaSyBN35ZQgbiGfGnl7RU18ojmhQjVp7uNqU4
def routeCountry(fro, to,  gmaps = None):
  '''Returns route from A to B points
  fro/to - (lat,long) tuples/lists||string addresses of points
  Returns list with routes: 
  [
    list with types of reasonable transport(like trains)
    list with fare for transport//tries to take it from google, if not - counts from distance
    length of time of travel(in seconds)
    distance(meters)
  ]
  '''
  transport_dict = {
    'HIGH_SPEED_TRAIN': "Сапсан",
    'HEAVY_RAIL':'Поезд дальнего следования',
    'COMMUTER_TRAIN':"Электричка",
    'INTERCITY_BUS':"Межгородской автобус"
  }
  if gmaps == None:
    gmaps = googlemaps.Client(key = "AIzaSyBv9aZckFBbPa0wOx_jYDps_8Uou13TGdk")
  src_routes = gmaps.directions(origin = fro, destination = to, mode = 'transit', alternatives = False, language = 'rus', units = 'metric')
  #format src_distance_all = gmaps.distance(origin = from, destination = to, mode = 'transit', alternatives = True, language = 'rus', units = 'metric')
  route_array = []
  transport_set = {'HIGH_SPEED_TRAIN','HEAVY_RAIL','COMMUTER_TRAIN','INTERCITY_BUS'}
  eq = 1.1
  for route in src_routes:
    route_temp = [] #points of trip that matters
    trip = [] #result of all this
    duration = 0 #seconds
    length = 0.0 #meters
    fare = 0.0 #money
    for leg in route['legs']:
      leg_distance = leg['distance']['value']
      length += leg_distance

      try:
        duration += leg['duration']['value']
      except KeyError:
        duration += 6*leg_distance #estimated time(guy walks 1 meter per second), if there is no 'google'' estimated time

      for step in leg['steps']:
        try:
          veht = step['transit_details']['line']['vehicle']['type']
          if veht in transport_set:
            route_temp.append(transport_dict[veht])
        except:
          pass
    #do nothing lul
    #building our trip file:
    try:
      fare = [int([route['fare']['value']])]
      fare.append(route['fare']['currency'])
    except:
      fare = [int(length*eq/1000)]
      fare.append('RUB')
    trip.append(route_temp)
    trip.append(fare)
    trip.append(duration)
    trip.append(length)
    route_array.append(trip)
  return route_array

if __name__ == "__main__":
  a = routeCountry('Moscow', 'London')
  print(a);
  
