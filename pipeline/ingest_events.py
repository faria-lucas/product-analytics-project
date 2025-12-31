import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


RAW_EVENTS_PATH = Path("data/raw/events.json")
OUTPUT_PATH = Path("data/parquet/events.parquet")


def load_events(path: Path) -> list[dict]:
    """Load raw events from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_event(event: dict) -> None:
    """Basic validation for required fields."""
    required_fields = ["event_id", "event_name", "event_time"]

    for field in required_fields:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    if not event.get("user_id") and not event.get("anonymous_id"):
        raise ValueError("Event must have user_id or anonymous_id")


def normalize_event(event: dict) -> dict:
    """Normalize event structure."""
    event_time = datetime.fromisoformat(
        event["event_time"].replace("Z", "+00:00")
    )

    user_key = event.get("user_id") or event.get("anonymous_id")

    return {
        "event_id": event["event_id"],
        "event_name": event["event_name"],
        "event_time": event_time,
        "user_id": event.get("user_id"),
        "anonymous_id": event.get("anonymous_id"),
        "user_key": user_key,
        "properties": json.dumps(event.get("properties", {})),
        "event_date": event_time.strftime("%Y-%m-%d"),
    }


def ingest_events():
    print("Loading raw events...")
    raw_events = load_events(RAW_EVENTS_PATH)

    normalized_events = []

    for event in raw_events:
        try:
            validate_event(event)
            normalized = normalize_event(event)
            normalized_events.append(normalized)
        except ValueError as e:
            # Simple handling: skip invalid events
            print(f"Skipping invalid event {event.get('event_id')}: {e}")

    if not normalized_events:
        raise RuntimeError("No valid events to ingest.")

    print(f"Valid events: {len(normalized_events)}")

    df = pd.DataFrame(normalized_events)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("Writing Parquet file...")
    table = pa.Table.from_pandas(df)
    pq.write_table(table, OUTPUT_PATH)

    print(f"Ingestion completed: {OUTPUT_PATH}")

    print("dataa", pd.read_parquet("/home/l-faria/workspaces/product-analytics-platform/data/parquet/events.parquet"))


if __name__ == "__main__":
    ingest_events()
