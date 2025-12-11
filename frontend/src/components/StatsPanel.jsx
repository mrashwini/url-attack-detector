// frontend/src/components/StatsPanel.jsx
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
} from "recharts";

export default function StatsPanel({ stats }) {
  if (!stats) return null;

  const { by_attack_type, by_src_ip, by_day } = stats;

  const cardStyle = {
    background: "rgba(15, 23, 42, 0.95)", // dark slate
    borderRadius: "12px",
    padding: "1rem 1.5rem",
    marginBottom: "1.5rem",
    boxShadow: "0 12px 30px rgba(0,0,0,0.4)",
    border: "1px solid rgba(148, 163, 184, 0.4)",
  };

  const sectionTitle = {
    marginBottom: "0.5rem",
    fontSize: "1rem",
    fontWeight: 600,
    color: "#e5e7eb",
  };

  return (
    <div style={{ marginBottom: "2rem" }}>
      <h2 style={{ fontSize: "1.25rem", marginBottom: "1rem" }}>
        Attack Statistics
      </h2>

      {/* Attacks by type */}
      <div style={{ ...cardStyle, height: 260 }}>
        <h3 style={sectionTitle}>Attacks by Type</h3>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={by_attack_type}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="attack_type" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip
              contentStyle={{ backgroundColor: "#020617", border: "1px solid #4f46e5", color: "#e5e7eb" }}
            />
            <Legend />
            <Bar dataKey="count" fill="#4f46e5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Top Source IPs */}
      <div style={{ ...cardStyle, height: 260 }}>
        <h3 style={sectionTitle}>Top Source IPs</h3>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={by_src_ip}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="ip" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip
              contentStyle={{ backgroundColor: "#020617", border: "1px solid #22c55e", color: "#e5e7eb" }}
            />
            <Legend />
            <Bar dataKey="count" fill="#22c55e" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Timeline */}
      <div style={{ ...cardStyle, height: 260 }}>
        <h3 style={sectionTitle}>Attack Timeline (per day)</h3>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={by_day}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="date" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip
              contentStyle={{ backgroundColor: "#020617", border: "1px solid #f97316", color: "#e5e7eb" }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="count"
              stroke="#f97316"
              strokeWidth={3}
              dot={{ r: 4, stroke: "#fed7aa", strokeWidth: 1, fill: "#f97316" }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
