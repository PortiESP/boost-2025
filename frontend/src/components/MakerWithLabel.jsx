import { useState } from "react"
import { Marker } from "react-simple-maps"

// A modular component for rendering a marker with a hoverable label
export function MarkerWithLabel(props) {
    const { marker } = props

    const [hovered, setHovered] = useState(false)

    return (
        <Marker 
            coordinates={marker.coordinates}
            // Set hovered state when mouse enters and leaves the marker
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
        >
            {/* Marker circle */}
            <circle r={marker.size} fill={marker.color} stroke="#fff" strokeWidth={2} />
            {/* Conditionally render label based on hover state */}
            {hovered && (
                <text
                    textAnchor="middle"
                    y={marker.size + 5}
                    style={{ fontFamily: "system-ui", fill: "#5D5A6D" }}
                >
                    {marker.label}
                </text>
            )}
        </Marker>
    )
}