import unittest
from geolocation.GeoPyInterface import Geolocator, ResultType

class TestGeolocator(unittest.TestCase):
    def setUp(self):
        self.geolocator = Geolocator()

    def tearDown(self):
        pass

    def test_geolocationEPFC(self):
        address = "2 avenue charles thielemans 1150 bruxelles"
        location = self.geolocator.findLocationByAddress(address)
        if location["result"] == ResultType.OK:
            print("{}".format(location["location"].__str__()))
            print("Latitude = {}".format(location["location"].latitude.__str__()))
            print("Longitude = {}".format(location["location"].longitude.__str__()))

    def test_distance(self):
        address1 = "2 avenue charles thielemans 1150 bruxelles"
        address2 = "1 clos des artistes 1030 bruxelles"
        location1 = self.geolocator.findLocationByAddress(address1)
        location2 = self.geolocator.findLocationByAddress(address2)
        if location1["result"] == ResultType.OK and location2["result"] == ResultType.OK:
            distance = self.geolocator.getDistanceBetweenTwoCoordinates(
                location1["location"].latitude,
                location1["location"].longitude,
                location2["location"].latitude,
                location2["location"].longitude)
            print("{} km".format(distance.__str__()))

    def test_fakeAddress(self):
        #TODO
        pass

if __name__ == "__main__":
    unittest.main()