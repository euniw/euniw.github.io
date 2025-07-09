import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';
import InputForm from './InputForm';
import ResultsDisplay from './ResultsDisplay';
import PresetsSelect from './PresetsSelect';
function App() {

  const REACT_APP_API_URL= "http://localhost:5000/api/calculate"
  const [inputs, setInputs] = useState({
    K: 1000, I: 10, F: 500, S: 50, CR0: 5, CD0: 50
  });
  const [results, setResults] = useState(null); // To store calculation results
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: value}));
  };

  // const handlePresetSelect = (presetValues) => {
  //   setInputs(presetValues);
  // };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission
    setError(null);
    setResults(null);

    // --- Core Logic for Processing Inputs before API Call ---
    const dataToSend = {};
    for (const key in inputs) {
      const value = inputs[key];
      const parsedValue = parseFloat(value);
 
      // If the value is an empty string or not a valid number, treat it as 0
      dataToSend[key] = isNaN(parsedValue) ? 0 : parsedValue;
    }
    console.log('Data being prepared to send:', dataToSend);

    try {
        const response = await axios.post(REACT_APP_API_URL, dataToSend);
        setResults(response.data);
    } catch (err) {
        console.error("Error calculating:", err.response ? err.response.data : err.message);
        setError(err.response ? err.response.data.error : "An unexpected error occurred.");
    }
  };

  return (
    <div className="App">
        <h1>Optimal Build Calculator</h1>
        {/* <PresetsSelect onSelectPreset={handlePresetSelect} /> */}
        <InputForm inputs={inputs} onInputChange={handleInputChange} onSubmit={handleSubmit} />
        {error && <div className="error-message">{error}</div>}
        {results && <ResultsDisplay results={results} />}
    </div>
  );
}

export default App;
