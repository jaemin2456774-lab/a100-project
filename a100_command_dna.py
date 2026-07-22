"""A100 V118 RC3.9 authoritative command inventory and Command DNA projection.

Read-only with respect to runtime/ledger/trading state. The module snapshots the
already-authoritative runtime registry and writes replaceable projection files.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Mapping

SCHEMA_VERSION = "a100.command.dna.v1"
INVENTORY_FILENAME = "a100_v118_command_inventory.json"
MATRIX_FILENAME = "a100_v118_certification_matrix_seed.json"


def _normalize(name: Any) -> str:
    return str(name or "").strip().lower().lstrip("/")


def _sha256_json(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        try:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
        except OSError:
            pass


def _category(command: str) -> str:
    groups = (
        ("IDENTITY", {"version", "buildinfo", "versionaudit", "status", "runtimehealth"}),
        ("CERTIFICATION", {"commandcert", "commandmatrix", "trustgate", "releasegate", "ltscertification", "regressionguard"}),
        ("PERFORMANCE", {"performance", "performancebudget", "perf", "latency", "commandperformance", "profiling"}),
        ("OPERATIONS", {"errors", "cache", "cachehealth", "apicheck", "health", "selfcheck"}),
        ("LEARNING", {"outcome", "attributioncheck", "attributiondebug", "calibration2", "champion", "closedloop", "coach"}),
        ("TRADING", {"coin", "chart", "check", "best", "bottom", "breakout85", "auto", "autotrack"}),
    )
    for category, names in groups:
        if command in names:
            return category
    if command.startswith(("paper", "shadow", "live", "trade", "entry", "close")):
        return "TRADING"
    if command.startswith(("ai", "intelligence", "news", "whale", "macro", "regime")):
        return "INTELLIGENCE"
    if command.startswith(("audit", "cert", "trust", "release", "regression")):
        return "CERTIFICATION"
    return "GENERAL"


def _owner(category: str) -> str:
    return {
        "IDENTITY": "RUNTIME",
        "CERTIFICATION": "CERTIFICATION",
        "PERFORMANCE": "PERFORMANCE",
        "OPERATIONS": "OPERATIONS",
        "LEARNING": "LEARNING",
        "TRADING": "TRADING",
        "INTELLIGENCE": "INTELLIGENCE",
    }.get(category, "PLATFORM")


def _callback_name(callback: Any) -> str:
    return str(getattr(callback, "__name__", type(callback).__name__))


def build_command_inventory(registry: Mapping[str, Callable[..., Any]], *, build_id: str, version: str) -> dict[str, Any]:
    if not isinstance(registry, Mapping):
        raise TypeError("registry must be a mapping")
    rows: list[dict[str, Any]] = []
    for index, (raw_name, callback) in enumerate(sorted(registry.items(), key=lambda item: _normalize(item[0])), start=1):
        command = _normalize(raw_name)
        category = _category(command)
        callable_ok = callable(callback)
        rows.append({
            "command_id": f"CMD-{index:03d}",
            "command": command,
            "owner": _owner(category),
            "category": category,
            "handler": _callback_name(callback),
            "handler_module": str(getattr(callback, "__module__", "")),
            "registered": True,
            "callable": callable_ok,
            "runtime": "PASS" if callable_ok else "FAILED",
            "evidence": "NOT_MEASURED",
            "output": "NOT_MEASURED",
            "storage": "NOT_APPLICABLE",
            "replay": "NOT_MEASURED",
            "performance": "NOT_MEASURED",
            "documentation": "NOT_MEASURED",
            "certification": "PARTIAL" if callable_ok else "FAILED",
            "reason": "authoritative_registry_callable_only" if callable_ok else "registered_handler_not_callable",
        })
    canonical = [{k: row[k] for k in ("command_id", "command", "handler", "owner", "category", "registered", "callable")} for row in rows]
    inventory_hash = _sha256_json(canonical)
    return {
        "schema": SCHEMA_VERSION,
        "generated_at": time.time(),
        "version": version,
        "build_id": build_id,
        "source": "V90_COMMAND_REGISTRY",
        "policy": "strict_read_only_projection; no ledger append; no synthetic PASS",
        "total": len(rows),
        "callable_handlers": sum(1 for row in rows if row["callable"]),
        "non_callable_handlers": sum(1 for row in rows if not row["callable"]),
        "inventory_hash": inventory_hash,
        "rows": rows,
    }


def export_authoritative_command_inventory(*, registry: Mapping[str, Callable[..., Any]], build_id: str, version: str, data_dir: str = "/data") -> dict[str, Any]:
    inventory = build_command_inventory(registry, build_id=build_id, version=version)
    base = Path(data_dir)
    inventory_path = base / INVENTORY_FILENAME
    matrix_path = base / MATRIX_FILENAME
    matrix = {
        "schema": "a100.certification.matrix.seed.v1",
        "generated_at": inventory["generated_at"],
        "version": version,
        "build_id": build_id,
        "inventory_hash": inventory["inventory_hash"],
        "total": inventory["total"],
        "dimensions": ["runtime", "evidence", "output", "storage", "replay", "performance", "documentation", "certification"],
        "rows": [{key: row[key] for key in ("command_id", "command", "runtime", "evidence", "output", "storage", "replay", "performance", "documentation", "certification", "reason")} for row in inventory["rows"]],
    }
    _atomic_json(inventory_path, inventory)
    _atomic_json(matrix_path, matrix)
    return {
        "ok": inventory["total"] == 341 and inventory["non_callable_handlers"] == 0,
        "total": inventory["total"],
        "callable_handlers": inventory["callable_handlers"],
        "non_callable_handlers": inventory["non_callable_handlers"],
        "inventory_hash": inventory["inventory_hash"],
        "inventory_path": str(inventory_path),
        "matrix_path": str(matrix_path),
    }
