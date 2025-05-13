import requests
import json
from datetime import datetime

url = "https://colintalkscrypto.com/cbbi/data/latest.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

# Prepare the response dictionary
response_data = {
    "data": [],
    "average_value": None,
    "latest_timestamp": None
}

if response.status_code == 200:
    data = response.json()

    values = []  # To store the latest values for averaging (excluding "Price")
    max_timestamp = 0  # To keep track of the latest (max) timestamp
    min_timestamp = float('inf')  # Initialize to positive infinity to track minimum timestamp

    for key in data:
        timestamp_keys = list(data[key].keys())  # Convert to a list to access the keys
        if timestamp_keys:
            # Ensure timestamps are treated as integers for comparison
            latest_timestamp = max(timestamp_keys, key=int)
            latest_timestamp = int(latest_timestamp)  # Make sure it's an integer
            latest_value = data[key].get(str(latest_timestamp))  # Access using string keys
            if latest_value is not None:
                date = datetime.fromtimestamp(latest_timestamp).strftime('%Y-%m-%d %H:%M')
                
                # Append the latest data to the response dictionary
                response_data["data"].append({
                    "key": key,
                    "date": date,
                    "latest_value": latest_value
                })
                
                # Exclude "Price" key from averaging
                if key != "Price":
                    values.append(latest_value)  # Store the value for averaging (excluding "Price")
                
                if latest_timestamp > max_timestamp:
                    max_timestamp = latest_timestamp  # Update the max timestamp if needed
                if latest_timestamp < min_timestamp:
                    min_timestamp = latest_timestamp  # Update the min timestamp if needed
            else:
                response_data["data"].append({
                    "key": key,
                    "date": None,
                    "latest_value": None
                })
        else:
            response_data["data"].append({
                "key": key,
                "date": None,
                "latest_value": None
            })
    
    if values:
        average_value = sum(values) / len(values)  # Calculate the average of the values (excluding "Price")
        response_data["average_value"] = round(average_value, 4)  # Store the average rounded to 4 decimal places
        
    # Store the latest (max) timestamp in a readable format
    if max_timestamp:
        max_date = datetime.fromtimestamp(max_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        response_data["latest_timestamp"] = max_date
    # Store the earliest (min) timestamp in a readable format
    if min_timestamp != float('inf'):
        min_date = datetime.fromtimestamp(min_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        response_data["earliest_timestamp"] = min_date

else:
    response_data["error"] = f"Failed to fetch data: {response.status_code}"

# Convert the response data to JSON format
response_json = json.dumps(response_data, indent=4)

# Print the result to simulate an API response
print(response_json)
