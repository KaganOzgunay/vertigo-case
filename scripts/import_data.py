#!/usr/bin/env python3
"""Script to import clan data from CSV file."""

import sys
import os
from datetime import datetime, timezone
from uuid import uuid4

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.clan import Clan


def parse_timestamp(value) -> datetime:
    """Parse timestamp from various formats."""
    if pd.isna(value) or value == "":
        return datetime.now(timezone.utc)

    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)

    try:
        if isinstance(value, str) and value.isdigit():
            return datetime.fromtimestamp(int(value), tz=timezone.utc)
    except (ValueError, OSError):
        pass

    try:
        dt = pd.to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return datetime.now(timezone.utc)


def import_clans(csv_path: str) -> dict:
    """Import clans from CSV file.

    Returns:
        dict with 'imported' and 'skipped' counts
    """
    Base.metadata.create_all(bind=engine)

    df = pd.read_csv(csv_path)

    db = SessionLocal()
    imported = 0
    skipped = 0

    try:
        for _, row in df.iterrows():
            name = row.get("name", "")

            if pd.isna(name) or str(name).strip() == "":
                skipped += 1
                continue

            region = row.get("region", "")
            if pd.isna(region):
                region = "UNKNOWN"

            created_at = parse_timestamp(row.get("created_at"))

            clan = Clan(
                id=str(uuid4()),
                name=str(name).strip(),
                region=str(region).strip(),
                created_at=created_at
            )
            db.add(clan)
            imported += 1

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return {"imported": imported, "skipped": skipped}


if __name__ == "__main__":
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "clan_sample_data.csv"
    )

    if len(sys.argv) > 1:
        csv_path = sys.argv[1]

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        sys.exit(1)

    print(f"Importing clans from: {csv_path}")
    result = import_clans(csv_path)
    print(f"Import complete: {result['imported']} imported, {result['skipped']} skipped")
