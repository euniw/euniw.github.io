import React from 'react';
import Plot from 'react-plotly.js';

function DamageHeatmap({ data }) {
    if(!data || data.length === 0) {
        return null;
    }
    // Extract coordinate data
    const x_coords = data.map(d => d.x);
    const y_coords = data.map(d => d.y);
    const damage_coords = data.map(d => d.damage);

    const customData = data.map(d => [d.z, d.damage]);

    const plotData = [
        {
            x: x_coords,
            y: y_coords,
            z: damage_coords,
            type: 'heatmap',
            colorscale: 'Jet',
            colorbar: {
                title: 'Damage',
            },
        
            // Customize the hover text to show all four variables
            hovertemplate: 
                "Attack Points (x): %{x}<br>" +
                "Crit Rate Points (y): %{y}<br>" +
                "Crit Damage Points (z): %{customdata[0]}<br>" +
                "Damage: %{customdata[1]:.2f}<br>" +
                "<extra></extra>",
            customdata: customData, 
        },
    ];

    const plotLayout = {
        title: 'Damage Heatmap',
        xaxis: {
            title: 'Attack Points (x)',
            automargin: true,
        },
        yaxis: {
            title: 'Crit Rate Points (y)',
            automargin: true,
        },
    };

    return (
        <Plot
            data={plotData}
            layout={plotLayout}
            style={{ width: '100%', height: '500%'}}
            config={{ responsive: true}}
            />
    );
}

export default DamageHeatmap;