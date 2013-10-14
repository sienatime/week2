from nose.tools import *
from skills2 import reservation
import datetime

string_date1 = "10/9/2013"
string_date2 = "10/04/2013"
datetime_obj = datetime.datetime(2013,10,9)
test_line1 = "5, 10/9/2013, 10/16/2013"
test_line2 = "15, 10/8/2013, 10/11/2013"

def test_parse_date():
    parsed_date1 = reservation.parse_date(string_date1)
    parsed_date2 = reservation.parse_date(string_date2)

    assert_equal( isinstance(datetime_obj, datetime.datetime), isinstance(parsed_date1, datetime.datetime) )
    assert_equal( isinstance(datetime_obj, datetime.datetime), isinstance(parsed_date2, datetime.datetime) )
    assert_equal( parsed_date1.day, 9)
    assert_equal( parsed_date2.day, 4)

def test_parse_one_line():
    d1 = reservation.parse_one_record(test_line1)
    d2 = {}
    d2["Unit ID"] = 5
    d2["Start Date"] = datetime.datetime(2013,10,9)
    d2["End Date"] = datetime.datetime(2013,10,16)

    assert_equal( d1["Unit ID"], d2["Unit ID"])
    assert_equal( d1["Start Date"], d2["Start Date"])
    assert_equal( d1["End Date"], d2["End Date"])
    