let map, infoWindow;

async function initMap() {
  // Import the needed library
  const { Map, InfoWindow, Marker } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 }, // default center
    zoom: 6,
    gestureHandling: "greedy",
  });

  infoWindow = new InfoWindow();

  const locationButton = document.createElement("button");
  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

  locationButton.addEventListener("click", () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          infoWindow.setPosition(pos);
          infoWindow.setContent("Location found.");
          infoWindow.open(map);

          // Pan and zoom into street level
          map.setCenter(pos);
          map.setZoom(17); // street-level zoom
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        },
        {
          enableHighAccuracy: true, // optional, gets better GPS on mobile
          timeout: 10000,
          maximumAge: 0,
        }
      );
    } else {
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}

initMap();
