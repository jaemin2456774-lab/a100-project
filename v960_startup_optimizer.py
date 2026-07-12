"""A100 V96.0 startup optimizer.
Pure helpers only: no network, no schema changes, no live trading.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from threading import Lock
from typing import Any, Callable, Dict, Optional


@dataclass
class StartupState:
    process_started_at: float
    health_started_at: float = 0.0
    telegram_started_at: float = 0.0
    background_started_at: float = 0.0
    warmup_finished_at: float = 0.0
    phase: str = "IMPORT"
    warmup_error: str = ""

    def snapshot(self) -> Dict[str, Any]:
        data = asdict(self)
        now = time.time()
        data["uptime_seconds"] = max(0.0, now - self.process_started_at)
        return data


class IncrementalFileCache:
    """Caches computed data until the backing file metadata changes."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._signature: Optional[tuple[int, int]] = None
        self._value: Any = None
        self.hits = 0
        self.misses = 0

    def get(self, signature: tuple[int, int], loader: Callable[[], Any]) -> Any:
        with self._lock:
            if self._signature == signature and self._value is not None:
                self.hits += 1
                return self._value
        value = loader()
        with self._lock:
            self._signature = signature
            self._value = value
            self.misses += 1
        return value

    def clear(self) -> None:
        with self._lock:
            self._signature = None
            self._value = None
