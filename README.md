# Nuts Finder |build|

You give it a point, it tells you all the EU NUTS regions.

.. |build| image:: https://travis-ci.org/nestauk/nuts_finder.svg?branch=master
    :target: https://travis-ci.org/nestauk/nuts_finder
    :alt: Build Status (master)

# Usage

```python

from nuts_finder import NutsFinder

nf = NutsFinder()  # <-- expect a little bit of loading time here whilst it downloads some shapefiles
nf.find(lat=53.406115, lon=-2.965604)  # <-- a few seconds

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

# Advanced usage

The look-up is performed via point-in-polygon tests from the [official repository of NUTS shapefiles](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts). You can additionally specify the year (`year`) and scale (1:`scale` Million) of the downloaded shapefiles as follows:

```python
nf = NutsFinder(year=2013, scale=60)
```

Note that the default year is the latest available, and the scale is the most granular available. At time of writing (late 2019), this was `year=2016` and `scale=1`, respectively.
