
from pathlib import Path
import html
import math
import folium
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

# --------------------------------------------------
# Configuration and data
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "streetscape_hybrid.geojson"
IMAGE_DIR = ROOT / "data" / "processed" / "perspective_views"

st.set_page_config(
    page_title="Urban Streetscape Health Explorer",
    page_icon="🗺️",
    layout="wide",
)

@st.cache_data
def load_data():
    gdf = gpd.read_file(DATA_FILE).to_crs("EPSG:4326")
    assert len(gdf) == 100
    assert gdf["location_id"].nunique() == 50
    return gdf

data = load_data()
location_ids = sorted(data["location_id"].unique())

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("Urban Streetscape Health Explorer")
st.caption(
    "Amsterdam | An exploratory GeoAI prototype for "
    "interpretable streetscape assessment"
)

c1, c2, c3 = st.columns(3)
c1.metric("Sampled locations", data["location_id"].nunique())
c2.metric("Street views", len(data))
c3.metric("Visual indicators", 4)

st.divider()


# --------------------------------------------------
# Selected location and map-click handling
# --------------------------------------------------

if "selected_location" not in st.session_state:
    st.session_state.selected_location = sorted(
        data["location_id"].unique()
    )[0]

if "last_map_click" not in st.session_state:
    st.session_state.last_map_click = None


def nearest_location(lat, lon):
    """Return the nearest sampled location to a map click."""
    points = data.drop_duplicates("location_id")

    def distance_m(point):
        # Haversine distance in metres
        radius = 6_371_000
        lat1, lon1 = map(math.radians, [lat, lon])
        lat2, lon2 = map(
            math.radians,
            [point.geometry.y, point.geometry.x]
        )
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )
        return 2 * radius * math.asin(min(1, math.sqrt(a)))

    distances = points.apply(distance_m, axis=1)
    nearest = points.loc[distances.idxmin()]

    # Ignore clicks that are not close to a sampled marker.
    if distances.min() > 30:
        return None

    return nearest["location_id"]


# --------------------------------------------------
# Map
# --------------------------------------------------

map_col, detail_col = st.columns(
    [1.1, 1],
    gap="large"
)

with map_col:
    st.subheader("Explore Amsterdam")
    st.caption("Click a blue marker to inspect its street views.")

    center = [
        data.geometry.y.mean(),
        data.geometry.x.mean()
    ]

    m = folium.Map(
        location=center,
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    for location_id, group in data.groupby("location_id"):
        point = group.geometry.iloc[0]
        selected = (
            location_id == st.session_state.selected_location
        )

        folium.CircleMarker(
            location=[point.y, point.x],
            radius=9 if selected else 7,
            color="#ff9f1c" if selected else "#2374ab",
            weight=3 if selected else 2,
            fill=True,
            fill_opacity=0.95,
            tooltip=location_id,
        ).add_to(m)

    map_result = st_folium(
        m,
        height=650,
        width=None,
        returned_objects=["last_object_clicked"],
        key="interactive_streetscape_map",
    )

    clicked = map_result.get("last_object_clicked")

    if clicked:
        click_signature = (
            clicked["lat"],
            clicked["lng"]
        )

        if click_signature != st.session_state.last_map_click:
            st.session_state.last_map_click = click_signature

            location_id = nearest_location(
                clicked["lat"],
                clicked["lng"]
            )

            if (
                location_id is not None
                and location_id
                != st.session_state.selected_location
            ):
                st.session_state.selected_location = location_id
                st.rerun()


# --------------------------------------------------
# Location inspection panel
# --------------------------------------------------

with detail_col:
    selected_id = st.session_state.selected_location

    selected_views = (
        data[data["location_id"] == selected_id]
        .sort_values("image_id")
    )

    st.subheader(f"Location {selected_id}")
    st.caption("Two opposite street-level perspectives")

    view_a, view_b = st.columns(2, gap="medium")

    for column, (_, view) in zip(
        [view_a, view_b],
        selected_views.iterrows()
    ):
        with column:
            view_name = view["image_id"].split("_")[-1]
            st.markdown(f"#### View {view_name}")

            image_path = IMAGE_DIR / view["filename"]

            if image_path.is_file():
                st.image(
                    str(image_path),
                    use_container_width=True
                )
            else:
                st.warning("Image unavailable")

            st.markdown("**Visual indicators**")
            st.write(f"🌳 Greenery: **{view['greenery']}**")
            st.write(f"🚶 Pedestrian: **{view['pedestrian']}**")
            st.write(f"🚲 Cycling: **{view['cycling']}**")
            st.write(
                f"🚗 Motor vehicles: **{view['motor_vehicle']}**"
            )

            with st.expander("Cycling evidence"):
                st.write(view["cycling_evidence"])

# --------------------------------------------------
# Interpretation note
# --------------------------------------------------

st.info(
    "These labels describe visible streetscape characteristics "
    "in sampled images. They are not direct measurements of "
    "health outcomes, safety, or causal effects."
)

st.caption(
    "Street imagery: © City of Amsterdam, "
    "Kernregistratie Panoramabeelden (CC BY 4.0). "
    "Images reprojected, cropped and resized. "
    "Basemap: © OpenStreetMap contributors."
)