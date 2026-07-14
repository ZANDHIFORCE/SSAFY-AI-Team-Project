import { defineStore } from "pinia";
import { fetchPlaces } from "../api/places";

export const usePlacesStore = defineStore("places", {
  state: () => ({
    places: [],
    loading: false,
    error: null,
  }),
  getters: {
    topPlaces: (state) => (n) => state.places.slice(0, n),
  },
  actions: {
    async loadPlaces({ refresh = false } = {}) {
      if (this.places.length > 0 && !refresh) return;
      this.loading = true;
      this.error = null;
      try {
        this.places = await fetchPlaces();
      } catch (err) {
        this.error = err.detail ?? "장소 목록을 불러오지 못했습니다.";
      } finally {
        this.loading = false;
      }
    },
  },
});
