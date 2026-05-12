import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import './index.css'
import { simLap, initRace, postRace, postChampionship } from './api_endpoints';
import { Team, Player, Teams, Players } from './players_teams'
import { Navbar, Herosection } from './ui_elements'

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



export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main>
        <div className='Herosection'>
          <Herosection isMobile={isMobile}/>
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