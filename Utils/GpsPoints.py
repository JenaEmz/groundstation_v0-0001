import math
class GpsPoints(object):
    def __init__(self,lat,lon,home_lat,home_lon):
        self.lat = lat
        self.lon = lon
        self.home_lat = home_lat
        self.home_lon = home_lon
        self.Wgs84toLocal()

    def setLocal(self,x,y):
        self.x = x
        self.y = y
        self.LocaltoWgs84()

    def Wgs84toLocal(self):
        M_DEG_TO_RAD = 0.017453292519943295
        CONSTANTS_RADIUS_OF_EARTH=6371000
        DBL_EPSILON = 2e-016
        lat_rad = self.lat * M_DEG_TO_RAD;
        lon_rad = self.lon * M_DEG_TO_RAD;

        sin_lat = math.sin(lat_rad);
        cos_lat = math.cos(lat_rad);
        cos_d_lon = math.cos(lon_rad - self.home_lon*M_DEG_TO_RAD);
        home_sin_lat = math.sin(self.home_lat* M_DEG_TO_RAD);
        home_cos_lat = math.cos(self.home_lat* M_DEG_TO_RAD)
        arg = home_sin_lat * sin_lat + home_cos_lat * cos_lat * cos_d_lon;

        if (arg > 1.0) :
            arg = 1.0;

        elif (arg < -1.0):
            arg = -1.0;

        c = math.acos(arg);
        if c< DBL_EPSILON :
            k=1
        else:
            k = c / math.sin(c);

        self.x = k * (home_cos_lat  * sin_lat - home_sin_lat * cos_lat * cos_d_lon) *CONSTANTS_RADIUS_OF_EARTH;
        self.y = k * cos_lat * math.sin(lon_rad - self.home_lon * M_DEG_TO_RAD) *CONSTANTS_RADIUS_OF_EARTH;

    def LocaltoWgs84(self):
        M_DEG_TO_RAD = 0.017453292519943295
        CONSTANTS_RADIUS_OF_EARTH = 6371000
        DBL_EPSILON =2e-016
        M_PI = 3.14159265
        x_rad = self.x / CONSTANTS_RADIUS_OF_EARTH;
        y_rad = self.y / CONSTANTS_RADIUS_OF_EARTH;
        c = math.sqrt(x_rad * x_rad + y_rad * y_rad);
        sin_c = math.sin(c);
        cos_c = math.cos(c);
        home_sin_lat = math.sin(self.home_lat* M_DEG_TO_RAD);
        home_cos_lat = math.cos(self.home_lat* M_DEG_TO_RAD)
        if (math.fabs(c) > DBL_EPSILON):
            lat_rad = math.asin(cos_c * home_sin_lat + (x_rad * sin_c * home_cos_lat) / c);
            lon_rad = (self.home_lon * M_DEG_TO_RAD + math.atan2(y_rad * sin_c, c *  home_cos_lat * cos_c - x_rad * home_sin_lat * sin_c));
        else:
            lat_rad = self.home_lat*M_DEG_TO_RAD;
            lon_rad = self.home_lon*M_DEG_TO_RAD;

        self.lat = lat_rad * 180.0 / M_PI;
        self.lon = lon_rad * 180.0 / M_PI;
