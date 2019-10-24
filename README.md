# Nuts Finder [![Build Status](https://travis-ci.com/nestauk/nuts_finder.svg?branch=master)](https://travis-ci.com/nestauk/nuts_finder)

You give it a point, it tells you all the EU NUTS regions.

## Installation

```bash

pip install nuts-finder
```

## Usage

```python

from nuts_finder import NutsFinder

nf = NutsFinder()  # <-- expect a little bit of loading time here whilst it downloads some shapefiles
nf.find(lat=53.406115, lon=-2.965604)  # <-- pretty quick

>>> [{'CNTR_CODE': 'UK',
>>>  'FID': 'UK',
>>>  'LEVL_CODE': 0,
>>>  'NUTS_ID': 'UK',
>>>  'NUTS_NAME': 'UNITED KINGDOM'},
>>> {'CNTR_CODE': 'UK',
>>>  'FID': 'UKD',
>>>  'LEVL_CODE': 1,
>>>  'NUTS_ID': 'UKD',
>>>  'NUTS_NAME': 'NORTH WEST (ENGLAND)'},
>>> {'CNTR_CODE': 'UK',
>>>  'FID': 'UKD7',
>>>  'LEVL_CODE': 2,
>>>  'NUTS_ID': 'UKD7',
>>>  'NUTS_NAME': 'Merseyside'},
>>> {'CNTR_CODE': 'UK',
>>>  'FID': 'UKD72',
>>>  'LEVL_CODE': 3,
>>>  'NUTS_ID': 'UKD72',
>>>  'NUTS_NAME': 'Liverpool'}]
```

## Give me the shapes

You can access all of the NUTS boundaries via:

```python

nf = NutsFinder()
nf.shapes

>>> {"crs": {"properties": {"name": "urn:ogc:def:crs:EPSG::4326"}, "type": "name"}, "features": [{"geometry": {"coordinates": [[[16.107, 50.662], [16.333, 50.592], [16.58, 50.143], [15.438, 50.11], [15.147, 50.523], [15.42, 50.5], [15.584, 50.627], [15.535, 50.779], [16.107, 50.662]]], "type": "Polygon"}, "id": "CZ052", "properties": {"CNTR_CODE": "CZ", "FID": "CZ052", "LEVL_CODE": 3, "NUTS_ID": "CZ052", "NUTS_NAME": "Kr\\u00e1lov\\u00e9hradeck\\u00fd kraj"}, "type": "Feature"}, ...}
```

## Advanced usage

The look-up is performed via point-in-polygon tests from the [official repository of NUTS shapefiles](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts). You can additionally specify the year (`year`) and scale (1:`scale` Million) of the downloaded shapefiles as follows:

```python
nf = NutsFinder(year=2013, scale=60)
```

Note that the default year is the latest available, and the scale is the median available. At time of writing the available years were `{2003, 2006, 2010, 2013, 2016}` and available scales were `{1, 3, 10, 20, 60}`.

## Speed-ups

The `find(...)` method is significantly faster for coarser geographical scales. For most purposes, a scale of around 10 should be sufficient. See below for a benchmark on my laptop (macOS, 2.3 GHz, 16GB) against the scales available at the time of writing:

| `scale`  | time                      |
| ---------|:-------------------------:|
| 1        | 2.66 s ± 191 ms per loop  |
| 3        | 608 ms ± 15 ms per loop   |
| 10       | 215 ms ± 1.85 ms per loop |
| 20       | 145 ms ± 11.6 ms per loop |
| 60       | 105 ms ± 14 ms per loop   |
