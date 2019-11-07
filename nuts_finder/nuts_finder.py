import geojson
import requests
import re
from io import BytesIO
from zipfile import ZipFile
from shapely import geometry

YEAR_REGEX = 'NUTS ([0-9]+)'
SCALE_REGEX = '1:([0-9]+) Million'
TOP_URL = ("https://ec.europa.eu/eurostat/cache/"
           "GISCO/distribution/v2/nuts/download")
ZIP_URL = (f"{TOP_URL}/"
           "ref-nuts-{year}-{scale}m.geojson.zip")
NESTED_FILE = 'NUTS_RG_{scale}M_{year}_4326.geojson'


def _middle(values):
    n = len(values)
    is_odd = n % 2
    middle_idx = int((n + is_odd)/2) - 1
    return sorted(values)[middle_idx]


def _setattr(obj, value, value_name, regex, selector):
    allowed_values = _get_available(regex)
    if value is None:
        value = selector(allowed_values)
    if value not in allowed_values:
        raise ValueError(f"'{value_name}' must be one of {allowed_values}")
    setattr(obj, value_name, value)


def _get_available(regex):
    r = requests.get(TOP_URL)
    values = set(int(yr) for yr in
                 re.findall(regex, r.text))
    return values


class NutsFinder:
    def __init__(self, year=None, scale=None):
        _setattr(self, year, 'year', YEAR_REGEX, max)
        _setattr(self, scale, 'scale', SCALE_REGEX, _middle)
        self.shapes = self._get_shapes()

    def _get_shapes(self):
        scale = str(self.scale).zfill(2)
        url = ZIP_URL.format(year=self.year, scale=scale)
        r = requests.get(url)
        r.raise_for_status()
        zipfile = ZipFile(BytesIO(r.content))
        filename = NESTED_FILE.format(year=self.year, scale=scale)
        shapes = geojson.load(zipfile.open(filename))
        return shapes

    def find(self, lat, lon):
        p = geometry.Point(lon, lat)
        nuts = []
        for region in self.shapes['features']:
            s = geometry.shape(region['geometry'])
            if s.contains(p):
                nuts.append(region['properties'])
        return sorted(nuts, key=lambda row: row['LEVL_CODE'])
