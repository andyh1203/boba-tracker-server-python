from datetime import datetime


def add_created_at_updated_at(data: dict):
    timestamp = datetime.now().isoformat()
    for timestamp_col in ("created_at", "updated_at"):
        data[timestamp_col] = timestamp
    return data
