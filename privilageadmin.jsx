import React, { useState } from "react";

export default function PrivilegedAdminUI() {
  const [input, setInput] = useState("");
  const [records, setRecords] = useState([]);
  const [duplicates, setDuplicates] = useState([]);

  const processData = () => {
    const values = input.split(",").map(v => v.trim());
    const seen = new Set();
    const dup = new Set();

    values.forEach(val => {
      if (seen.has(val)) dup.add(val);
      else seen.add(val);
    });

    setRecords(values);
    setDuplicates([...dup]);
  };

  const removeDuplicates = () => {
    const unique = [...new Set(records)];
    setRecords(unique);
    setDuplicates([]);
  };

  return (
    <div>
      <h2>🔐 Privileged Admin Panel</h2>

      <textarea
        placeholder="Enter user emails"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <br />
      <button onClick={processData}>Analyze</button>
      <button onClick={removeDuplicates}>Remove Duplicates</button>

      <h3>📋 All Records:</h3>
      <ul>
        {records.map((r, i) => (
          <li key={i}>{r}</li>
        ))}
      </ul>

      <h3>⚠️ Duplicate Records:</h3>
      <ul style={{ color: "red" }}>
        {duplicates.map((d, i) => (
          <li key={i}>{d}</li>
        ))}
      </ul>
    </div>
  );
}
