import requests
import json
import time


def fetch_data(url):
    """Fetches data from the given URL and returns JSON response."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def transform_item(item):
    """Transforms a single item to the desired format with a unique millisecond timestamp ID."""
    # Generate a unique ID using current time in milliseconds
    # time.time_ns() gives nanoseconds, divide by 1,000,000 for milliseconds.
    new_id = str(int(time.time_ns() / 1_000_000))
    # Add a very brief sleep to help ensure unique timestamps if items are processed extremely rapidly.
    # This is a precaution; time_ns() offers high resolution.
    time.sleep(0.001)  # Sleep for 1 millisecond
    return {
        "title": item.get("name"),
        "content": item.get("ch") or item.get("en"),
        "category": item.get("categorie"),
        "id": new_id
    }


def transform_data(data):
    """Transforms the fetched data, keeping only 'name' (as 'title') and 'ch' (as 'content')."""
    if not data or "items" not in data or not isinstance(data["items"], list):
        print("No items found in data or data format is incorrect.")
        return []

    transformed_list = []
    for item in data["items"]:
        print(f"prompt is: {item}")
        if isinstance(item, dict):
            transformed_list.append(transform_item(item))
        else:
            print(f"Skipping invalid item: {item}")
    return transformed_list


def save_to_json_file(data, filename):
    """Saves the given data to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved transformed data to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")


if __name__ == '__main__':
    API_URL = "https://api-prompt.leops.cn/api/prompt?page=1&limit=10000&sort=new"
    OUTPUT_FILENAME = "transformed_prompts.json"

    print(f"Attempting to fetch data from: {API_URL}")
    raw_data = fetch_data(API_URL)

    if raw_data:
        print("Data fetched successfully. Starting transformation...")
        transformed_data = transform_data(raw_data)
        if transformed_data:
            print("Data transformed successfully. Saving to file...")
            save_to_json_file(transformed_data, OUTPUT_FILENAME)
        else:
            print("Transformation resulted in empty data. Nothing to save.")
    else:
        print("Failed to fetch data. Please check the URL and your network connection.")

# To run this script, ensure you have the 'requests' library installed:
# pip install requests
