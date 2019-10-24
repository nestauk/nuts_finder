from unittest import mock
import pytest
from nuts_finder.nuts_finder import _setattr
from nuts_finder.nuts_finder import _get_available
from nuts_finder.nuts_finder import YEAR_REGEX
from nuts_finder.nuts_finder import SCALE_REGEX
from nuts_finder import NutsFinder
from nuts_finder.nuts_finder import _middle


class Object:
    pass


def test_middle():
    assert _middle(['a', 'b', 'd', 'c', 'e']) == 'c'
    assert _middle(['a', 'd', 'c', 'e']) == 'c'
    assert _middle(['a', 'b', 'e']) == 'b'
    assert _middle([4, 3, 4]) == 4
    assert _middle([1, 2, 1, 3]) == 1
    assert _middle([1, 2, 1, 2, 3]) == 2


@mock.patch('nuts_finder.nuts_finder._get_available')
def test_set_attr_default(mocked):
    values = (100, 23, -23)
    mocked.return_value = values
    obj = Object()
    _setattr(obj, value=None,
             regex='blah',
             selector=min,
             value_name='test_value')
    assert obj.test_value == -23

    obj = Object()
    _setattr(obj, value=None,
             regex='blah',
             selector=max,
             value_name='test_value')
    assert obj.test_value == 100


@mock.patch('nuts_finder.nuts_finder._get_available')
def test_set_attr_success(mocked):
    values = (100, 23, -23)
    mocked.return_value = values
    for selector in (max, min):
        for v in values:
            obj = Object()
            _setattr(obj, value=v,
                     regex='blah',
                     selector=selector,
                     value_name='test_value')
            assert obj.test_value == v


@mock.patch('nuts_finder.nuts_finder._get_available')
def test_set_attr_success(mocked):
    allowed = (100, 23, -23)
    not_allowed = ('a', '23', 101)
    mocked.return_value = allowed
    for selector in (max, min, _middle):
        for v in not_allowed:
            with pytest.raises(ValueError):
                obj = Object()
                _setattr(obj, value=v,
                         regex='blah',
                         selector=selector,
                         value_name='test_value')


def test_get_available_years():
    years = _get_available(YEAR_REGEX)
    assert all(type(yr) is int for yr in years)
    assert len(years) > 0
    assert all(yr > 2000 and yr < 2100 for yr in years)


def test_get_available_scales():
    scales = _get_available(SCALE_REGEX)
    assert all(type(s) is int for s in scales)
    assert len(scales) > 0
    assert all(s >= 1 and s < 100 for s in scales)


def test_nut_finder():
    nf = NutsFinder()
    result = nf.find(53.406115, -2.965604)
    assert result == [{'CNTR_CODE': 'UK',
                       'FID': 'UK',
                       'LEVL_CODE': 0,
                       'NUTS_ID': 'UK',
                       'NUTS_NAME': 'UNITED KINGDOM'},
                      {'CNTR_CODE': 'UK',
                       'FID': 'UKD',
                       'LEVL_CODE': 1,
                       'NUTS_ID': 'UKD',
                       'NUTS_NAME': 'NORTH WEST (ENGLAND)'},
                      {'CNTR_CODE': 'UK',
                       'FID': 'UKD7',
                       'LEVL_CODE': 2,
                       'NUTS_ID': 'UKD7',
                       'NUTS_NAME': 'Merseyside'},
                      {'CNTR_CODE': 'UK',
                       'FID': 'UKD72',
                       'LEVL_CODE': 3,
                       'NUTS_ID': 'UKD72',
                       'NUTS_NAME': 'Liverpool'}]
