#!/usr/bin/env python3
"""
Parse Apple Health export.xml and extract Workout records to CSV.

Columns:
  type         - workout activity type (e.g. Running, Walking, Cycling)
  date         - start date of the workout
  duration_min - duration in minutes (rounded to 2 decimal places)
  distance_mi  - distance in miles from WorkoutStatistics (blank if not recorded)
  calories     - active energy burned in Cal from WorkoutStatistics (blank if not recorded)
"""

import csv
import xml.etree.ElementTree as ET
from pathlib import Path

INPUT_XML = Path("/Users/PhilSimon2/Desktop/apple_health_export/export.xml")
OUTPUT_CSV = Path("/Users/PhilSimon2/Desktop/workouts.csv")

# Map stat type identifiers to column names
STAT_MAP = {
    "HKQuantityTypeIdentifierActiveEnergyBurned": "calories",
    "HKQuantityTypeIdentifierDistanceWalkingRunning": "distance_mi",
    "HKQuantityTypeIdentifierDistanceCycling": "distance_mi",
    "HKQuantityTypeIdentifierDistanceSwimming": "distance_mi",
}

def clean_type(raw: str) -> str:
    """Strip the 'HKWorkoutActivityType' prefix for readability."""
    return raw.replace("HKWorkoutActivityType", "")

def main():
    rows = []
    workout_count = 0

    print(f"Parsing {INPUT_XML} — this may take a minute on a 2 GB file...")

    # Use both start and end events:
    #   - 'start' for Workout: capture its attributes before children are processed
    #   - 'end' for WorkoutStatistics: collect stats while still in the Workout subtree
    #   - 'end' for Workout: finalize the row and clear memory
    current_workout = None
    current_stats = {}

    context = ET.iterparse(INPUT_XML, events=["start", "end"])
    for event, elem in context:
        if event == "start" and elem.tag == "Workout":
            current_workout = dict(elem.attrib)
            current_stats = {}

        elif event == "end" and elem.tag == "WorkoutStatistics" and current_workout is not None:
            stat_type = elem.attrib.get("type", "")
            col = STAT_MAP.get(stat_type)
            if col and col not in current_stats:
                current_stats[col] = elem.attrib.get("sum", "")

        elif event == "end" and elem.tag == "Workout":
            if current_workout is not None:
                rows.append({
                    "type": clean_type(current_workout.get("workoutActivityType", "")),
                    "date": current_workout.get("startDate", ""),
                    "duration_min": round(float(current_workout.get("duration", 0)), 2),
                    "distance_mi": current_stats.get("distance_mi", ""),
                    "calories": current_stats.get("calories", ""),
                })
                workout_count += 1
                current_workout = None
                current_stats = {}
            elem.clear()

        elif event == "end" and elem.tag not in ("WorkoutStatistics", "WorkoutEvent", "WorkoutRoute", "MetadataEntry"):
            elem.clear()

    print(f"Found {workout_count} workouts. Writing CSV...")

    fieldnames = ["type", "date", "duration_min", "distance_mi", "calories"]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done. Saved to: {OUTPUT_CSV}")

    # Quick summary
    from collections import Counter
    types = Counter(r["type"] for r in rows)
    print("\nWorkout types found:")
    for wtype, cnt in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {wtype:30s} {cnt:5d}")

if __name__ == "__main__":
    main()
