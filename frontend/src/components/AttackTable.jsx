// AttackTable.jsx — full replacement
export default function AttackTable({ data }) {
  if (!data || data.length === 0) {
    return <div style={{ color: "#e5e7eb", padding: "1rem" }}>No results.</div>;
  }

  return (
    <div style={{ background: "rgba(2,6,23,0.5)", padding: "0.75rem", borderRadius: 10, marginTop: "1rem" }}>
      <table style={{
        width: "100%",
        color: "#e5e7eb",
        borderCollapse: "collapse",
        fontSize: "0.95rem"
      }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
            <th style={{ padding: "10px 12px" }}>ID</th>
            <th style={{ padding: "10px 12px" }}>Time</th>
            <th style={{ padding: "10px 12px" }}>Src IP</th>
            <th style={{ padding: "10px 12px" }}>Dst IP</th>
            <th style={{ padding: "10px 12px" }}>Method</th>
            <th style={{ padding: "10px 12px" }}>URL</th>
            <th style={{ padding: "10px 12px" }}>Attack Type</th>
            <th style={{ padding: "10px 12px" }}>Successful</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id} style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
              <td style={{ padding: "10px 12px" }}>{row.id}</td>
              <td style={{ padding: "10px 12px" }}>{new Date(row.timestamp).toLocaleString()}</td>
              <td style={{ padding: "10px 12px" }}>{row.src_ip}</td>
              <td style={{ padding: "10px 12px" }}>{row.dst_ip}</td>
              <td style={{ padding: "10px 12px" }}>{row.method}</td>
              <td style={{ padding: "10px 12px", maxWidth: 700, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{row.url}</td>
              <td style={{ padding: "10px 12px" }}>{row.attack_type}</td>
              <td style={{ padding: "10px 12px" }}>{row.is_successful ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
