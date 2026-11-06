#!/usr/bin/env python3
"""Recompute bounded, same-run decision-support counts from frozen v6 tables.

This script is deliberately standard-library-only and performs no model fitting.
"""
import ast
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/processed/v6"
OUT = ROOT / "reports/scientific-closure"
MANIFEST_SHA256 = "d74465cbb353af872681cf3c6bbd1055ee0523441a889ec90832d7fc3affa45e"
INPUTS = ("assay_decisions.csv", "feature_lineage.csv", "time_policy.csv", "split_manifest.json")
AGES = (1, 5, 15)
REJECT_FLAGS = ("no_past_observation", "duplicate_source_time", "invalid_value",
                "status_value_blank", "status_not_ok", "past_only_derived_zero")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def truth(value):
    return str(value).strip().lower() == "true"


def number(value):
    return float(value) if value not in (None, "") else None


def read_csv(name):
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def core_fields():
    """Read CORE_FIELDS without importing preparation's optional dependencies."""
    tree = ast.parse((ROOT / "biosynvia/preparation.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CORE_FIELDS" for t in node.targets):
            fields = ast.literal_eval(node.value)
            if len(fields) != 8:
                raise ValueError("Expected eight producer CORE_FIELDS")
            return fields
    raise ValueError("CORE_FIELDS not found")


def assert_frozen(manifest):
    if digest(DATA / "stage12_manifest.json") != MANIFEST_SHA256:
        raise ValueError("v6 stage12 manifest hash differs from the supplied frozen hash")
    expected = manifest["outputs"]
    for name in INPUTS:
        actual = digest(DATA / name)
        if actual != expected[name]:
            raise ValueError(f"Frozen input hash mismatch: {name}")


def target_kind(assay):
    value = number(assay["VCD Mean (cells/mL)"])
    if value is None:
        return None
    if value > 0:
        return "positive"
    if value >= 0:
        return "recorded_nonnegative"
    return None


def eligible(row, age_minutes, status_policy):
    # Intentionally recompute from age_hours. The frozen fixed-5m `stale` flag is ignored.
    age = number(row["age_hours"])
    if age is None or age < 0 or age > age_minutes / 60 + 1e-10:
        return False
    if any(truth(row[name]) for name in REJECT_FLAGS):
        return False
    if status_policy == "strict_status" and truth(row["status_column_absent"]):
        return False
    return True


def count_assays(assays, rows_by_assay_field, fields, age, policy, label):
    retained = []
    for assay in assays:
        if target_kind(assay) is None:
            continue
        rows = [rows_by_assay_field.get((assay["assay_id"], field)) for field in fields]
        if all(row is not None and eligible(row, age, policy) for row in rows):
            if label == "positive" and target_kind(assay) != "positive":
                continue
            retained.append(assay)
    return retained


def partition(rows, key):
    return {name: len({r["assay_id"] for r in values})
            for name, values in sorted(group(rows, key).items())}


def group(rows, key):
    result = defaultdict(list)
    for row in rows:
        result[row[key]].append(row)
    return result


def write_csv(path, rows, columns):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def describe(rows):
    """Counts with the requested run, experiment, and split-group partitions."""
    return {"count": len(rows), "distinct_assay_ids": len({r["assay_id"] for r in rows}),
            "by_run": partition(rows, "run_id"), "by_experiment": partition(rows, "experiment_id"),
            "by_partition": partition(rows, "partition")}


def main():
    manifest = json.loads((DATA / "stage12_manifest.json").read_text(encoding="utf-8"))
    assert_frozen(manifest)
    split = json.loads((DATA / "split_manifest.json").read_text(encoding="utf-8"))
    experiment_partition = {row["experiment_id"]: row["partition"] for row in split["assignments"]}
    fields = core_fields()
    assays = read_csv("assay_decisions.csv")
    for assay in assays:
        assay["partition"] = experiment_partition[assay["experiment_id"]]
    lineage = read_csv("feature_lineage.csv")
    policy_rows = read_csv("time_policy.csv")
    # Same-run is enforced before any feature eligibility computation.
    assay_by_id = {row["assay_id"]: row for row in assays}
    lineage = [row for row in lineage if row["assay_id"] in assay_by_id and
               row["run_id"] == assay_by_id[row["assay_id"]]["run_id"]]
    by_assay_field = {(row["assay_id"], row["field"]): row for row in lineage}

    scenarios = (("five_core_strict_status", fields[:5], "strict_status"),
                 ("eight_core_status_absent_allowed", fields, "status_absent_allowed"),
                 ("eight_core_strict_status", fields, "strict_status"))
    count_rows, zero_rows, results = [], [], {}
    for scenario, selected, status_policy in scenarios:
        results[scenario] = {"fields": selected, "status_policy": status_policy, "ages_minutes": {}}
        for age in AGES:
            support = count_assays(assays, by_assay_field, selected, age, status_policy, "recorded_nonnegative")
            positive = count_assays(assays, by_assay_field, selected, age, status_policy, "positive")
            zero_candidates = [r for r in assays if target_kind(r) == "recorded_nonnegative"]
            retained_zero_ids = {r["assay_id"] for r in support if target_kind(r) == "recorded_nonnegative"}
            item = {"support": len(support), "positive": len(positive), "recorded_nonnegative_zero_challenge_total": len(zero_candidates),
                    "recorded_nonnegative_zero_challenge_retained": len(retained_zero_ids),
                    "distinct_assay_ids": {"support": len({r["assay_id"] for r in support}),
                                           "positive": len({r["assay_id"] for r in positive})},
                    "by_run": partition(support, "run_id"), "by_experiment": partition(support, "experiment_id"),
                    "by_partition": {"support": partition(support, "partition"), "positive": partition(positive, "partition")}}
            results[scenario]["ages_minutes"][str(age)] = item
            count_rows.append({"scenario": scenario, "age_minutes": age, "label_policy": "recorded_nonnegative",
                               "retained_assays": len(support), "distinct_assay_ids": len({r["assay_id"] for r in support}),
                               "by_run_json": json.dumps(item["by_run"], sort_keys=True),
                               "by_experiment_json": json.dumps(item["by_experiment"], sort_keys=True),
                               "by_partition_json": json.dumps(item["by_partition"]["support"], sort_keys=True)})
            count_rows.append({"scenario": scenario, "age_minutes": age, "label_policy": "target_positive",
                               "retained_assays": len(positive), "distinct_assay_ids": len({r["assay_id"] for r in positive}),
                               "by_run_json": json.dumps(partition(positive, "run_id"), sort_keys=True),
                               "by_experiment_json": json.dumps(partition(positive, "experiment_id"), sort_keys=True),
                               "by_partition_json": json.dumps(item["by_partition"]["positive"], sort_keys=True)})
            for r in zero_candidates:
                zero_rows.append({"scenario": scenario, "age_minutes": age, "assay_id": r["assay_id"], "run_id": r["run_id"],
                                  "experiment_id": r["experiment_id"], "time_hours": r["Time (h)"],
                                  "target_value": r["VCD Mean (cells/mL)"],
                                  "retained_in_support": r["assay_id"] in retained_zero_ids})

    # Evidence-informed cohort alternatives. These are masks, not source-data edits and
    # deliberately have no inferred onset-time rule.
    cohort_masks = {
        "retain_all_EXP011": lambda r: True,
        "quarantine_EXP011_R02": lambda r: r["run_id"] != "EXP011_R02",
        "quarantine_entire_EXP011": lambda r: r["experiment_id"] != "EXP011",
    }
    cohort_results = {}
    cohort_by_feature_family = {}
    feature_families = (("five_core_strict_status", fields[:5], "strict_status"),
                        ("eight_core_status_absent_allowed", fields, "status_absent_allowed"))
    zero_candidates = [r for r in assays if target_kind(r) == "recorded_nonnegative"]
    for family_name, selected, status_policy in feature_families:
        family_results = {}
        for cohort_name, include in cohort_masks.items():
            cohort_assays = [r for r in assays if include(r)]
            nominal_positive = [r for r in cohort_assays if target_kind(r) == "positive"]
            nominal_nonnegative = [r for r in cohort_assays if target_kind(r) is not None]
            entry = {"mask_rule": "cohort exclusion only; no time-onset threshold", "nominal": {
                "target_positive": describe(nominal_positive),
                "recorded_nonnegative": describe(nominal_nonnegative),
                "recorded_zero_challenge_cases": len([r for r in zero_candidates if include(r)])}, "ages_minutes": {}}
            for age in AGES:
                positive = count_assays(cohort_assays, by_assay_field, selected, age, status_policy, "positive")
                nonnegative = count_assays(cohort_assays, by_assay_field, selected, age, status_policy, "recorded_nonnegative")
                retained_zero_ids = {r["assay_id"] for r in nonnegative if target_kind(r) == "recorded_nonnegative"}
                entry["ages_minutes"][str(age)] = {"target_positive": describe(positive),
                    "recorded_nonnegative": describe(nonnegative),
                    "recorded_zero_challenge": {"total_in_cohort": len([r for r in zero_candidates if include(r)]),
                        "retained_in_support": len(retained_zero_ids)}}
                for label, rows in (("target_positive", positive), ("recorded_nonnegative", nonnegative)):
                    details = describe(rows)
                    count_rows.append({"scenario": f"joint_zero_positive_cohort_mask_{family_name}", "cohort_mask": cohort_name,
                    "age_minutes": age, "label_policy": label, "retained_assays": details["count"],
                    "distinct_assay_ids": details["distinct_assay_ids"],
                    "nominal_positive_denominator": len(nominal_positive),
                    "by_run_json": json.dumps(details["by_run"], sort_keys=True),
                    "by_experiment_json": json.dumps(details["by_experiment"], sort_keys=True),
                    "by_partition_json": json.dumps(details["by_partition"], sort_keys=True)})
                # Keep all original zero cases and annotate each mask once; never duplicate
                # EXP011_R02's five cases through a separate contamination subtraction.
                for r in zero_candidates:
                    zero_rows.append({"scenario": f"joint_zero_positive_cohort_mask_{family_name}", "cohort_mask": cohort_name,
                        "age_minutes": age, "assay_id": r["assay_id"], "run_id": r["run_id"],
                        "experiment_id": r["experiment_id"], "time_hours": r["Time (h)"],
                        "target_value": r["VCD Mean (cells/mL)"], "included_by_cohort_mask": include(r),
                        "retained_in_support": r["assay_id"] in retained_zero_ids})
            family_results[cohort_name] = entry
        cohort_by_feature_family[family_name] = family_results
        if family_name == "five_core_strict_status":
            cohort_results = family_results
    case_annotations = [{"assay_id": r["assay_id"], "run_id": r["run_id"], "experiment_id": r["experiment_id"],
                         "partition": r["partition"], "time_hours": r["Time (h)"], "target_class": target_kind(r),
                         "cohort_mask_inclusion": {name: include(r) for name, include in cohort_masks.items()}}
                        for r in assays]

    forecast = {}
    for horizon in (6, 12, 24):
        candidates = [r for r in assays if number(r["Time (h)"]) is not None and number(r["Time (h)"]) >= horizon]
        forecast[str(horizon)] = {"all_original_target_assays_upper_bound": len(candidates),
            "positive_target_assays_upper_bound": sum(target_kind(r) == "positive" for r in candidates),
            "origin_rule": "origin_hours = target_time_hours - horizon; exact future label only; no future inputs or interpolation",
            "limitation": "Upper bound only: raw snapshot extraction at each new origin is not implemented."}
    forecast_by_cohort = {}
    for cohort_name, include in cohort_masks.items():
        ceiling = {}
        for horizon in (6, 12, 24):
            candidates = [r for r in assays if include(r) and number(r["Time (h)"]) is not None and number(r["Time (h)"]) >= horizon]
            ceiling[str(horizon)] = {"all_original_target_assays_upper_bound": len(candidates),
                "positive_target_assays_upper_bound": sum(target_kind(r) == "positive" for r in candidates)}
        forecast_by_cohort[cohort_name] = {"origin_rule": "origin_hours = target_time_hours - horizon; exact future label only; no future inputs or interpolation",
            "limitation": "Upper bound only: raw snapshot extraction at each new origin is not implemented.", "ceilings": ceiling}

    endpoint = {}
    bounds = {}
    for run, rows in group(policy_rows, "run_id").items():
        bounds[run] = (min(number(r["aligned_first_hours"]) for r in rows),
                       max(number(r["aligned_last_hours"]) for r in rows))
    for label, predicate in (("all", lambda r: True), ("positive", lambda r: target_kind(r) == "positive")):
        covered = [r for r in assays if predicate(r) and r["run_id"] in bounds and
                   bounds[r["run_id"]][0] <= number(r["Time (h)"]) <= bounds[r["run_id"]][1]]
        endpoint[label] = {"count": len(covered), "by_run": partition(covered, "run_id"),
                           "by_experiment": partition(covered, "experiment_id")}

    OUT.mkdir(parents=True, exist_ok=True)
    counts_path, zeros_path, json_path = OUT / "counts-by-run.csv", OUT / "zero-case-support.csv", OUT / "decision-counts.json"
    write_csv(counts_path, count_rows, ("scenario", "cohort_mask", "age_minutes", "label_policy", "retained_assays", "distinct_assay_ids", "nominal_positive_denominator", "by_run_json", "by_experiment_json", "by_partition_json"))
    write_csv(zeros_path, zero_rows, ("scenario", "cohort_mask", "age_minutes", "assay_id", "run_id", "experiment_id", "time_hours", "target_value", "included_by_cohort_mask", "retained_in_support"))
    payload = {"purpose": "bounded scientific decision-count closure; no model fitting", "frozen_manifest_sha256": MANIFEST_SHA256,
               "source_hashes": {name: digest(DATA / name) for name in ("stage12_manifest.json", *INPUTS)},
               "method_hashes": {"script_sha256": digest(Path(__file__)), "preparation_py_sha256": digest(ROOT / "biosynvia/preparation.py")},
               "output_hashes": {"counts-by-run.csv": digest(counts_path), "zero-case-support.csv": digest(zeros_path)},
               "method": {"same_run_only": True, "ages_recomputed_from_age_hours": True, "frozen_stale_flag_ignored": True,
                          "rejection_flags": REJECT_FLAGS, "strict_status": "reject status-column-absent; reject blank/not-Ok statuses",
                          "status_absent_allowed": "allows only explicitly absent status columns; still rejects blank/not-Ok statuses"},
               "scenarios": results, "joint_zero_positive_cohort_masks": cohort_results,
               "cohort_counts_by_feature_family": cohort_by_feature_family,
               "case_annotations": {"description": "All original assay IDs retained; masks annotate inclusion only and do not alter frozen inputs.",
                                    "cases": case_annotations},
               "forecast_feasibility_upper_bounds": forecast, "forecast_feasibility_upper_bounds_by_cohort": forecast_by_cohort,
               "aligned_endpoint_coverage": {"definition": "Assay timestamp lies within publisher aligned start/end for its run.",
                                               "warning": "Endpoint coverage is not causal feature eligibility.", "counts": endpoint}}
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Bounded reconciliation checks requested for this frozen release.
    expected = {"five_core_strict_status": ((335, 339, 341), (330, 333, 335)),
                "eight_core_status_absent_allowed": ((335, 339, 341), (330, 333, 335)),
                "eight_core_strict_status": ((0, 0, 0), (0, 0, 0))}
    for scenario, (supports, positives) in expected.items():
        actual_supports = tuple(results[scenario]["ages_minutes"][str(age)]["support"] for age in AGES)
        actual_positives = tuple(results[scenario]["ages_minutes"][str(age)]["positive"] for age in AGES)
        if (actual_supports, actual_positives) != (supports, positives):
            raise AssertionError(f"Count reconciliation failed for {scenario}: {(actual_supports, actual_positives)}")
    if tuple(forecast[str(h)]["all_original_target_assays_upper_bound"] for h in (6, 12, 24)) != (352, 346, 322):
        raise AssertionError("Forecast all-target upper-bound reconciliation failed")
    if tuple(forecast[str(h)]["positive_target_assays_upper_bound"] for h in (6, 12, 24)) != (346, 340, 316):
        raise AssertionError("Forecast positive-target upper-bound reconciliation failed")
    if results["five_core_strict_status"]["ages_minutes"]["5"]["by_partition"]["positive"] != {"development": 258, "final_test_proposal": 75}:
        raise AssertionError("Five-minute positive development/reserved partition reconciliation failed")
    if sum(target_kind(r) == "recorded_nonnegative" for r in assays) != 6:
        raise AssertionError("Expected six recorded-zero target challenge cases")
    expected_cohorts = {"retain_all_EXP011": 333, "quarantine_EXP011_R02": 322, "quarantine_entire_EXP011": 308}
    for name, expected_positive in expected_cohorts.items():
        actual = cohort_results[name]["ages_minutes"]["5"]["target_positive"]["count"]
        if actual != expected_positive:
            raise AssertionError(f"Five-minute cohort-mask reconciliation failed for {name}: {actual}")
    expected_forecasts = {"retain_all_EXP011": ((346, 340, 316), (352, 346, 322)),
                          "quarantine_EXP011_R02": ((336, 330, 307), (337, 331, 308)),
                          "quarantine_entire_EXP011": ((321, 315, 293), (322, 316, 294))}
    for name, (positives, totals) in expected_forecasts.items():
        ceiling = forecast_by_cohort[name]["ceilings"]
        actual = (tuple(ceiling[str(h)]["positive_target_assays_upper_bound"] for h in (6, 12, 24)),
                  tuple(ceiling[str(h)]["all_original_target_assays_upper_bound"] for h in (6, 12, 24)))
        if actual != (positives, totals):
            raise AssertionError(f"Cohort forecast reconciliation failed for {name}: {actual}")
    for name in cohort_masks:
        for age in AGES:
            for label in ("target_positive", "recorded_nonnegative"):
                if cohort_by_feature_family["five_core_strict_status"][name]["ages_minutes"][str(age)][label]["count"] != cohort_by_feature_family["eight_core_status_absent_allowed"][name]["ages_minutes"][str(age)][label]["count"]:
                    raise AssertionError(f"Feature-family cohort reconciliation failed for {name}, {age}m, {label}")
    print(f"Wrote {json_path}, {counts_path}, and {zeros_path}; all reconciliation checks passed.")


if __name__ == "__main__":
    main()
