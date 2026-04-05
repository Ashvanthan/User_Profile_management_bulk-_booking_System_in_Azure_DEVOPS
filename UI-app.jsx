import React, { useState } from "react";
import * as XLSX from "xlsx";

export default function App() {
  const [role, setRole] = useState("");
  const [page, setPage] = useState("dashboard");

  const [records, setRecords] = useState([]);
  const [duplicates, setDuplicates] = useState([]);

  // 📂 Handle file upload (CSV + Excel)
  const handleFiles = async (e) => {
    const files = e.target.files;
    let allData = [];

    for (let file of files) {
      const data = await file.arrayBuffer();
      const workbook = XLSX.read(data);
      const sheet = workbook.Sheets[workbook.SheetNames[0]];
      const json = XLSX.utils.sheet_to_json(sheet, { header: 1 });

      const values = json.flat().map(v => String(v).trim()).filter(v => v);
      allData = [...allData, ...values];
    }

    setRecords(allData);
  };

  // 🔍 Find duplicates
  const findDuplicates = () => {
    const seen = new Set();
    const dup = new Set();

    records.forEach((val) => {
      if (seen.has(val)) dup.add(val);
      else seen.add(val);
    });

    setDuplicates([...dup]);
  };

  // ❌ Remove duplicates (Privileged Admin only)
  const removeDuplicates = () => {
    const unique = [...new Set(records)];
    setRecords(unique);
    setDuplicates([]);
  };

  // 🎟️ Booking Page
  if (page === "booking") {
    return (
      <div style={styles.container}>
        <h2>🎟️ Booking Page</h2>
        <p>Booking system interface here...</p>
        <button onClick={() => setPage("dashboard")}>⬅ Back</button>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h1>📊 Booking Management System</h1>

      {/* ROLE SELECTION */}
      {!role && (
        <div>
          <button onClick={() => setRole("admin")}>👤 Admin</button>
          <button onClick={() => setRole("privileged")}>
            🔐 Privileged Admin
          </button>
        </div>
      )}

      {/* DASHBOARD */}
      {role && (
        <>
          <h2>
            {role === "admin"
              ? "👤 Admin Dashboard"
              : "🔐 Privileged Admin Dashboard"}
          </h2>

          {/* FILE UPLOAD */}
          <input
            type="file"
            multiple={role === "privileged"}
            accept=".csv,.xlsx"
            onChange={handleFiles}
          />

          <br />

          {/* ACTION BUTTONS */}
          <button onClick={findDuplicates}>🔍 Find Duplicates</button>

          {role === "privileged" && (
            <button onClick={removeDuplicates}>❌ Remove Duplicates</button>
          )}

          <button onClick={() => setPage("booking")}>
            ➡ Go to Booking Page
          </button>

          {/* RECORDS */}
          <h3>📋 Records:</h3>
          <ul>
            {records.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>

          {/* DUPLICATES */}
          <h3 style={{ color: "red" }}>⚠️ Duplicates:</h3>
          <ul>
            {duplicates.map((d, i) => (
              <li key={i}>{d}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

// 🎨 Styles
const styles = {
  container: {
    textAlign: "center",
    padding: "20px",
    fontFamily: "Arial",
  },
};
