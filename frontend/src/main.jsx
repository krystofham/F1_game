import { StrictMode, useState, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'




export async function getFullState() {
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
        <li>{data.drivers[0]}</li>
        <li>{data.drivers[1]}</li>
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
        Points: {data.points} <br></br>
        Team: {data.points}
      </p>
    </div>
  )
}

export default function Teams() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getFullState().then(res => setData(res));
  }, []);

  // Tady je ten "kreslící" klid
  if (!data) return <div>Načítám...</div>;

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

  // Tady je ten "kreslící" klid
  if (!data) return <div>Načítám...</div>;
  return(
    <>
    <h1>Jezdci</h1>
    {data.drivers.map((driversData, index) => (
        <Team key={index} data={driversData} />
      ))}
    </>
  )
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Teams />
  </StrictMode>,
)