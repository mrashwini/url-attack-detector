// Project developed by Ashwini © 2025
// frontend/src/App.jsx
import { useState, useEffect } from "react";
import FilterPanel from "./components/FilterPanel";
import AttackTable from "./components/AttackTable";
import StatsPanel from "./components/StatsPanel";
import { queryAttacks, getCsvUrl, getJsonUrl, getStats } from "./api";

function App() {
  const [data, setData] = useState([]);
  const [stats, setStats] = useState(null);

  const handleSearch = async (filters) => {
    const res = await queryAttacks(filters);
    setData(res);
  };

  const loadStats = async () => {
    const s = await getStats();
    setStats(s);
  };

  useEffect(() => {
    handleSearch({});
    loadStats();
  }, []);

  // 🌟 UPDATED: Anime Background Added Here
  const appStyle = {
    minHeight: "100vh",
    margin: 0,
    padding: "3rem 2rem",
    backgroundImage:
      'linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url("/anime.jpg")',
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",
    backgroundAttachment: "fixed",
    color: "#f9fafb",
    fontFamily:
      "-apple-system, BlinkMacSystemFont, system-ui, -system-ui, 'Segoe UI', sans-serif",
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
  };

  const cardStyle = {
    width: "min(1400px, 96%)",
    margin: "1rem auto",
    background: "rgba(8, 12, 20, 0.9)",
    borderRadius: "16px",
    padding: "2rem",
    boxShadow: "0 24px 60px rgba(0,0,0,0.6)",
    border: "1px solid rgba(148, 163, 184, 0.12)",
  };

  const titleStyle = {
    fontSize: "2.25rem",
    fontWeight: 700,
    marginBottom: "1rem",
    textShadow: "0 3px 10px rgba(0,0,0,0.7)",
  };

  const exportBarStyle = {
    marginBottom: "1rem",
    display: "flex",
    gap: "1rem",
    alignItems: "center",
    fontSize: "1rem",
  };

  const exportLinkStyle = {
    color: "#38bdf8",
    textDecoration: "none",
    fontWeight: 500,
  };

  return (
    <div style={appStyle}>
      <div style={cardStyle}>
        <h1 style={titleStyle}>URL-based Attack Detection Dashboard</h1>

        {/* Charts */}
        <StatsPanel stats={stats} />

        {/* Filters + table */}
        <FilterPanel onSearch={handleSearch} />

        <div style={exportBarStyle}>
          <a href={getCsvUrl()} target="_blank" rel="noreferrer" style={exportLinkStyle}>
            Export CSV
          </a>
          <span>|</span>
          <a href={getJsonUrl()} target="_blank" rel="noreferrer" style={exportLinkStyle}>
            Export JSON
          </a>
        </div>

        <AttackTable data={data} />

        {/* 🌟 Added Signature  */}
        <div
          style={{
            marginTop: "2rem",
            textAlign: "center",
            fontSize: "0.85rem",
            opacity: 0.65,
          }}
        >
          © 2025 • Developed by <b>Ashwini</b>
        </div>
      </div>
    </div>
  );
}

export default App;
