from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy import exc
import enum
import math

"""
Documentation de Geopy 1.9.1 @ https://geopy.readthedocs.org/en/1.9.1/
"""

class ResultType(enum.Enum):
    OK = 1
    KO = 2

class GeoPyInterface:
    def __init__(self):
        self.geolocator = Nominatim()

    def findLocationByAddress(self, fullAddress):
        resultData = {
            "result": ResultType.KO,
            "location": None,
        }
        # Gestion des exceptions
        try:
            resultData["location"] = self.geolocator.geocode(fullAddress)
            resultData["result"] = ResultType.OK
            return resultData
        except exc.ConfigurationError:
            print("Configuration de l'adresse incorrecte, ou adresse non existante: \n{}".format(exc.ConfigurationError.__str__()))
            return resultData
        except exc.GeocoderQuotaExceeded:
            print("Quota d'utilisation de GeoPy dépassé!")
            return resultData
        except exc.GeocoderUnavailable:
            print("Impossible de se connecter au geocoder: \n{}".format(exc.GeocoderUnavailable.__str__()))
            return resultData
        except exc.GeocoderServiceError:
            print("Impossible de se connecter au geocoder: \n{}".format(exc.GeocoderServiceError.__str__()))
            return resultData

    def getDistanceBetweenTwoCoordinates(self, lat1, long1, lat2, long2):
        # Cette methode est "offline" donc pas besoin de gérer les exceptions de connection, quota, etc...
        location1 = (lat1, long1)
        location2 = (lat2, long2)
        distance = vincenty(location1, location2).kilometers
        return math.floor(distance * 100.0) / 100.0