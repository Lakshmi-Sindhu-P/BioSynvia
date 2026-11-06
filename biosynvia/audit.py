"""Validate a provisional long-form CSV contract without altering source files."""

from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
from hashlib import sha256
import io
import math
from pathlib import Path


COLUMNS = ("experiment_id", "cultivation_id", "time_hours", "variable", "value", "unit")


@dataclass(frozen=True)
class Observation:
    experiment_id: str
    cultivation_id: str
    time_hours: float
    variable: str
    value: float | None
    unit: str


def read_table(path: Path, table: str) -> tuple[list[Observation], dict, list[dict]]:
    # Hash exactly the bytes parsed, so provenance cannot describe another read.
    raw = path.read_bytes()
    source = {"name": path.name, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)}
    issues = []
    rows = []

    def issue(line: int, code: str, message: str) -> None:
        issues.append({"table": table, "line": line, "code": code, "message": message})

    try:
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")), strict=True)
        if reader.fieldnames is None or len(reader.fieldnames) != len(set(reader.fieldnames)):
            issue(1, "header", "Headers must be present and unique.")
            return rows, source, issues
        if set(reader.fieldnames) != set(COLUMNS):
            issue(1, "header", f"Expected exactly these columns: {', '.join(COLUMNS)}")
            return rows, source, issues
        seen = set()
        units = {}
        last_times = {}
        for record in reader:
            line = reader.line_num
            if None in record or any(value is None for value in record.values()):
                issue(line, "row_width", "Row has too many or too few fields.")
                continue
            record = {key: value.strip() for key, value in record.items()}
            if any(not record[key] for key in COLUMNS if key != "value"):
                issue(line, "required", "Identifiers, time, variable, and unit must be present.")
                continue
            try:
                time = float(record["time_hours"])
                value = float(record["value"]) if record["value"] else None
            except ValueError:
                issue(line, "numeric", "Time and nonempty values must be numeric.")
                continue
            if not math.isfinite(time) or time < 0 or (value is not None and not math.isfinite(value)):
                issue(line, "numeric", "Time must be finite and nonnegative; values must be finite.")
                continue
            row = Observation(record["experiment_id"], record["cultivation_id"], time,
                              record["variable"], value, record["unit"])
            key = (row.cultivation_id, row.time_hours, row.variable)
            if key in seen:
                issue(line, "duplicate", "Duplicate cultivation/time/variable observation.")
            seen.add(key)
            if row.variable in units and units[row.variable] != row.unit:
                issue(line, "unit", f"Inconsistent units for {row.variable!r}; convert explicitly before import.")
            units[row.variable] = row.unit
            series = (row.cultivation_id, row.variable)
            if time < last_times.get(series, time):
                issue(line, "time_order", "Times must be nondecreasing within each cultivation/variable.")
            last_times[series] = time
            rows.append(row)
    except (UnicodeDecodeError, csv.Error) as exc:
        issue(0, "csv", f"Cannot parse UTF-8 CSV: {exc}")
    if not rows:
        issue(0, "empty", "No valid observations found.")
    return rows, source, issues


def summarize(rows: list[Observation]) -> dict:
    variables = defaultdict(list)
    for row in rows:
        variables[row.variable].append(row)
    summaries = {}
    for name, observations in sorted(variables.items()):
        present = [row for row in observations if row.value is not None]
        values = [row.value for row in present]
        summaries[name] = {
            "rows": len(observations), "nonmissing": len(present),
            "missing": len(observations) - len(present),
            "units": sorted({row.unit for row in observations}),
            "experiments_with_values": sorted({row.experiment_id for row in present}),
            "cultivations_with_values": sorted({row.cultivation_id for row in present}),
            "min": min(values) if values else None, "max": max(values) if values else None,
            "time_range_hours": [min(row.time_hours for row in observations),
                                 max(row.time_hours for row in observations)],
        }
    return {
        "rows": len(rows), "experiments": sorted({row.experiment_id for row in rows}),
        "cultivations": sorted({row.cultivation_id for row in rows}), "variables": summaries,
    }


def audit(sensors: Path, measurements: Path) -> dict:
    sensor_rows, sensor_source, sensor_issues = read_table(sensors, "sensors")
    measurement_rows, measurement_source, measurement_issues = read_table(measurements, "measurements")
    issues = sensor_issues + measurement_issues
    groups = defaultdict(set)
    for row in sensor_rows + measurement_rows:
        groups[row.cultivation_id].add(row.experiment_id)
    for cultivation, experiments in sorted(groups.items()):
        if len(experiments) != 1:
            issues.append({"table": "both", "line": None, "code": "group_conflict",
                           "message": f"Cultivation {cultivation!r} belongs to multiple experiments."})
    sensor_summary = summarize(sensor_rows)
    measurement_summary = summarize(measurement_rows)
    sensor_keys = {row.cultivation_id for row in sensor_rows}
    measurement_keys = {row.cultivation_id for row in measurement_rows}
    warnings = []
    if sensor_keys != measurement_keys:
        warnings.append("Cultivation coverage differs between sensors and measurements.")
    if any(row.value is None for row in sensor_rows + measurement_rows):
        warnings.append("Missing values exist; no imputation was performed.")
    if len({row.experiment_id for row in sensor_rows + measurement_rows}) < 2:
        warnings.append("At least two independent experiment groups are needed for a grouped holdout.")
    candidates = []
    earliest_sensor = {}
    for row in sensor_rows:
        if row.value is not None:
            earliest_sensor[row.cultivation_id] = min(
                earliest_sensor.get(row.cultivation_id, row.time_hours), row.time_hours)
    for variable, summary in measurement_summary["variables"].items():
        observations = [row for row in measurement_rows if row.variable == variable and row.value is not None]
        # Availability only: do not join to future sensors or claim feature completeness.
        with_prior = sum(earliest_sensor.get(row.cultivation_id, math.inf) <= row.time_hours
                         for row in observations)
        candidates.append({"variable": variable, "nonmissing": summary["nonmissing"],
                           "experiment_count": len(summary["experiments_with_values"]),
                           "cultivation_count": len(summary["cultivations_with_values"]),
                           "observations_with_any_sensor_at_or_before_time": with_prior,
                           "status": "requires_scientific_review"})
    counts = Counter(row.experiment_id for row in sensor_rows + measurement_rows)
    return {
        "schema_version": "0.1", "contract_status": "provisional",
        "software_version": "0.1.0", "valid": not issues,
        "sources": {"sensors": sensor_source, "measurements": measurement_source},
        "tables": {"sensors": sensor_summary, "measurements": measurement_summary},
        "cultivation_to_experiment": {key: next(iter(value)) for key, value in sorted(groups.items())
                                      if len(value) == 1},
        "observations_per_experiment": dict(sorted(counts.items())),
        "target_candidates": candidates if not issues else [],
        "errors": issues, "warnings": warnings,
        "limitations": ["No biological plausibility limits have been applied.",
                        "No model has been trained or scientifically validated.",
                        "Any prior sensor is only an availability check, not a usable feature set.",
                        "Targets require scientific review and confirmation against the source dataset."],
    }
