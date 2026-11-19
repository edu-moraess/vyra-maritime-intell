"""Stable initialization for Streamlit region selector widget state."""

from __future__ import annotations

from collections.abc import MutableMapping

from src.config.regions import REGION_OPTIONS, region_name_for_bbox
from src.config.settings import RegionBBox


def initialize_region_widget_state(
    state: MutableMapping[str, object],
    label: str,
    bbox: RegionBBox,
) -> None:
    """Initialize region widget keys once without overwriting operator edits.

    Streamlit reruns the script after widget interactions. Values already present
    in session state belong to the operator and must not be reset from the
    currently active engine configuration on subsequent reruns.
    """
    normalized_label = label.lower()
    selection_key = f"monitor_region_{normalized_label}"
    default_selection = region_name_for_bbox(bbox) or "Custom"

    if selection_key not in state or state[selection_key] not in REGION_OPTIONS:
        state[selection_key] = default_selection

    if state[selection_key] != "Custom":
        return

    coordinate_keys = (
        f"region_{normalized_label}_min_lat",
        f"region_{normalized_label}_min_lon",
        f"region_{normalized_label}_max_lat",
        f"region_{normalized_label}_max_lon",
    )
    (min_lat, min_lon), (max_lat, max_lon) = bbox
    defaults = (min_lat, min_lon, max_lat, max_lon)

    for key, value in zip(coordinate_keys, defaults):
        if key not in state:
            state[key] = float(value)
