import json
from yelp import search
from geopy.geocoders import Nominatim


def recommend(listOfTags, location, locationCoord=None):
    listOfHits = []

    searchQuery = compileQuery(listOfTags)
    yelp_response = yelp_search(searchQuery, location, locationCoord)
    businesses = yelp_response.get('businesses')

    for entry in businesses:
        business_id = entry['id']
        name = entry['name']
        image_url = entry['image_url']
        categories = entry['categories']
        yelp_url = entry['url']
        rating = entry['rating']
        entryDump = {'business_id': business_id, 'name': name, 'image_url': image_url, 'categories': categories,
                  'yelp_url': yelp_url, 'rating': rating}
        listOfHits.append(entryDump)

    json_output = json.dumps(listOfHits)
    return json_output


def compileQuery(listOfTags):
    searchQuery = ""
    for tag in listOfTags:
        searchQuery += tag + " "
    return searchQuery.rstrip()

def findCentroid(listOfFloatPairStrings):
    sumLat = 0
    sumLong = 0
    for entry in listOfFloatPairStrings:
        sumLat += float(entry.split(",")[0])
        sumLong += float(entry.split(",")[1])
    centroidLat = sumLat/len(listOfFloatPairStrings)
    centroidLong = sumLong/len(listOfFloatPairStrings)
    return str(centroidLat)+","+str(centroidLong)


def yelp_search(searchQuery, location, locationCoord):
    return search(searchQuery, location, locationCoord)

def findNeighbourhood(coordinatePairString):
    geolocator = Nominatim()
    location = geolocator.reverse(centroidOfCoordsString)
    location_neighbouhood = location.raw.get('address').get('neighbourhood')
    return location_neighbouhood

# listOfTags = ["good", "chinese"]
listOfTags = ["tacos"]
listOfCoordsString = ["47.649826,-122.350708", "47.627434, -122.342953", "47.655832, -122.305960"]

centroidOfCoordsString = findCentroid(listOfCoordsString)
centroidLocation = findNeighbourhood(centroidOfCoordsString)
print centroidLocation

result = recommend(listOfTags, centroidLocation, centroidOfCoordsString)

print result

