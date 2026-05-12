import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import './index.css'
import { simLap, initRace, postRace, postChampionship } from './api_endpoints';
import { Team, Player, Teams, Players } from './players_teams'
const isMobile = window.matchMedia("(max-width: 768px)").matches;
async function getFullState() {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/get_state");
    return await response.json();
  } catch (err) {
    console.error("Server spí:", err);
    return null;
  }
}




export function Herosection() {
  if (!isMobile){
  return (
    <>
      <HeroSectionDesktop />
    </>
  );}
  else {
    return (
    <>
      <HeroSectionMobile />
    </>
    );
  }
}

export default function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Teams</Link> | <Link to="/players">Drivers</Link>
      </nav>
      <main>
        <div className='Herosection'>
          <Herosection />
        </div>
      </main>
      <div>
        <Routes>
          <Route path="/" element={<Teams />} />
          <Route path="/players" element={<Players />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}