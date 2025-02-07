import requests

BASE_URL = "http://127.0.0.1:2000"

# Fetch raw data
def fetch_raw_data():
    response = requests.get(f"{BASE_URL}/fetch-data")
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.text)
        return None

# Process data by sending it to API
def process_data():
    response = requests.post(f"{BASE_URL}/process-data")
    if response.status_code == 200:
        return response.json()
    else:
        print("Error processing data:", response.text)
        return None

# Retrieve processed data
def get_processed_data():
    response = requests.get(f"{BASE_URL}/get-processed-data")
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching processed data:", response.text)
        return None

if __name__ == "__main__":
    print("\nFetching raw data...")
    raw_data = fetch_raw_data()
    print(raw_data)

    print("\nProcessing data...")
    processed_data = process_data()
    print(processed_data)

    print("\nRetrieving processed data...")
    final_data = get_processed_data()
    print(final_data)
