var INITIAL_VIEWPORT_STATE = {
  latitude: 37.78,
  longitude: -122.45,
  zoom: 13,
  pitch: 0,
  bearing: 10
};
var layers = [
  new ScatterplotLayer({
    updateTriggers: {},
    getPosition: function(x) {
      return [x.lng, x.lat];
    },
    getRadius: function(x) {
      return 100000.0;
    },
    data: [
      { lat: 37.6957743533, lng: -122.5394439697, city: "SF" },
      { lat: 37.8265990579, lng: -122.2874450684, city: "SF" },
      { lat: 36.0382725592, lng: -115.1940536499, city: "Las Vegas" },
      { lat: 33.408516828, lng: -112.1319580078, city: "Phoenix" },
      { lat: 18.9634415956, lng: -99.1845703125, city: "Ciudad de Mexico" },
      { lat: 41.5820659886, lng: -88.1597900391, city: "Chicago" },
      { lat: 40.7259253407, lng: -73.999786377, city: "New York" }
    ],
    getColor: function(x) {
      return [255, 127, 0];
    }
  })
];
var deckgl = new deck.DeckGL({
  container: "container",
  mapboxApiAccessToken: "pk.xxxxxxxxxxxxxxxxxxxx",
  viewState: INITIAL_VIEWPORT_STATE,
  controller: deck.MapController,
  onViewportChange: onViewportChange,
  layers: layers
});
function onViewportChange(viewport) {
  deckgl.setProps({ viewState: viewport });
}
