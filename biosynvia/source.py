"""Fingerprint and inventory an archive without extracting or changing it."""

from collections import Counter
from datetime import datetime, timezone
import hashlib
from pathlib import Path, PurePosixPath
import re
import zipfile

from . import __version__


DATASET_DOI = "10.5281/zenodo.20829178"
DATASET_URL = "https://zenodo.org/records/20829178"
EXPECTED_MD5 = "71b2a35b7df2ed11644ec9f177453772"


def reconcile_structure(files: list[dict]) -> dict:
    """Reconcile source names; never infer grouping from observation row order."""
    workbook_pattern = re.compile(r"(EXP\d{3})_(batch|fed-batch)\.xlsx")
    csv_pattern = re.compile(r"(EXP\d{3})_(batch|fed-batch)_(R\d{2})_(inline|offline)\.csv")
    workbooks = {}
    aligned = {}
    errors = []
    for entry in files:
        name = PurePosixPath(entry["path"]).name
        workbook = workbook_pattern.fullmatch(name)
        table = csv_pattern.fullmatch(name)
        if workbook:
            experiment, mode = workbook.groups()
            key = experiment
            if key in workbooks:
                errors.append(f"Duplicate workbook for {experiment}.")
            workbooks[key] = mode
            entry.update(experiment_id=experiment, process_mode=mode, measurement_kind="workbook")
        elif table:
            experiment, mode, reactor, kind = table.groups()
            key = (experiment, reactor, kind)
            if key in aligned:
                errors.append(f"Duplicate aligned combination: {experiment}/{reactor}/{kind}.")
            aligned[key] = mode
            entry.update(experiment_id=experiment, process_mode=mode, reactor_id=reactor,
                         measurement_kind=kind)
        else:
            errors.append(f"Unrecognized source file: {entry['path']}.")
    expected_experiments = {f"EXP{index:03d}" for index in range(1, 13)}
    for experiment in sorted(expected_experiments - workbooks.keys()):
        errors.append(f"Missing workbook for {experiment}.")
    for experiment in sorted(workbooks.keys() - expected_experiments):
        errors.append(f"Unexpected workbook experiment: {experiment}.")
    expected_tables = {(experiment, reactor, kind) for experiment in expected_experiments
                       for reactor in ("R01", "R02") for kind in ("inline", "offline")}
    for key in sorted(expected_tables - aligned.keys()):
        errors.append(f"Missing aligned combination: {'/'.join(key)}.")
    for key in sorted(aligned.keys() - expected_tables):
        errors.append(f"Unexpected aligned combination: {'/'.join(key)}.")
    for (experiment, reactor, kind), mode in sorted(aligned.items()):
        if experiment in workbooks and mode != workbooks[experiment]:
            errors.append(f"Mode mismatch for {experiment}/{reactor}/{kind}.")
    modes = Counter(workbooks.values())
    if modes != {"batch": 9, "fed-batch": 3}:
        errors.append("Expected 9 batch and 3 fed-batch experiment workbooks.")
    return {"valid": not errors, "experiment_count": len(workbooks),
            "aligned_combination_count": len(aligned), "experiment_modes": dict(sorted(workbooks.items())),
            "mode_counts": dict(sorted(modes.items())), "errors": errors}


def inventory_archive(path: Path, expected_md5: str = EXPECTED_MD5) -> dict:
    md5 = hashlib.md5(usedforsecurity=False)
    sha256 = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            md5.update(chunk)
            sha256.update(chunk)
    actual = md5.hexdigest()
    if actual != expected_md5:
        raise ValueError(f"Archive checksum mismatch: expected {expected_md5}, got {actual}. No ingestion performed.")
    with zipfile.ZipFile(path) as archive:
        files = [{"path": entry.filename, "bytes": entry.file_size,
                  "compressed_bytes": entry.compress_size, "crc32": f"{entry.CRC:08x}"}
                 for entry in archive.infolist() if not entry.is_dir()]
    files.sort(key=lambda item: item["path"])
    counts = Counter(PurePosixPath(item["path"]).suffix.lower() for item in files)
    warnings = []
    if counts[".xlsx"] != 12:
        warnings.append(f"Expected 12 Excel workbooks; found {counts['.xlsx']}.")
    if counts[".csv"] != 48:
        warnings.append(f"Expected 48 aligned CSVs; found {counts['.csv']}.")
    names = [item["path"] for item in files]
    if len(names) != len(set(names)):
        warnings.append("Archive contains duplicate file paths.")
    if any(PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts or "\\" in name
           for name in names):
        warnings.append("Archive contains unsafe paths; do not extract them.")
    structure = reconcile_structure(files)
    if not structure["valid"]:
        warnings.append("Experiment/reactor/modality reconciliation failed; see experiment_structure.errors.")
    return {
        "schema_version": "0.1", "doi": DATASET_DOI, "source_url": DATASET_URL,
        "tool_version": __version__,
        "source_citation": "Uhlendorff, Fulek, Eimler, Pein-Hackelbusch and Frahm (2026). "
                           "Dataset Based on Chinese Hamster Ovary (CHO) Cultivations including "
                           "Turbidity, Permittivity, O2 and CO2 Measurements. Zenodo.",
        "retrieved_at_utc": None,
        "retrieval_time_status": "Exact retrieval event not recorded; local file modification time retained separately.",
        "archive_name": path.name, "bytes": path.stat().st_size,
        "expected_md5": expected_md5, "md5": actual, "sha256": sha256.hexdigest(),
        "checksum_verified": True,
        "manifest_created_at_utc": datetime.now(timezone.utc).isoformat(),
        "local_file_modified_at_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
        "license_status": "unresolved; no raw-data redistribution",
        "public_raw_data_distribution_allowed": False,
        "experiment_structure": structure,
        "counts_by_extension": dict(sorted(counts.items())), "files": files, "warnings": warnings,
        "limitations": ["Grouping is reconciled from filenames, not checked against workbook contents.",
                        "No observations, units, or time axes have been parsed.",
                        "Archive members were not extracted."],
    }
