// ResultsDisplay.js
import React from 'react';

function ResultsDisplay({ results }) {
  if (!results) return null; // Don't render if no results yet

  return (
    <div>
      <h2>Calculation Results</h2>
      <p>Optimal X: {results.optimal_x}</p>
      <p>Optimal Y: {results.optimal_y}</p>
      <p>Optimal Z: {results.optimal_z}</p>
      <p>Max Damage: {results.max_damage}</p>
    </div>
  );
}
export default ResultsDisplay;