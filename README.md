# Apple Health Workout Parser

Parse your Apple Health `export.xml` and explore your workout history in an interactive dashboard.

## What It Does

- **`parse_workouts.py`** — extracts all workout records from Apple Health's `export.xml` into a clean CSV
- **`workout-dashboard.html`** — a self-contained visual dashboard for exploring that data (no server required)

## Requirements

- Python 3.7+
- No third-party libraries needed

## Usage

### Step 1 — Export your Apple Health data

On your iPhone: **Health → your profile photo → Export All Health Data**. This produces a zip file containing `export.xml`.

### Step 2 — Parse the export

```bash
python3 parse_workouts.py /path/to/export.xml workouts.csv
```

This generates a `workouts.csv` with these columns:

| Column | Description |
|---|---|
| `type` | Workout activity type (Running, Walking, Cycling, etc.) |
| `date` | Start date and time |
| `duration_min` | Duration in minutes |
| `distance_mi` | Distance in miles (blank if not recorded) |
| `calories` | Active calories burned (blank if not recorded) |

### Step 3 — Visualize in the dashboard

Open `workout-dashboard.html` in any browser. The dashboard includes:

- Total workouts, distance, calories, and time at a glance
- Weekly activity chart
- Workout type breakdown
- Filterable workout log

To load your own data, paste the contents of your `workouts.csv` into the `__csvData` variable at the top of the script block in `workout-dashboard.html`.

## Privacy Note

`workouts.csv` and `export.xml` are excluded from version control via `.gitignore`. Do not commit these files — they contain personal health data.

## Workout Types

Apple Health supports many workout types. Common ones you may see:

`Running` · `Walking` · `Cycling` · `Swimming` · `TraditionalStrengthTraining` · `HighIntensityIntervalTraining` · `CoreTraining` · `Tennis` · `Yoga` · and more.
