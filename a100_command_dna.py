"""A100 V118 RC3.11 authoritative Command Health DNA v3 projection.

Strict read-only with respect to runtime, certification ledger, learning, and
trading state. This module mirrors already measured Certification SSOT fields
into a replaceable Command DNA projection. It never promotes a command by
registration alone and never appends certification events.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Mapping

SCHEMA_VERSION = "a100.command.dna.v3"
INVENTORY_FILENAME = "a100_v118_command_inventory.json"
MATRIX_FILENAME = "a100_v118_certification_matrix_seed.json"
CORE_REPORT_FILENAME = "a100_v118_core_command_linkage_report.json"
HEALTH_REPORT_FILENAME = "a100_v118_command_health_report.json"
DEFAULT_PROJECTION_FILENAME = "a100_v117_certification_projection.json"
CORE_PHASE_COMMANDS = (
    "version", "buildinfo", "versionaudit", "performance", "profiling",
    "commandcert", "commandmatrix", "trustgate", "intelligencescore", "errors",
)


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


def _read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def _category(command: str) -> str:
    groups = (
        ("IDENTITY", {"version", "buildinfo", "versionaudit", "status", "runtimehealth"}),
        ("CERTIFICATION", {"commandcert", "commandmatrix", "trustgate", "releasegate", "ltscertification", "regressionguard", "intelligencescore"}),
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


def _projection_rows(projection: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = projection.get("rows") if isinstance(projection, Mapping) else []
    return {
        _normalize(row.get("command")): row
        for row in (rows or [])
        if isinstance(row, dict) and _normalize(row.get("command"))
    }


def _status(value: Any, *, applicable: bool = True) -> str:
    if not applicable:
        return "NOT_APPLICABLE"
    return "PASS" if bool(value) else "NOT_MEASURED"




_HEALTH_WEIGHTS = {
    "runtime": 20,
    "evidence": 20,
    "output": 20,
    "storage": 10,
    "replay": 10,
    "performance": 10,
    "documentation": 10,
}

def _dimension_points(status: str, weight: int) -> float:
    value = str(status or "").upper()
    if value == "PASS":
        return float(weight)
    if value == "NOT_APPLICABLE":
        return float(weight)
    if value in {"PARTIAL", "MEASURED_PARTIAL"}:
        return float(weight) * 0.5
    return 0.0

def _health_profile(row: Mapping[str, Any]) -> dict[str, Any]:
    score = round(sum(_dimension_points(str(row.get(name)), weight) for name, weight in _HEALTH_WEIGHTS.items()), 2)
    blockers = [name for name in _HEALTH_WEIGHTS if str(row.get(name) or "").upper() not in {"PASS", "NOT_APPLICABLE"}]
    cert = str(row.get("certification") or "PARTIAL").upper()
    if cert == "FAILED" or not bool(row.get("callable")):
        risk = "CRITICAL"
    elif score < 40:
        risk = "HIGH"
    elif score < 75:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    phase_bonus = 30 if row.get("phase") == "CORE_PHASE_1" else 0
    impact_bonus = {"IDENTITY": 25, "CERTIFICATION": 25, "PERFORMANCE": 20, "OPERATIONS": 15, "TRADING": 10, "INTELLIGENCE": 10}.get(str(row.get("category")), 5)
    priority_score = min(100, int(round((100.0 - score) * 0.55 + phase_bonus + impact_bonus)))
    return {
        "health_score": score,
        "health_band": "HEALTHY" if score >= 90 else "DEVELOPING" if score >= 70 else "WEAK" if score >= 40 else "CRITICAL",
        "blockers": blockers,
        "next_transition": blockers[0] if blockers else "CERTIFIED",
        "risk": risk,
        "priority_score": priority_score,
    }


def build_command_inventory(
    registry: Mapping[str, Callable[..., Any]],
    *,
    build_id: str,
    version: str,
    certification_projection: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(registry, Mapping):
        raise TypeError("registry must be a mapping")
    measured_by_command = _projection_rows(certification_projection or {})
    rows: list[dict[str, Any]] = []
    for index, (raw_name, callback) in enumerate(sorted(registry.items(), key=lambda item: _normalize(item[0])), start=1):
        command = _normalize(raw_name)
        category = _category(command)
        callable_ok = callable(callback)
        measured = measured_by_command.get(command) or {}
        cert = str(measured.get("cert") or ("PARTIAL" if callable_ok else "FAILED"))
        state = str(measured.get("state") or ("REGISTERED" if callable_ok else "DISCOVERED"))
        reason = str(measured.get("reason") or ("authoritative_registry_callable_only" if callable_ok else "registered_handler_not_callable"))
        storage_applicable = bool(measured) or category in {"LEARNING", "TRADING", "CERTIFICATION", "OPERATIONS"}
        row = {
            "command_id": f"CMD-{index:03d}",
            "command": command,
            "owner": _owner(category),
            "category": category,
            "handler": _callback_name(callback),
            "handler_module": str(getattr(callback, "__module__", "")),
            "registered": True,
            "callable": callable_ok,
            "authoritative_route": callable_ok,
            "runtime": _status(measured.get("runtime")) if measured else ("PASS" if callable_ok else "FAILED"),
            "evidence": _status(measured.get("evidence")) if measured else "NOT_MEASURED",
            "output": _status(measured.get("output")) if measured else "NOT_MEASURED",
            "storage": _status(measured.get("store"), applicable=storage_applicable) if measured else ("NOT_MEASURED" if storage_applicable else "NOT_APPLICABLE"),
            "replay": _status(measured.get("replay")) if measured else "NOT_MEASURED",
            "performance": "NOT_MEASURED",
            "documentation": "NOT_MEASURED",
            "certification": cert,
            "certification_state": state,
            "reason": reason,
            "certification_source": "CERTIFICATION_SSOT_PROJECTION" if measured else "AUTHORITATIVE_REGISTRY",
            "certification_projection_hash": str((certification_projection or {}).get("projection_hash") or ""),
            "phase": "CORE_PHASE_1" if command in CORE_PHASE_COMMANDS else "BACKLOG",
        }
        row.update(_health_profile(row))
        rows.append(row)
    canonical = [{k: row[k] for k in (
        "command_id", "command", "handler", "owner", "category", "registered",
        "callable", "certification", "certification_state", "phase"
    )} for row in rows]
    inventory_hash = _sha256_json(canonical)
    counts = {name: sum(1 for row in rows if row["certification"] == name) for name in ("PASS", "PARTIAL", "FAILED")}
    return {
        "schema": SCHEMA_VERSION,
        "generated_at": time.time(),
        "version": version,
        "build_id": build_id,
        "source": "V90_COMMAND_REGISTRY + CERTIFICATION_SSOT_PROJECTION",
        "policy": "strict_read_only_projection; no ledger append; no synthetic PASS",
        "total": len(rows),
        "callable_handlers": sum(1 for row in rows if row["callable"]),
        "non_callable_handlers": sum(1 for row in rows if not row["callable"]),
        "counts": counts,
        "health": {
            "average": round(sum(float(row["health_score"]) for row in rows) / max(1, len(rows)), 2),
            "healthy": sum(1 for row in rows if row["health_band"] == "HEALTHY"),
            "developing": sum(1 for row in rows if row["health_band"] == "DEVELOPING"),
            "weak": sum(1 for row in rows if row["health_band"] == "WEAK"),
            "critical": sum(1 for row in rows if row["health_band"] == "CRITICAL"),
        },
        "inventory_hash": inventory_hash,
        "projection_hash": str((certification_projection or {}).get("projection_hash") or ""),
        "rows": rows,
    }


def export_authoritative_command_inventory(
    *,
    registry: Mapping[str, Callable[..., Any]],
    build_id: str,
    version: str,
    data_dir: str = "/data",
    certification_projection_path: str | None = None,
) -> dict[str, Any]:
    base = Path(data_dir)
    projection_path = Path(certification_projection_path) if certification_projection_path else base / DEFAULT_PROJECTION_FILENAME
    projection = _read_json(projection_path)
    inventory = build_command_inventory(
        registry,
        build_id=build_id,
        version=version,
        certification_projection=projection,
    )
    inventory_path = base / INVENTORY_FILENAME
    matrix_path = base / MATRIX_FILENAME
    core_report_path = base / CORE_REPORT_FILENAME
    health_report_path = base / HEALTH_REPORT_FILENAME
    matrix = {
        "schema": "a100.certification.matrix.seed.v2",
        "generated_at": inventory["generated_at"],
        "version": version,
        "build_id": build_id,
        "inventory_hash": inventory["inventory_hash"],
        "projection_hash": inventory["projection_hash"],
        "total": inventory["total"],
        "counts": inventory["counts"],
        "dimensions": ["runtime", "evidence", "output", "storage", "replay", "performance", "documentation", "certification"],
        "rows": [{key: row[key] for key in (
            "command_id", "command", "phase", "runtime", "evidence", "output",
            "storage", "replay", "performance", "documentation", "certification",
            "certification_state", "reason", "certification_source",
            "health_score", "health_band", "blockers", "next_transition",
            "risk", "priority_score"
        )} for row in inventory["rows"]],
    }
    core_rows = [row for row in inventory["rows"] if row["phase"] == "CORE_PHASE_1"]
    core_report = {
        "schema": "a100.command.dna.core.linkage.v1",
        "generated_at": inventory["generated_at"],
        "version": version,
        "build_id": build_id,
        "policy": "mirror measured SSOT only; no command execution; no certification mutation",
        "projection_hash": inventory["projection_hash"],
        "total": len(core_rows),
        "pass": sum(1 for row in core_rows if row["certification"] == "PASS"),
        "partial": sum(1 for row in core_rows if row["certification"] == "PARTIAL"),
        "failed": sum(1 for row in core_rows if row["certification"] == "FAILED"),
        "rows": core_rows,
    }
    priority_rows = sorted(inventory["rows"], key=lambda row: (-int(row["priority_score"]), str(row["command"])))
    health_report = {
        "schema": "a100.command.health.v1",
        "generated_at": inventory["generated_at"],
        "version": version,
        "build_id": build_id,
        "policy": "measured dimensions only; no synthetic PASS; strict read-only",
        "inventory_hash": inventory["inventory_hash"],
        "projection_hash": inventory["projection_hash"],
        "summary": inventory["health"],
        "top_priorities": [{key: row[key] for key in (
            "command", "category", "phase", "certification", "health_score",
            "health_band", "blockers", "next_transition", "risk", "priority_score"
        )} for row in priority_rows[:50]],
        "rows": [{key: row[key] for key in (
            "command_id", "command", "category", "phase", "certification",
            "health_score", "health_band", "blockers", "next_transition",
            "risk", "priority_score"
        )} for row in inventory["rows"]],
    }
    _atomic_json(inventory_path, inventory)
    _atomic_json(matrix_path, matrix)
    _atomic_json(core_report_path, core_report)
    _atomic_json(health_report_path, health_report)
    return {
        "ok": inventory["total"] == 341 and inventory["non_callable_handlers"] == 0,
        "total": inventory["total"],
        "callable_handlers": inventory["callable_handlers"],
        "non_callable_handlers": inventory["non_callable_handlers"],
        "counts": inventory["counts"],
        "core": {k: core_report[k] for k in ("total", "pass", "partial", "failed")},
        "health": inventory["health"],
        "top_priorities": [row["command"] for row in priority_rows[:10]],
        "inventory_hash": inventory["inventory_hash"],
        "projection_hash": inventory["projection_hash"],
        "inventory_path": str(inventory_path),
        "matrix_path": str(matrix_path),
        "core_report_path": str(core_report_path),
        "health_report_path": str(health_report_path),
    }
