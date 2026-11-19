"""Regression tests for region widget state across Streamlit reruns."""

from __future__ import annotations

from src.config.regions import REGION_PRESETS
from src.ui.region_state import initialize_region_widget_state


def test_region_selection_survives_rerun_with_old_active_settings():
    state = {}
    active_bbox = REGION_PRESETS["Singapore"]

    initialize_region_widget_state(state, "a", active_bbox)
    assert state["monitor_region_a"] == "Singapore"

    # Streamlit writes the operator's selection before rerunning the script.
    state["monitor_region_a"] = "Malacca Strait"
    initialize_region_widget_state(state, "a", active_bbox)

    assert state["monitor_region_a"] == "Malacca Strait"


def test_custom_coordinates_are_initialized_once_and_preserved():
    state = {}
    active_bbox = REGION_PRESETS["Singapore"]

    initialize_region_widget_state(state, "a", active_bbox)
    state["monitor_region_a"] = "Custom"
    initialize_region_widget_state(state, "a", active_bbox)

    assert state["region_a_min_lat"] == float(active_bbox[0][0])
    assert state["region_a_min_lon"] == float(active_bbox[0][1])
    assert state["region_a_max_lat"] == float(active_bbox[1][0])
    assert state["region_a_max_lon"] == float(active_bbox[1][1])

    state["region_a_min_lat"] = 1.23456
    state["region_a_max_lon"] = 104.98765
    initialize_region_widget_state(state, "a", active_bbox)

    assert state["region_a_min_lat"] == 1.23456
    assert state["region_a_max_lon"] == 104.98765


def test_region_a_and_b_widget_state_are_independent():
    state = {}
    initialize_region_widget_state(state, "a", REGION_PRESETS["Singapore"])
    initialize_region_widget_state(state, "b", REGION_PRESETS["Malacca Strait"])

    assert state["monitor_region_a"] == "Singapore"
    assert state["monitor_region_b"] == "Malacca Strait"

    state["monitor_region_a"] = "Custom"
    initialize_region_widget_state(state, "a", REGION_PRESETS["Singapore"])

    assert state["monitor_region_b"] == "Malacca Strait"
    assert "region_a_min_lat" in state
    assert "region_b_min_lat" not in state
