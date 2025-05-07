import "./App.css";
import InteractiveMap from "./components/Map";
import storesData from "./data/stores.json";
import { useEffect, useState } from "react";

function App() {
  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    // Load store data from stores.json and transform it
    const transformedMarkers = storesData.map(store => ({
      label: store.country,
      coordinates: [store.longitude, store.latitude],
      size: 5,
      color: "#FF5533"
    }));
    setMarkers(transformedMarkers);
  }, []);

  return (
    <div className="wrapper">
      <div className="map-wrapper">
        <InteractiveMap markers={markers} />
      </div>
    </div>
  );
}

export default App
