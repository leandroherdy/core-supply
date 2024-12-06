class TypeClassifier:
    """
    Coordinate-based user type classifier.
    """

    @staticmethod
    def classify_type(lon, lat):
        """
        Classifies a location based on its longitude and latitude.
        :param lon: Longitude of the location.
        :param lat: Latitude of the location.
        :return: Classification ('special', 'normal', or 'laborious').
        """
        if (-46.361899 <= lat <= -34.276938 and -15.411580 <= lon <= -2.196998) or \
           (-52.997614 <= lat <= -44.428305 and -23.966413 <= lon <= -19.766959):
            return 'special'
        elif -54.777426 <= lat <= -46.603598 and -34.016466 <= lon <= -26.155681:
            return 'normal'
        return 'laborious'
