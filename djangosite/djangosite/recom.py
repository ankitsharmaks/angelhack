import json
import time
from yelp import search
from geopy.geocoders import Nominatim


def recommend(tagWithCount, location, locationCoord=None):
    listOfHits = []
    tagName = tagWithCount[0]
    searchCount = tagWithCount[1]
    searchQuery = compileQuery(tagName)
    yelp_response = yelp_search(searchQuery, searchCount, location, locationCoord)
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

    return listOfHits


def compileQuery(tagname):
    return tagname.rstrip()

def findCentroid(listOfFloatPairStrings):
    sumLat = 0
    sumLong = 0
    for entry in listOfFloatPairStrings:
        sumLat += float(entry.split(",")[0])
        sumLong += float(entry.split(",")[1])
    centroidLat = sumLat/len(listOfFloatPairStrings)
    centroidLong = sumLong/len(listOfFloatPairStrings)
    return str(centroidLat)+","+str(centroidLong)


def yelp_search(searchQuery, searchCount,location, locationCoord):
    return search(searchQuery,searchCount, location, locationCoord)

def findNeighbourhood(coordinatePairString):
    geolocator = Nominatim()
    location = geolocator.reverse(coordinatePairString)
    location_neighbouhood = location.raw.get('address').get('neighbourhood')
    return location_neighbouhood

def test():
    listOfTags = ["indian", 4.0]
    listOfCoordsString = ["47.649826,-122.350708", "47.627434, -122.342953", "47.655832, -122.305960"]
    start = time.time()
    output = fetch_recommendation(listOfTags, listOfCoordsString)
    end = time.time()
    print end - start
    print output

def fetch_recommendation(tagWithCount, listOfCoords):
    centroidOfCoords = findCentroid(listOfCoords)
    centroidLocation = findNeighbourhood(centroidOfCoords)
    result = recommend(tagWithCount, centroidLocation, centroidOfCoords)
    return result

