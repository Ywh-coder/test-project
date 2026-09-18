import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "booking_data.json")


def load_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)
