import React from "react";

function InputForm({ inputs, onInputChange, onSubmit}){
    return(
        <form onSubmit={onSubmit}>
            {Object.keys(inputs).map(key => (
                <div key={key}>
                    <label>{key}:</label>
                    <input
                        type="number"
                        name={key}
                        value={inputs[key]}
                        onChange={onInputChange}
                        step="any"
                    />
                </div>
            ))}
            <button type="submit">Calculate</button>
        </form>
    );
}
export default InputForm;