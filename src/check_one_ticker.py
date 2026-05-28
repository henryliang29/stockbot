import requests
import datetime
import os
from dotenv import load_dotenv
from MA_method import moving_average


def check_one_ticker():

    load_dotenv("config.env")
    ACCESS_TOKEN = os.getenv("tradier_ACCESS_TOKEN")
    BASE_URL = os.getenv("tradier_BASE_URL")


    if not ACCESS_TOKEN:
        raise RuntimeError("Set TRADIER_SANDBOX_TOKEN before calling the Tradier API.")

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
    }


    flag = False
    while(not flag):
        try:
            SYMBOL = input("Enter a stock symbol (e.g., AAPL): ").upper().strip()
            params={"symbols": {SYMBOL}, "greeks": "false"}
                
            response = requests.get(
                f"{BASE_URL}/markets/quotes",
                headers=headers,
                params=params,
            )
            if( 'unmatched_symbols' in str(response.json().get("quotes"))):
                print(f"Symbol {SYMBOL} not found. Please enter a valid stock symbol.")
            else:
                flag = True
        except requests.RequestException as e:
            print(f"Error fetching quote for {SYMBOL}: {e}")
    
        
    params={"symbols": {SYMBOL}, "greeks": "false"}
            
    response = requests.get(
        f"{BASE_URL}/markets/quotes",
        headers=headers,
        params=params,
    )

    """
    print(f"URL: {response.url}")
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    """
    if response.status_code != 200:
        raise RuntimeError(f"Tradier returned {response.status_code}: {response.text}")

    data = response.json()
    dataquote = data.get("quotes").get("quote")

    """ # Prints all the stock data in a human-readable format, with special formatting for dates, volumes, and prices.
        print("\n")
        # The .items() method returns a view object that displays a list of a dictionary's key-value tuple pairs.
        for key, value in dataquote.items():
            if "date" in key.lower() and isinstance(value, int):
                date_value = datetime.fromtimestamp(value / 1000)
                print(f"{key}: {date_value.strftime('%B %d, %Y')}")
            elif "volume" in key.lower() and isinstance(value, int):
                print(f"{key}: {value:,} shares")
            elif isinstance(value, str):
                print(f"{key}: {value}")
            elif isinstance(value, int):
                print(f"{key}: {value:,}")
            elif isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")

    """

    moving_averages = moving_average(SYMBOL)

    average_values = [average for days_count, average in moving_averages]

    uptrend_count = 0
    downtrend_count = 0

    for i in range(len(average_values) - 1):
        older_average = average_values[i]
        recent_average = average_values[i + 1]
        percent_difference = abs(recent_average - older_average) / older_average

        if percent_difference <= 0.01:
            continue

        if older_average < recent_average:
            uptrend_count += 1
        elif older_average > recent_average:
            downtrend_count += 1

    total_comparisons = uptrend_count + downtrend_count

    if total_comparisons == 0:
        print(f"{SYMBOL} signal: sideways trend.")
    elif uptrend_count / total_comparisons >= 0.75:
        print(f"{SYMBOL} signal: moderate buy to strong buy.")
    elif downtrend_count / total_comparisons >= 0.75:
        print(f"{SYMBOL} signal: moderate sell to strong sell.")
    elif uptrend_count > downtrend_count:
        print(f"{SYMBOL} signal: sideways trend to moderate buy.")
    elif downtrend_count > uptrend_count:
        print(f"{SYMBOL} signal: sideways trend to moderate sell.")
    else:
        print(f"{SYMBOL} signal: sideways trend.")



    """ # Prints all moving averages for each period 
    print("\n***************** Moving Averages *****************")

    moving_averages = moving_average(SYMBOL)
    

    if not moving_averages:
        print(f"Not enough data to calculate moving averages for {SYMBOL}.")
    else:
        for days_count, average in moving_averages:
            print(f"{days_count}-day moving average: ${average:.2f}")

        average_values = [average for days_count, average in moving_averages]

        uptrend_count = 0
        downtrend_count = 0

        for i in range(len(average_values) - 1):
            older_average = average_values[i]
            recent_average = average_values[i + 1]
            percent_difference = abs(recent_average - older_average) / older_average

            if percent_difference <= 0.01:
                continue

            if older_average < recent_average:
                uptrend_count += 1
            elif older_average > recent_average:
                downtrend_count += 1

        total_comparisons = uptrend_count + downtrend_count

        if total_comparisons == 0:
            print(f"{SYMBOL} signal: sideways trend.")
        elif uptrend_count / total_comparisons >= 0.75:
            print(f"{SYMBOL} signal: moderate buy to strong buy.")
        elif downtrend_count / total_comparisons >= 0.75:
            print(f"{SYMBOL} signal: moderate sell to strong sell.")
        elif uptrend_count > downtrend_count:
            print(f"{SYMBOL} signal: sideways trend to moderate buy.")
        elif downtrend_count > uptrend_count:
            print(f"{SYMBOL} signal: sideways trend to moderate sell.")
        else:
            print(f"{SYMBOL} signal: sideways trend.")

    print("***************************************************\n")
    
    """