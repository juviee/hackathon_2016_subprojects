import googlemaps
import json
def get_beach():
  gmaps = googlemaps.Client(key = "AIzaSyBN35ZQgbiGfGnl7RU18ojmhQjVp7uNqU4")
  finput = open("TakeMeToTrip.json", "r")
  
  src_cities = json.loads(finput.read())["cities"]
  finput.close()
  finput = open("TakeMeToTrip.json", "r")
  src_cntr = json.loads(finput.read())["countries"]
  
  beach_countries = []
  
  log = False
  rad = 50000;
  idprev = src_cities[0]['countryId']
  requests = 0
  for c in src_cities:
    if c['countryId'] != idprev:
      log = False
    if log == False:
      requests+=1
      print(requests)
      if requests>7000: 
        break
      try:
        temp_srch = gmaps.places(query = "sea beach", location = [c['latitude'], c['longitude']], radius = rad)
      except:
        temp_srch = gmaps.places(query = "sea beach", location = [c['latitude'], c['longitude']], radius = rad)
    if(temp_srch["results"]):
      log = True
      temp = {"id":c['countryId'], "latitude":c['latitude'], "longitude":c['longitude']}
      print(temp)
      beach_countries.append(temp)
  fw = open("Beach_Countries.json", "wb")
  jsop = json.dumps(beach_countries, indent = 2)
  fw.write(jsop)
  fw.close()
if __name__ == "__main__":
    get_beach();
