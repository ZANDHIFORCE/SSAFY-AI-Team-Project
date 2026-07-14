<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const props = defineProps({
  places: { type: Array, default: () => [] },
});

const emit = defineEmits(["select-place"]);

const SEOUL_CENTER = [37.5665, 126.978];
const SEOUL_ZOOM = 12;

const mapEl = ref(null);
let map = null;
let markerLayer = null;
let hasFittedBounds = false;

function createPinIcon(postCount) {
  return L.divIcon({
    className: "map-pin",
    html: `<span class="map-pin__badge">${postCount ?? 0}</span>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -18],
  });
}

function renderMarkers() {
  if (!map || !markerLayer) return;
  markerLayer.clearLayers();

  const coords = [];

  props.places.forEach((place) => {
    if (typeof place.lat !== "number" || typeof place.lng !== "number") return;

    const marker = L.marker([place.lat, place.lng], {
      icon: createPinIcon(place.post_count),
      title: place.name,
    });

    marker.bindTooltip(
      `<strong>${place.name}</strong><br />게시글 ${place.post_count ?? 0}개`,
      { direction: "top", offset: [0, -14] },
    );

    marker.on("click", () => emit("select-place", place));
    markerLayer.addLayer(marker);
    coords.push([place.lat, place.lng]);
  });

  if (!hasFittedBounds && coords.length > 0) {
    hasFittedBounds = true;
    map.fitBounds(L.latLngBounds(coords), { padding: [32, 32], maxZoom: 13 });
  }
}

onMounted(() => {
  map = L.map(mapEl.value, {
    center: SEOUL_CENTER,
    zoom: SEOUL_ZOOM,
    zoomControl: true,
  });

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(map);

  markerLayer = L.layerGroup().addTo(map);
  renderMarkers();
});

watch(() => props.places, renderMarkers, { deep: true });

onBeforeUnmount(() => {
  if (map) {
    map.remove();
    map = null;
    markerLayer = null;
  }
});
</script>

<template>
  <div ref="mapEl" class="map-view"></div>
</template>

<style scoped>
.map-view {
  width: 100%;
  height: 100%;
}
</style>

<style>
/* Leaflet divIcon 커스텀 핀 — 이미지 에셋 대신 CSS 원형 핀 사용 */
.map-pin {
  background: transparent;
  border: none;
}

.map-pin__badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-primary);
  color: var(--color-on-primary);
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
  border: 2px solid var(--color-canvas);
}
</style>
