import os
from dotenv import load_dotenv
import time
from urllib import response
import pytest
import json
import requests
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.MA_method import moving_average
from massive import RESTClient
from src.check_one_ticker import check_one_ticker
from src.check_all_tickers import check_all_tickers
from src.ticker_symbols import tickers



"""@pytest.fixture
def driver_setup():
    # setup
    driver = webdriver.Chrome()
    yield driver

    #teardown
    #driver.quit()

    #def test_open_vantage():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key"""


def main():

    #check_all_tickers()
    check_one_ticker()
    



if '__main__' == __name__:
    main()
