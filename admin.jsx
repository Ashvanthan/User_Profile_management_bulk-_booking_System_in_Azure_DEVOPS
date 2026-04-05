import React, { useState } from "react";

export default function AdminUI() {
  const [input, setInput] = useState("");
  const [duplicates, setDuplicates] = useState([]);

  const findDuplicates = () => {
    const values = input.split(",").map(v => v.trim());
    const seen = new Set();
    const dup = new Set();

    values.forEach(val => {
      if (seen.has(val)) dup.add(val);
      else seen.add(val);
    });

    setDuplicates([...dup]);
  };

  return (
    <div>
      <h2>👤 Admin Panel</h2>

      <textarea
        placeholder="Enter user emails"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <br />
      <button onClick={findDuplicates}>Check Duplicates</button>

      <h3>⚠️ Duplicates:</h3>
      <ul>
        {duplicates.map((d, i) => (
          <li key={i}>{d}</li>
        ))}
      </ul>
    </div>
  );
}
