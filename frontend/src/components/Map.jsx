import { useState } from 'react';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import { MarkerWithLabel } from './MakerWithLabel';
import SearchBar from './SearchBar';

// URL for fetching map geography data
const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

// Main InteractiveMap component
export default function InteractiveMap({ markers }) {
    const [searchTerm, setSearchTerm] = useState('');

    const handleSearch = (term) => {
        setSearchTerm(term);
    };

    const filteredMarkers = markers.filter(marker =>
        marker.label.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
            <SearchBar onSearch={handleSearch} style={{
                position: 'absolute',
                top: '10px',
                left: '50%',
                transform: 'translateX(-50%)',
                zIndex: 10,
            }} />
            <ComposableMap
                projection="geoMercator"
                projectionConfig={{
                    center: [0, 40],
                    scale: 0,
                }}
                style={{ width: "100%", height: "100%" }}
            >
                <Geographies geography={geoUrl}>
                    {({ geographies }) =>
                        geographies.map(geo => (
                            <Geography
                                key={geo.rsmKey}
                                geography={geo}
                                style={{
                                    default: { fill: "#D6D6DA", outline: "none" },
                                    hover: { fill: "#F53", outline: "none" },
                                    pressed: { fill: "#E42", outline: "none" },
                                }}
                            />
                        ))
                    }
                </Geographies>
                {filteredMarkers.map((marker, index) => (
                    <MarkerWithLabel key={index} marker={marker} />
                ))}
            </ComposableMap>
        </div>
    );
}
