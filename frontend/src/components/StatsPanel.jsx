// frontend/src/components/StatsPanel.jsx
// Project Developed by Ashwini © 2025
// SOC-style Cybersecurity Dashboard with Attack Legend

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  LineChart,
  Line,
  Legend,
  ResponsiveContainer,
  Cell,
} from "recharts";

/* ---------------- Attack Type Color Legend ---------------- */
const AttackLegend = () => {
  const legendItems = [
    { label: "SQL Injection", color: "#f59e0b" },
    { label: "XSS", color: "#8b5cf6" },
    { label: "LFI / RFI", color: "#ef4444" },
    { label: "Directory Traversal", color: "#fb7185" },
    { label: "SSRF", color: "#22c55e" },
    { label: "Brute Force", color: "#38bdf8" },
  ];

  return (
    <div
      style={{
        minWidth: "220px",
        background: "rgba(10, 15, 25, 0.9)",
        border: "1px solid rgba(100,116,139,0.25)",
        borderRadius: "14px",
        padding: "1rem",
        marginRight: "1.5rem",
        boxShadow: "0 12px 30px rgba(0,0,0,0.4)",
      }}
    >
      <h4
        style={{
          marginBottom: "0.75rem",
          fontSize: "0.95rem",
          color: "#38bdf8",
          letterSpacing: "0.5px",
        }}
      >
        Attack Type Legend
      </h4>

      {legendItems.map((item) => (
        <div
          key={item.label}
          style={{
            display: "flex",
            alignItems: "center",
            marginBottom: "0.6rem",
            fontSize: "0.85rem",
            color: "#e5e7eb",
          }}
        >
          <span
            style={{
              width: "14px",
              height: "14px",
              backgroundColor: item.color,
              borderRadius: "4px",
              marginRight: "0.6rem",
              boxShadow: `0 0 8px ${item.color}66`,
            }}
          />
          {item.label}
        </div>
      ))}
    </div>
  );
};

export default function StatsPanel({ stats }) {
  if (!stats) return null;

  const { by_attack_type, by_src_ip, by_day } = stats;

  // ---- Styling ----
  const cardStyle = {
    background: "rgba(10, 15, 25, 0.85)",
    borderRadius: "14px",
    padding: "1rem 1.5rem",
    marginBottom: "1.75rem",
    boxShadow: "0 12px 35px rgba(0,0,0,0.45)",
    border: "1px solid rgba(100, 116, 139, 0.25)",
  };

  const sectionTitle = {
    marginBottom: "0.5rem",
    fontSize: "1rem",
    fontWeight: 600,
    color: "#f1f5f9",
    letterSpacing: "0.5px",
  };

  const gridColor = "rgba(148, 163, 184, 0.15)";
  const axisColor = "#94a3b8";
  const textColor = "#f8fafc";

  // ---- Attack Type → Color Mapping ----
  const attackColors = {
    SQL_INJECTION: "#f59e0b",
    XSS: "#8b5cf6",
    LFI_RFI: "#ef4444",
    DIRECTORY_TRAVERSAL: "#fb7185",
    SSRF: "#22c55e",
    BRUTE_FORCE: "#38bdf8",
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-start",
        marginBottom: "2rem",
      }}
    >
      {/* LEFT SIDE LEGEND */}
      <AttackLegend />

      {/* RIGHT SIDE CHARTS */}
      <div style={{ flex: 1 }}>
        <h2
          style={{
            fontSize: "1.35rem",
            marginBottom: "1rem",
            fontWeight: 700,
            color: "#38bdf8",
            textShadow: "0 0 12px rgba(56,189,248,0.6)",
          }}
        >
          Attack Statistics
        </h2>

        {/* -------- Attacks by Type -------- */}
        <div style={{ ...cardStyle, height: 260 }}>
          <h3 style={sectionTitle}>Attacks by Type</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={by_attack_type}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
              <XAxis dataKey="attack_type" stroke={axisColor} />
              <YAxis stroke={axisColor} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  border: "1px solid #38bdf8",
                  color: textColor,
                }}
              />
              <Legend />
              <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                {by_attack_type.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={attackColors[entry.attack_type] || "#64748b"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* -------- Top Source IPs -------- */}
        <div style={{ ...cardStyle, height: 260 }}>
          <h3 style={sectionTitle}>Top Source IPs</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={by_src_ip}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
              <XAxis dataKey="ip" stroke={axisColor} />
              <YAxis stroke={axisColor} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  border: "1px solid #22d3ee",
                  color: textColor,
                }}
              />
              <Legend />
              <Bar
                dataKey="count"
                fill="#22d3ee"
                radius={[6, 6, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* -------- Attack Timeline -------- */}
        <div style={{ ...cardStyle, height: 260 }}>
          <h3 style={sectionTitle}>Attack Timeline (per day)</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={by_day}>
              <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
              <XAxis dataKey="date" stroke={axisColor} />
              <YAxis stroke={axisColor} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  border: "1px solid #f59e0b",
                  color: textColor,
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="count"
                stroke="#f59e0b"
                strokeWidth={3}
                dot={{
                  r: 4,
                  stroke: "#fde68a",
                  strokeWidth: 1,
                  fill: "#f59e0b",
                }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
