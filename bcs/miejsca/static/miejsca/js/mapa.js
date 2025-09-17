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

  // Add "Pan to Current Location" button
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
        () => handleLocationError(true, infoWindow, map.getCenter())
      );
    } else {
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });

  // Load markers from Django JSON endpoint
  loadMarkers();
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

async function loadMarkers() {
  try {
    const response = await fetch("/miejsca/mapa/dane/");
    if (!response.ok) throw new Error("Network response was not ok");

    const miejsca = await response.json();

    const { Marker, InfoWindow } = google.maps;

    miejsca.forEach((m) => {
  const marker = new google.maps.Marker({
    position: { lat: m.latitude, lng: m.longitude },
    map,
    title: m.nazwa,
    icon: {
      url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="60" viewBox="0 0 24 24">
          <!-- red pin -->
          <path d="M12 2C8.1 2 5 5.1 5 9c0 5.3 7 13 7 13s7-7.7 7-13c0-3.9-3.1-7-7-7z" fill="#d00"/>
          <!-- emoji centered and scaled smaller -->
          <text x="12" y="10" font-size="8" text-anchor="middle" dominant-baseline="middle">${m.emoji}</text>
        </svg>
      `)}`,
      scaledSize: new google.maps.Size(50, 60),
    },
  });

  const markerInfoWindow = new google.maps.InfoWindow({
    content: `
      <div>
        <strong>${m.nazwa}</strong><br/>
        ${m.adres ? m.adres + "<br/>" : ""}
        Typ: ${m.typ || "N/A"}<br/>
        ${m.closed ? "<em>Closed permanently</em>" : ""}
      </div>
    `,
  });

  marker.addListener("click", () => {
    markerInfoWindow.open(map, marker);
  });
});


  } catch (error) {
    console.error("Error loading markers:", error);
  }
}

initMap();
