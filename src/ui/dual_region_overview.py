"""Dual-region operational picture with isolated tactical views and selection state."""
from __future__ import annotations

from dataclasses import replace
from math import log2

import streamlit as st

from src.config.regions import format_bbox, region_name_for_bbox
from src.config.settings import AppSettings, RegionBBox
from src.geospatial.map_data import filter_rows_to_bboxes, live_vessel_rows, vessel_rows
from src.geospatial.region_membership import contains_point, belongs_to_any
from src.intelligence.engine import EngineSnapshot, MaritimeIntelligenceEngine
from src.ui import _pages_map_render as map_render
from src.ui.pages_overview import _render_environmental_context, _render_workspace_controls
from src.ui.pages_helpers import _render_vessel_map
from src.ui.presentation import render_ops_bar, render_region_comparison, render_regional_events
from src.ui.vessel_popup import render_vessel_quick_intelligence


def _in_bbox(latitude: float | None, longitude: float | None, bbox: RegionBBox) -> bool:
    return contains_point(latitude, longitude, bbox)


def _inside_bboxes(latitude: float | None, longitude: float | None, bboxes: tuple[RegionBBox, ...]) -> bool:
    return belongs_to_any(latitude, longitude, bboxes)


def _regional_snapshot(snapshot: EngineSnapshot, bbox: RegionBBox) -> EngineSnapshot:
    """Create a presentation-only snapshot containing only one operational area."""
    observations = [o for o in snapshot.observations if _in_bbox(o.latitude, o.longitude, bbox)]
    vessels = [v for v in snapshot.vessels if _in_bbox(v.latitude, v.longitude, bbox)]
    findings = [f for f in snapshot.findings if _in_bbox(f.latitude, f.longitude, bbox)]
    current_session_observations = [o for o in getattr(snapshot, "current_session_observations", []) if _in_bbox(o.latitude, o.longitude, bbox)]
    current_session_findings = [f for f in getattr(snapshot, "current_session_findings", []) if _in_bbox(f.latitude, f.longitude, bbox)]
    speeds = [float(o.sog_knots) for o in observations if o.sog_knots is not None]
    summary = dict(snapshot.summary)
    summary.update({"active_vessels": len(vessels), "messages": len(observations), "anomalies": len(findings), "average_speed_knots": (sum(speeds) / len(speeds)) if speeds else 0.0})
    return replace(snapshot, observations=observations, current_session_observations=current_session_observations, vessels=vessels, findings=findings, current_session_findings=current_session_findings, summary=summary)


def _unified_snapshot(snapshot: EngineSnapshot, bboxes: tuple[RegionBBox, ...]) -> EngineSnapshot:
    """Create a presentation-only A+B snapshot for every auxiliary map layer."""
    observations = [o for o in snapshot.observations if _inside_bboxes(o.latitude, o.longitude, bboxes)]
    vessels = [v for v in snapshot.vessels if _inside_bboxes(v.latitude, v.longitude, bboxes)]
    findings = [f for f in snapshot.findings if _inside_bboxes(f.latitude, f.longitude, bboxes)]
    current_session_observations = [o for o in getattr(snapshot, "current_session_observations", []) if _inside_bboxes(o.latitude, o.longitude, bboxes)]
    current_session_findings = [f for f in getattr(snapshot, "current_session_findings", []) if _inside_bboxes(f.latitude, f.longitude, bboxes)]
    speeds = [float(o.sog_knots) for o in observations if o.sog_knots is not None]
    summary = dict(snapshot.summary)
    summary.update({"active_vessels": len(vessels), "messages": len(observations), "anomalies": len(findings), "average_speed_knots": (sum(speeds) / len(speeds)) if speeds else 0.0})
    return replace(snapshot, observations=observations, current_session_observations=current_session_observations, vessels=vessels, findings=findings, current_session_findings=current_session_findings, summary=summary)


def _unified_bbox(bboxes: tuple[RegionBBox, ...]) -> RegionBBox:
    """Return one enclosing viewport without inventing a geographic midpoint."""
    return ((min(b[0][0] for b in bboxes), min(b[0][1] for b in bboxes)), (max(b[1][0] for b in bboxes), max(b[1][1] for b in bboxes)))


def _unified_map_zoom(
    rows: list[dict],
    bboxes: tuple[RegionBBox, ...] | None = None,
    *,
    min_zoom: float = 1.5,
    max_zoom: float = 9.0,
) -> float:
    """Choose a viewport scale from real targets or the monitored regions."""
    if rows:
        latitudes = [float(row["latitude"]) for row in rows]
        longitudes = [float(row["longitude"]) for row in rows]
        lat_span = max(latitudes) - min(latitudes)
        lon_span = max(longitudes) - min(longitudes)
    elif bboxes:
        (min_lat, min_lon), (max_lat, max_lon) = _unified_bbox(bboxes)
        lat_span = max_lat - min_lat
        lon_span = max_lon - min_lon
    else:
        return max(min_zoom, min(max_zoom, 5.0))
    span = max(float(lat_span), float(lon_span), 0.01)
    zoom = log2(360.0 / (span * 1.25))
    return max(min_zoom, min(max_zoom, zoom))


def _capture_region_selection(event, selection_key: str) -> None:
    """Store a contact selection in region-local state without touching global selection."""
    try:
        selection = event.selection if event is not None else None
        objects = selection.get("objects") if hasattr(selection, "get") else getattr(selection, "objects", None)
    except Exception:
        return
    if not isinstance(objects, dict):
        return
    layer_objects = objects.get(map_render.AIS_TARGETS_LAYER_ID) or objects.get("ais_targets")
    if not layer_objects:
        return
    first = layer_objects[0] if isinstance(layer_objects, list) and layer_objects else None
    if not isinstance(first, dict):
        return
    mmsi = first.get("mmsi") or first.get("tooltip_mmsi")
    if mmsi is None:
        return
    mmsi = str(mmsi).strip()
    if mmsi.isdigit() and len(mmsi) == 9 and st.session_state.get(selection_key) != mmsi:
        st.session_state[selection_key] = mmsi
        st.rerun()


def _selected_region_vessel(snapshot: EngineSnapshot, selection_key: str):
    """Resolve a selected contact only from the selection belonging to this region."""
    selected_mmsi = st.session_state.get(selection_key)
    if not selected_mmsi:
        return None
    return next((v for v in snapshot.vessels if str(v.mmsi) == str(selected_mmsi)), None)


def _render_map(label: str, bbox: RegionBBox, snapshot: EngineSnapshot, settings: AppSettings, controls, engine: MaritimeIntelligenceEngine, *, selection_key: str, map_key: str, show_contact_panel: bool = True):
    """Render one tactical map using isolated selection and widget state."""
    min_speed, include_stale, map_style, show_vectors, show_trails, show_behavior, show_hexbin, show_anomaly_types, show_freshness, show_anomaly_hotspots = controls
    region_snapshot = _regional_snapshot(snapshot, bbox)
    region_settings = replace(settings, bbox=bbox, monitoring_bboxes=(bbox,))
    rows = vessel_rows(region_snapshot.vessels) if include_stale else live_vessel_rows(region_snapshot.vessels)
    rows = filter_rows_to_bboxes(rows, (bbox,))
    region_selection = st.session_state.get(selection_key)
    if min_speed > 0:
        rows = [row for row in rows if row.get("sog_knots") is not None and float(row["sog_knots"]) >= min_speed]
    if region_selection and not include_stale:
        selected = next((v for v in region_snapshot.vessels if str(v.mmsi) == str(region_selection)), None)
        if selected is not None and _in_bbox(selected.latitude, selected.longitude, bbox):
            if not any(str(row.get("mmsi")) == str(region_selection) for row in rows):
                rows.append(vessel_rows([selected])[0])
    region_name = region_name_for_bbox(bbox) or label
    previous_global_selection = st.session_state.get("selected_mmsi")
    st.session_state.selected_mmsi = region_selection

    def _scoped_apply_selection(event) -> None:
        _capture_region_selection(event, selection_key)

    try:
        st.caption(f"{label} · {region_name} · {format_bbox(bbox)}")
        _render_vessel_map(
            rows,
            snapshot=region_snapshot,
            settings=region_settings,
            show_heading=show_vectors,
            show_trails=show_trails,
            show_anomalies=show_behavior,
            show_hexbin=show_hexbin,
            show_anomaly_types=show_anomaly_types,
            show_freshness=show_freshness,
            show_anomaly_hotspots=show_anomaly_hotspots,
            map_style=map_style,
            map_key=map_key,
            selection_handler=_scoped_apply_selection,
        )
    finally:
        st.session_state.selected_mmsi = previous_global_selection

    selected = _selected_region_vessel(region_snapshot, selection_key)
    if show_contact_panel and selected is not None:
        with st.container(key=f"tactical-contact-panel-{label.lower()}", border=True):
            render_vessel_quick_intelligence(selected, region_snapshot, show_gemini_hook=True, engine=engine)
    return selected, region_snapshot


def _unified_rows(snapshot: EngineSnapshot, bboxes: tuple[RegionBBox, ...], *, include_stale: bool, selected_mmsi: str | None) -> list[dict]:
    """Build unified targets without dropping the real operational picture on rerun."""
    rows = vessel_rows(snapshot.vessels) if include_stale else live_vessel_rows(snapshot.vessels)
    rows = filter_rows_to_bboxes(rows, bboxes)
    return rows


def _render_unified_map(bboxes: tuple[RegionBBox, ...], snapshot: EngineSnapshot, settings: AppSettings, controls, engine: MaritimeIntelligenceEngine, *, show_contact_panel: bool = True) -> None:
    """Render all monitored regions in one enclosing tactical viewport."""
    unified_bbox = _unified_bbox(bboxes)
    min_speed, include_stale, map_style, show_vectors, show_trails, show_behavior, show_hexbin, show_anomaly_types, show_freshness, show_anomaly_hotspots = controls
    unified_settings = replace(settings, bbox=unified_bbox, monitoring_bboxes=bboxes)
    unified_selection_key = "selected_mmsi_unified"
    unified_selection = st.session_state.get(unified_selection_key)
    unified_snapshot = _unified_snapshot(snapshot, bboxes)
    rows = _unified_rows(unified_snapshot, bboxes, include_stale=include_stale, selected_mmsi=unified_selection)
    if min_speed > 0:
        rows = [row for row in rows if row.get("sog_knots") is not None and float(row["sog_knots"]) >= min_speed]
    previous_global_selection = st.session_state.get("selected_mmsi")
    previous_zoom = st.session_state.get("tactical_map_zoom")
    st.session_state.selected_mmsi = unified_selection
    st.session_state.tactical_map_zoom = _unified_map_zoom(rows, bboxes)

    def _capture_unified_selection(event) -> None:
        try:
            selection = event.selection if event is not None else None
            objects = selection.get("objects") if hasattr(selection, "get") else getattr(selection, "objects", None)
        except Exception:
            return
        if not isinstance(objects, dict):
            return
        layer_objects = objects.get(map_render.AIS_TARGETS_LAYER_ID) or objects.get("ais_targets")
        first = layer_objects[0] if isinstance(layer_objects, list) and layer_objects else None
        if not isinstance(first, dict):
            return
        mmsi = first.get("mmsi") or first.get("tooltip_mmsi")
        if mmsi is not None and str(mmsi).strip().isdigit() and len(str(mmsi).strip()) == 9:
            st.session_state[unified_selection_key] = str(mmsi).strip()
            st.rerun()

    try:
        st.caption("UNIFIED · A + B · CONSOLIDATED OPERATIONAL PICTURE")
        _render_vessel_map(
            rows,
            snapshot=unified_snapshot,
            settings=unified_settings,
            show_heading=show_vectors,
            show_trails=show_trails,
            show_anomalies=show_behavior,
            show_hexbin=show_hexbin,
            show_freshness=show_freshness,
            show_anomaly_types=show_anomaly_types,
            show_anomaly_hotspots=show_anomaly_hotspots,
            map_style=map_style,
            map_key="operational_ais_map_unified",
            selection_handler=_capture_unified_selection,
        )
    finally:
        st.session_state.selected_mmsi = previous_global_selection
        if previous_zoom is None:
            st.session_state.pop("tactical_map_zoom", None)
        else:
            st.session_state.tactical_map_zoom = previous_zoom
    selected_mmsi = st.session_state.get(unified_selection_key)
    if show_contact_panel and selected_mmsi:
        selected = next((v for v in snapshot.vessels if str(v.mmsi) == str(selected_mmsi)), None)
        if selected is not None:
            with st.container(key="tactical-contact-panel-unified", border=True):
                render_vessel_quick_intelligence(selected, snapshot, show_gemini_hook=True, engine=engine)


def _render_context_panel(selected, snapshot: EngineSnapshot, engine: MaritimeIntelligenceEngine, label: str) -> None:
    """Render evidence-led vessel context beside the primary map."""
    st.markdown(
        "<div class='mie-context-head'><span>CONTACT INTELLIGENCE</span>"
        f"<span>{label}</span></div>",
        unsafe_allow_html=True,
    )
    if selected is None:
        st.markdown(
            "<div class='mie-context-empty'><strong>NO CONTACT SELECTED</strong>"
            "<span>Select a real AIS target on the map to inspect its identity, "
            "reported position, motion and available evidence.</span></div>",
            unsafe_allow_html=True,
        )
        st.caption("No target details are inferred when no contact is selected.")
        return
    render_vessel_quick_intelligence(selected, snapshot, show_gemini_hook=True, engine=engine)


def render_overview(engine: MaritimeIntelligenceEngine, snapshot: EngineSnapshot, settings: AppSettings) -> None:
    """Render the command-workstation layout while preserving dual-region semantics."""
    monitoring = tuple(settings.monitoring_bboxes)
    if not monitoring:
        monitoring = (settings.bbox,)
    summary = snapshot.summary
    region = "A + B" if len(monitoring) > 1 else (region_name_for_bbox(settings.bbox) or "CUSTOM")
    duration = f"Collection {snapshot.last_collection_seconds:.1f}s" if snapshot.last_collection_seconds > 0 else "Collection —"

    # Compact workstation chrome: operational state and real-session counters.
    st.markdown(
        """
        <style>
        .mie-workstation{border:1px solid #263746;background:linear-gradient(110deg,#111c27,#0b151e);
          padding:9px 12px;margin:4px 0 10px;display:flex;justify-content:space-between;
          align-items:center;gap:12px;flex-wrap:wrap}
        .mie-workstation .eyebrow,.mie-context-head{font:600 .62rem 'IBM Plex Mono',monospace;
          color:#8296a5;letter-spacing:.13em;text-transform:uppercase}
        .mie-workstation .metrics{display:flex;gap:20px;flex-wrap:wrap}
        .mie-workstation .metric b{display:block;font:600 .95rem 'IBM Plex Mono',monospace;color:#d9e4ea}
        .mie-workstation .metric small{font:500 .56rem 'IBM Plex Mono',monospace;color:#8296a5;text-transform:uppercase}
        .mie-workstation .source{font:500 .59rem 'IBM Plex Mono',monospace;color:#8296a5}
        .mie-context-head{display:flex;justify-content:space-between;border-bottom:1px solid #345064;
          padding:5px 0 9px;margin-bottom:9px}
        .mie-context-empty{border:1px dashed #345064;background:#0d1923;padding:16px 12px;
          display:flex;flex-direction:column;gap:8px;min-height:110px}
        .mie-context-empty strong{font:600 .68rem 'IBM Plex Mono',monospace;color:#d4a017}
        .mie-context-empty span{font-size:.78rem;line-height:1.5;color:#aab9c3}
        .mie-map-stage{border:1px solid #263746;background:#0b1219;padding:7px}
        @media(max-width:760px){.mie-workstation{align-items:flex-start}.mie-workstation .metrics{gap:12px}
          .mie-workstation .metric b{font-size:.82rem}}
        </style>
        """,
        unsafe_allow_html=True,
    )
    state = str(snapshot.status.state or "UNKNOWN").upper()
    render_ops_bar(
        live_state=state, region=region, vessels=summary["active_vessels"],
        messages=f"{summary['messages']:,}", anomalies=summary["anomalies"],
        collection=duration, provenance="REAL AIS · VERIFIED SOURCE",
        avg_speed=f"{summary['average_speed_knots']:.1f} kn",
        last_message=snapshot.status.last_received_at.strftime("%H:%M:%S UTC")
        if snapshot.status.last_received_at else "—",
    )
    controls = _render_workspace_controls(engine, settings)

    # Keep comparison and event data available, but move them below the live picture.
    if len(monitoring) >= 2:
        modes = ["A", "B", "UNIFIED", "SPLIT"]
        mode = st.segmented_control(
            "OPERATIONAL VIEW", options=modes, default="A",
            key="mie_command_view_mode", label_visibility="visible",
        )
    else:
        mode = "A"

    if mode == "SPLIT" and len(monitoring) >= 2:
        with st.container(key="mie-command-split"):
            col_a, col_b = st.columns(2, gap="small")
            with col_a:
                _render_map("A", monitoring[0], snapshot, settings, controls, engine,
                            selection_key="selected_mmsi_a", map_key="operational_ais_map_a")
            with col_b:
                _render_map("B", monitoring[1], snapshot, settings, controls, engine,
                            selection_key="selected_mmsi_b", map_key="operational_ais_map_b")
    else:
        selected = None
        context_snapshot = snapshot
        # Wide geospatial canvas with a persistent intelligence rail.
        # Streamlit columns stack naturally on narrow mobile viewports.
        map_col, context_col = st.columns([3.25, 1.15], gap="medium")
        if mode == "UNIFIED" and len(monitoring) >= 2:
            left_label = "A + B"
            context_snapshot = _unified_snapshot(snapshot, monitoring[:2])
            selected_mmsi = st.session_state.get("selected_mmsi_unified")
            selected = next((v for v in snapshot.vessels if str(v.mmsi) == str(selected_mmsi)), None)
            with map_col:
                with st.container(key="mie-command-map-stage", border=True):
                    _render_unified_map(monitoring[:2], snapshot, settings, controls, engine, show_contact_panel=False)
        else:
            idx = 1 if mode == "B" and len(monitoring) > 1 else 0
            left_label = "REGION B" if idx == 1 else "REGION A"
            bbox = monitoring[idx]
            with map_col:
                with st.container(key="mie-command-map-stage", border=True):
                    selected, context_snapshot = _render_map(
                        left_label, bbox, snapshot, settings, controls, engine,
                        selection_key="selected_mmsi_b" if idx == 1 else "selected_mmsi_a",
                        map_key="operational_ais_map_b" if idx == 1 else "operational_ais_map_a",
                        show_contact_panel=False,
                    )
        with context_col:
            _render_context_panel(selected, context_snapshot, engine, left_label)
            st.markdown("<div class='mie-context-head'>REGIONAL STATUS</div>", unsafe_allow_html=True)
            st.caption(f"Monitoring areas · {len(monitoring)}")
            for i, bbox in enumerate(monitoring[:2]):
                st.caption(f"{'A' if i == 0 else 'B'} · {format_bbox(bbox)}")
            st.caption("Position and movement fields are shown only when present in real AIS observations.")

    with st.expander("REGIONAL INTELLIGENCE · DERIVED", expanded=False):
        render_region_comparison(snapshot.region_comparison)
    with st.expander("INTELLIGENCE EVENT TIMELINE · REAL AIS / DERIVED", expanded=True):
        if snapshot.regional_events:
            render_regional_events(snapshot.regional_events)
        else:
            st.caption("No regional events are available in the current session.")
    _render_environmental_context(snapshot, monitoring)
    st.caption(
        "Operational picture derived from real AIS observations. Regional analysis remains "
        "separated in SPLIT and UNIFIED modes; unavailable observations are never replaced with zero-valued contacts."
    )

