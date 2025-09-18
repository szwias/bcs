(function (config) {
  const apiName = "The Google Maps JavaScript API";
  const googleNamespace = "google";
  const importLibraryMethod = "importLibrary";
  const importCallback = "__ib__";
  const documentRef = document;
  const windowRef = window;

  windowRef[googleNamespace] = windowRef[googleNamespace] || {};
  const mapsNamespace =
    windowRef[googleNamespace].maps || (windowRef[googleNamespace].maps = {});

  let scriptPromise, scriptElement, paramKey;
  const requestedLibraries = new Set();
  const urlParams = new URLSearchParams();

  const loadScript = () =>
    scriptPromise ||
    (scriptPromise = new Promise(async (resolve, reject) => {
      scriptElement = documentRef.createElement("script");
      urlParams.set("libraries", [...requestedLibraries] + "");

      for (paramKey in config) {
        urlParams.set(
          paramKey.replace(/[A-Z]/g, (t) => "_" + t[0].toLowerCase()),
          config[paramKey]
        );
      }

      urlParams.set("callback", googleNamespace + ".maps." + importCallback);
      scriptElement.src =
        `https://maps.${googleNamespace}apis.com/maps/api/js?` + urlParams;
      mapsNamespace[importCallback] = resolve;

      scriptElement.onerror = () => {
        scriptPromise = reject(Error(apiName + " could not load."));
      };

      scriptElement.nonce =
        documentRef.querySelector("script[nonce]")?.nonce || "";

      documentRef.head.append(scriptElement);
    }));

  if (mapsNamespace[importLibraryMethod]) {
    console.warn(apiName + " only loads once. Ignoring:", config);
  } else {
    mapsNamespace[importLibraryMethod] = (library, ...args) =>
      requestedLibraries.add(library) &&
      loadScript().then(() =>
        mapsNamespace[importLibraryMethod](library, ...args)
      );
  }
})({
  key: GOOGLE_MAPS_API_KEY, // injected from template
  v: "weekly",
  language: "pl",
  region: "PL",
});
