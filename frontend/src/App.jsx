import { useState, useEffect } from 'react'
import { 
  createBrowserRouter, 
  RouterProvider, 
  Outlet 
} from 'react-router-dom' // Změna importů
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

const RootLayout = () => (
  <>
    <Navbar />
    <div>
      <Outlet /> 
    </div>
  </>
);

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      {
        index: true, 
        element: <HeroSection isMobile={isMobile} />
      },
      {
        path: "teams",
        element: <Teams />
      },
      {
        path: "players",
        element: <Players />
      }
    ]
  }
]);
export default function App() {
  return <RouterProvider router={router} />;
}