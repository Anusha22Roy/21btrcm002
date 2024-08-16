import requests
import time
from flask import Flask, jsonify
from collections import deque

app = Flask(__name__)

window_size = 10
number_store = deque(maxlen=window_size)

def fetch_numbers(number_id):
    url = f"https://your-third-party-api/numbers/{number_id}"  # Replace with actual URL
    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
        return response.json()['numbers']
    except (requests.exceptions.RequestException, ValueError):
        return []

@app.route('/numbers/<number_id>')
def get_average(number_id):
    start_time = time.time()

    numbers = fetch_numbers(number_id)
    new_numbers = [num for num in numbers if num not in number_store]
    number_store.extend(new_numbers)

    prev_state = list(number_store)
    avg = sum(number_store) / len(number_store) if number_store else 0

    response = {
        "windowPrevState": list(number_store),
        "windowCurrState": list(number_store),
        "numbers": new_numbers,
        "avg": avg
    }

    end_time = time.time()
    print(f"Request processed in {end_time - start_time:.3f} seconds")

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)