from app import add
import pytest
import requests
import time 

@pytest.fixture
def count():
    return 1

def test_add1():
    assert add(2, 3) == 5

def test_api(count):
    print("testing api")
    try:
        time.sleep(1)
        r = requests.get('http://0.0.0.0:5000/')
        print(r.text)
        assert r.text == 'Hello World! I have been seen {} times.\n'.format(count)
    except Exception as e:
        print("exception: ", e)
        assert False
    
def test_mysql():
    print("testing mysql")
    try:
        time.sleep(1)
        r = requests.get('http://0.0.0.0:5000/mysql')
        print(r.text)
        assert True
    except Exception as e:
        print("exception: ", e)
        assert False