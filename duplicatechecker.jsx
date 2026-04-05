import React, { useState } from "react";

export default function DuplicateChecker() {
  const [input, setInput] = useState("");
  const [duplicates, setDuplicates] = useState([]);
  const [unique, setUnique] = useState([]);

  const findDuplicates = () => {
    const values = input.split(",").map(v => v.trim());
    const seen = new Set();
    const dup = new Set();

    values.forEach(val => {
      if (seen.has(val)) {
        dup.add(val);
      } else {
        seen.add(val);
      }
    });

    setDuplicates([...dup]);
    setUnique([...seen]);
  };

  return (
    <div className="container">
      <h2>🔍 Duplicate Record Finder</h2>

      <textarea
        placeholder="Enter values separated by commas (e.g., a,b,c,a,d)"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button onClick={findDuplicates}>Find Duplicates</button>

      <div className="results">
        <h3>✅ Unique Records:</h3>
        <ul>
          {unique.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>

        <h3>⚠️ Duplicate Records:</h3>
        <ul className="duplicates">
          {duplicates.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
