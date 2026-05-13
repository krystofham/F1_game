import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import './index.css'
import { simLap, initRace, postRace, postChampionship } from './api_endpoints';
import { Team, Player, Teams, Players } from './players_teams'
import { Navbar, HeroSection } from './ui_elements'

const isMobile = window.matchMedia("(max-width: 768px)").matches;


export async function getFullState() {
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
      <div>
        <Routes>
          <Route path="/" element={<HeroSection isMobile={isMobile}/>} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/players" element={<Players />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}