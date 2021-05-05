"""
nuts_finder
-----------

You give it a point, it tells you all the EU NUTS regions
"""
import geojson
import requests
import re
from io import BytesIO
from zipfile import ZipFile
from shapely import geometry
from functools import lru_cache
import logging

YEAR_REGEX = "NUTS ([0-9]+)"
SCALE_REGEX = "1:([0-9]+) Million"
TOP_URL = "https://ec.europa.eu/eurostat/cache/" "GISCO/distribution/v2/nuts/download"
ZIP_URL = f"{TOP_URL}/" "ref-nuts-{year}-{scale}m.geojson.zip"
NESTED_FILE = "NUTS_RG_{scale}M_{year}_4326.geojson"


def _middle(values):
    """Lower bound of median, without using numpy (heavy reqs)"""
    n = len(values)
    is_odd = n % 2
    middle_idx = int((n + is_odd) / 2) - 1
    return sorted(values)[middle_idx]


def _setattr(obj, value, value_name, regex, selector):
    """Either apply setattr on `obj` with value `value`, if `value` is not None, otherwise
    select a `value` from the available range of allowed values, selected by a custom `selector`
    function.

    Args:
        obj: An object on which to run setattr
        value: A value which if not None will be set as an attribute of object
        value_name (str): The name of the new attribute
        regex (str): regex string by which to find allowed values on the NUTS website.
        selector (function): Function which takes an iterable and selects a value.
    """
    allowed_values = _get_available(regex)
    if value is None:
        value = selector(allowed_values)
    if value not in allowed_values:
        raise ValueError(f"'{value_name}' must be one of {allowed_values}")
    setattr(obj, value_name, value)


@lru_cache()
def _get_available(regex):
    """Use the provided regex to find allowed values on the NUTS website."""
    r = requests.get(TOP_URL, verify=True)
    values = set(int(yr) for yr in re.findall(regex, r.text))
    return values


class NutsFinder:
    """
    Object for holding onto NUTS data and exposing to the user, also
    providing a lat, lon lookup
    """

    def __init__(self, year=None, scale=None):
        """
        Args:
            year (int): If provided, NUTS regions for this year will be used (if available)
            scale (int): If provided, NUTS regions at this resolution will be used (if available)
        """
        self.years = list(_get_available(YEAR_REGEX))
        self.year_selector = max
        _setattr(self, year, "year", YEAR_REGEX, self.year_selector)
        _setattr(self, scale, "scale", SCALE_REGEX, _middle)  # Take the middle scale
        self.shapes = self._get_shapes()

    def _get_shapes(self):
        """Load the shape files for the given year and scale"""
        scale = str(self.scale).zfill(2)
        filename = NESTED_FILE.format(year=self.year, scale=scale)
        url = ZIP_URL.format(year=self.year, scale=scale)
        r = requests.get(url, verify=True)
        r.raise_for_status()
        try:
            with ZipFile(BytesIO(r.content)) as zipfile:
                with zipfile.open(filename) as f:
                    shapes = geojson.load(f)
        # For some reason this year/scale isn't available
        except KeyError:
            logging.warning(
                f"No match for this year ({self.year}) and scale ({self.scale})"
            )
            # Remove this year from the sample and try another year
            self.years.remove(self.year)
            self.year = self.year_selector(self.years)
            logging.warning(f"Retrying with year ({self.year})")
            return self._get_shapes()
        return shapes

    def find(self, lat, lon):
        """Find every NUTS region for this lat, lon"""
        p = geometry.Point(lon, lat)
        nuts = []
        for region in self.shapes["features"]:
            s = geometry.shape(region["geometry"])
            if s.contains(p):
                nuts.append(region["properties"])
        return sorted(nuts, key=lambda row: row["LEVL_CODE"])
