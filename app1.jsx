import React, { useState } from "react";
import AdminUI from "./AdminUI";
import PrivilegedAdminUI from "./PrivilegedAdminUI";

function App() {
  const [role, setRole] = useState("");

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>🔐 User Profile Management</h1>

      {!role && (
        <>
          <button onClick={() => setRole("admin")}>Admin</button>
          <button onClick={() => setRole("privileged")}>
            Privileged Admin
          </button>
        </>
      )}

      {role === "admin" && <AdminUI />}
      {role === "privileged" && <PrivilegedAdminUI />}
    </div>
  );
}

export default App;
