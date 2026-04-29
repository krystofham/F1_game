import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import './index.css'

async function getFullState() {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/get_state");
    return await response.json();
  } catch (err) {
    console.error("Server spí:", err);
    return null;
  }
}

function Team({ data }) {
  return (
    <div className="team-card">
      <h2>{data.name}</h2>
      <ul>
        {data.drivers.map((d, i) => <li key={i}>{d}</li>)}
      </ul>
      <p>Body: {data.points}</p>
    </div>
  )
}

function Player({ data }) {
  return (
    <div className='player-card'>
      <h2>{data.name}</h2>
      <p>
        Points: {data.points} <br />
        Team: {data.team || "Neznámý"}
      </p>
    </div>
  )
}

export function Teams() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getFullState().then(res => setData(res));
  }, []);
  if (!data) return <div>Načítám týmy...</div>;
  return (
    <>
      <h1>Týmy</h1>
      {data.teams.map((teamData, index) => (
        <Team key={index} data={teamData} />
      ))}
    </>
  );
}

export function Players() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getFullState().then(res => setData(res));
  }, []);
  if (!data) return <div>Načítám jezdce...</div>;
  return (
    <>
      <h1>Jezdci</h1>
      {data.drivers.map((driversData, index) => (
        <Player key={index} data={driversData} />
      ))}
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: "20px", background: "#eee", marginBottom: "10px" }}>
        <Link to="/">Týmy</Link> | <Link to="/players">Jezdci</Link>
      </nav>
      <div style={{ padding: "20px" }}>
        <Routes>
          <Route path="/" element={<Teams />} />
          <Route path="/players" element={<Players />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}