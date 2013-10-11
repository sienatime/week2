from nose.tools import *
from skills2 import skills

list1 = [1,2,3,4,5]
list2 = [3,4,5,6,7]
list3 = [5,5,5,6,7]

strlist1 = ["hello", "hey","hi"]
strlist2 = ["hello"]

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_common_items():
    assert_equal(skills.common_items(strlist1, strlist2), ["hello"])

def test_common_items2():
    assert_equal( skills.common_items(list1, list2), [3,4,5])