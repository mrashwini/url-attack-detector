// frontend/src/components/FilterPanel.jsx
import { useState } from "react";

export default function FilterPanel({ onSearch }) {
  const [attackType, setAttackType] = useState("");
  const [srcIp, setSrcIp] = useState("");
  const [dstIp, setDstIp] = useState("");
  const [successfulOnly, setSuccessfulOnly] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({
      attack_type: attackType || null,
      src_ip: srcIp || null,
      dst_ip: dstIp || null,
      successful_only:
        successfulOnly === "" ? null : successfulOnly === "true",
    });
  };

  // FilterPanel.jsx — replace existing return JSX with this version
return (
  <form onSubmit={handleSubmit} style={{
      display: "flex",
      gap: "1rem",
      flexWrap: "wrap",
      marginBottom: "1rem",
      alignItems: "center"
    }}>
    <input
      placeholder="Attack type (SQL_INJECTION, XSS...)"
      value={attackType}
      onChange={(e) => setAttackType(e.target.value)}
      style={{ minWidth: 220, padding: "8px 10px", borderRadius: 6 }}
    />
    <input
      placeholder="Source IP"
      value={srcIp}
      onChange={(e) => setSrcIp(e.target.value)}
      style={{ minWidth: 180, padding: "8px 10px", borderRadius: 6 }}
    />
    <input
      placeholder="Destination IP"
      value={dstIp}
      onChange={(e) => setDstIp(e.target.value)}
      style={{ minWidth: 180, padding: "8px 10px", borderRadius: 6 }}
    />
    <select
      value={successfulOnly}
      onChange={(e) => setSuccessfulOnly(e.target.value)}
      style={{ padding: "8px 10px", borderRadius: 6 }}
    >
      <option value="">All</option>
      <option value="true">Successful only</option>
      <option value="false">Attempts only</option>
    </select>
    <button type="submit" style={{ padding: "8px 12px", borderRadius: 6 }}>Search</button>
  </form>
  );
}
