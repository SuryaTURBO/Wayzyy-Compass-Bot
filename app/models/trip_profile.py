from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class TripProfile:
    """Structured trip data, built up incrementally from conversation."""

    destination: Optional[str] = None
    start_date: Optional[str] = None       # ISO format, e.g. "2026-10-03"
    end_date: Optional[str] = None
    travellers: Optional[int] = None
    stay: Optional[str] = None             # e.g. "Candolim"
    budget: Optional[int] = None
    budget_type: Optional[str] = None      # "group" or "per_person"
    hotel_excluded: Optional[bool] = None
    diet: list[str] = field(default_factory=list)
    activities: list[str] = field(default_factory=list)
    nightlife: Optional[bool] = None
    max_travel_preference: Optional[str] = None  # "short", "medium", "far"
    skipped_fields: list[str] = field(default_factory=list)

    # Fields required before we can move to research/itinerary
    REQUIRED_FIELDS = [
        "destination", "start_date", "end_date", "travellers", "budget"
    ]

    # Optional preference fields — asked for, but don't block progress
    SOFT_FIELDS = ["stay", "diet", "activities", "nightlife"]

    def missing_fields(self) -> list[str]:
        """Which required fields are still unset."""
        data = asdict(self)
        return [f for f in self.REQUIRED_FIELDS if data.get(f) is None]

    def is_complete(self) -> bool:
        return len(self.missing_fields()) == 0

    def missing_soft_fields(self) -> list[str]:
        """Which optional preference fields are still unset (and not explicitly skipped)."""
        data = asdict(self)
        missing = []
        for f in self.SOFT_FIELDS:
            if f in self.skipped_fields:
                continue
            value = data.get(f)
            if value is None or value == []:
                missing.append(f)
        return missing

    def is_fully_gathered(self) -> bool:
        """True once both required and soft fields are captured."""
        return self.is_complete() and len(self.missing_soft_fields()) == 0

    def to_dict(self) -> dict:
        return asdict(self)
