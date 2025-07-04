import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';
function App() {

  const REACT_APP_API_URL= "http://localhost:5000/api/calculate"
  const [inputs, setInputs] = useState({
    K: 1000, I: 10, F: 500, S: 50, CR0: 5, CD0: 50
  });
  const [results, setResults] = useState(null); // To store calculation results
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: parseFloat(value) || 0 }));
  };

  const handlePresetSelect = (presetValues) => {
    setInputs(presetValues);
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission
    setError(null);
    setResults(null);
    try {
        const response = await axios.post(REACT_APP_API_URL, inputs);
        setResults(response.data);
    } catch (err) {
        console.error("Error calculating:", err.response ? err.response.data : err.message);
        setError(err.response ? err.response.data.error : "An unexpected error occurred.");
    }
  };

  return (
    <div className="App">
        <h1>Optimal Build Calculator</h1>
        <PresetsSelect onSelectPreset={handlePresetSelect} />
        <InputForm inputs={inputs} onInputChange={handleInputChange} onSubmit={handleSubmit} />
        {error && <div className="error-message">{error}</div>}
        {results && <ResultsDisplay results={results} />}
    </div>
);
}

export default App;
