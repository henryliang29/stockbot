import os
from dotenv import load_dotenv
import time
from datetime import date, datetime, timedelta
import pytest
import json
import requests

load_dotenv("config.env")
ACCESS_TOKEN = os.getenv("tradier_ACCESS_TOKEN")
BASE_URL = os.getenv("tradier_BASE_URL")

def moving_average(symbol):

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
    }

    end_date = date.today()
    start_date = end_date - timedelta(days=365 * 50)
    # Return the start_date looking back 50 years (in this case) to ensure we have enough data for the moving average calculations 

    response = requests.get(
        f"{BASE_URL}/markets/history",
        headers=headers,
        params={
            "symbol": symbol,
            "interval": "daily",
            "start": start_date,
            "end": end_date,
        },
    )

    data = response.json()

    history = data.get("history")
    if not history or "day" not in history:
        return []
    # If there is no history data, or if the history data does not contain "day" records, return an empty list.



    days = history["day"]
    # Returns the daily historical data for the specified symbol, which is a list of dictionaries where each dictionary contains the data for a single day (e.g., open, close, high, low, volume, date).

    if isinstance(days, dict):
        days = [days]
    # The api provides a single day of historical data as a dictionary instead of a list when there is only one day of data available. 
    # This code checks if the "days" variable is a dictionary and converts it to a list containing that single dictionary if necessary. 
    # This ensures that the rest of the code can process the historical data consistently as a list, 
    # regardless of whether there is one day or multiple days of data.


    moving_averages = []
    moving_average_periods = [1000, 500, 250, 200, 150, 100, 50, 25]
    max_days = len(days)

    for days_count in moving_average_periods:
        if days_count > max_days:
            continue

        last_days = days[-days_count:]
        closing_prices = [day["close"] for day in last_days]
        average = sum(closing_prices) / len(closing_prices)
        moving_averages.append((days_count, average))

    """
        This calculates all moving averages from the oldest to most recent time period
        
        moving_averages = []
        days_count = len(days)

        while days_count >= 1:
            last_days = days[-days_count:]
            #Calculates the farthest moving average first, starting with the longest period (e.g., 50-day) and then halving the period for each 
            # subsequent moving average (e.g., 25-day, 12-day, etc.) until it reaches the shortest period (e.g., 1-day).
            closing_prices = [day["close"] for day in last_days]
            average = sum(closing_prices) / len(closing_prices)
            moving_averages.append((days_count, average))

            if days_count == 1:
                break

            days_count = days_count // 2
    """


    return moving_averages