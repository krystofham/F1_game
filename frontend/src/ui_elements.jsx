import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import './ui_elements.css'

export function Navbar(isMobile) {
  return (
    <>
      {isMobile?< NavbarMobile />: <NavbarDesktop/>}
    </>
  )
}
export function NavbarDesktop() {
  return (
    <nav className="navbar">
      <a href="/" className="navbar-logo">
        <span>F1</span>game
      </a>
      <div className="navbar-links">
        <Link to="/teams">Teams</Link>
        <Link to="/players">Drivers</Link>
      </div>
    </nav>
  );
}

function NavbarMobile() {
  return (
    <nav className="navbar-mobile">
      <a href="/" className="navbar-logo">
        <span>F1</span>game
      </a>
      <div className="navbar-mobile-links">
        <Link to="/teams">Teams</Link>
        <Link to="/players">Drivers</Link>
      </div>
    </nav>
  );
}

function HeroSectionDesktop() {
  const features = [
    { title: 'Live Standings', desc: 'Real-time constructor & driver championship tables updated after every race.' },
    { title: 'Race Calendar', desc: 'Full season schedule with circuit details, session times, and countdowns.' },
    { title: 'Driver Profiles', desc: 'Career stats, lap records, and head-to-head comparisons for every driver.' },
    { title: 'Team Analysis', desc: 'Technical data, strategy breakdowns, and performance trends per constructor.' },
  ];

  return (
    <div className="hero hero-desktop">
      <div className="hero-slash" />

      <div className="hero-desktop-left hero-content">
        <span className="hero-eyebrow">Season 2025</span>

        <h1 className="hero-title">
          Where<br />
          Speed<br />
          <span className="hero-title-accent">Meets</span><br />
          Data.
        </h1>

        <p className="hero-subtitle">
          Your all-in-one hub for Formula 1 standings, driver stats,
          and team performance — from lights out to the podium.
        </p>

        <div className="hero-ctas">
          <Link to="/players" className="btn-primary">View Drivers</Link>
          <Link to="/" className="btn-ghost">Explore Teams</Link>
        </div>

        <div className="hero-stats">
          <div>
            <div className="stat-value">20</div>
            <div className="stat-label">Drivers</div>
          </div>
          <div>
            <div className="stat-value">10</div>
            <div className="stat-label">Teams</div>
          </div>
          <div>
            <div className="stat-value">24</div>
            <div className="stat-label">Races</div>
          </div>
        </div>
      </div>

      <div className="hero-desktop-right">
        <div className="hero-watermark">F1</div>
        <div className="hero-feature-grid">
          {features.map((f) => (
            <div key={f.title} className="hero-feature-card">
              <div className="feature-icon" aria-hidden="true" />
              <div className="feature-title">{f.title}</div>
              <div className="feature-desc">{f.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function HeroSectionMobile() {
  return (
    <div className="hero hero-mobile">

      <div className="hero-mobile-body hero-content">
        <div className="mobile-speed-bar" />

        <span className="hero-mobile-eyebrow">Season 2025</span>

        <h1 className="hero-mobile-title">
          Where<br />
          Speed<br />
          <span style={{ color: 'var(--red)' }}>Meets</span><br />
          Data.
        </h1>

        <p className="hero-mobile-subtitle">
          The best game in the universe
        </p>

        <div className="hero-mobile-ctas">
          <Link to="/players" className="btn-primary" style={{ textAlign: 'center' }}>
            View Drivers
          </Link>
          <Link to="/" className="btn-ghost" style={{ textAlign: 'center' }}>
            Explore Teams
          </Link>
        </div>

        <div className="hero-mobile-stats">
          <div>
            <div className="stat-value">20</div>
            <div className="stat-label">Drivers</div>
          </div>
          <div>
            <div className="stat-value">10</div>
            <div className="stat-label">Teams</div>
          </div>
          <div>
            <div className="stat-value">24</div>
            <div className="stat-label">Races</div>
          </div>
        </div>
      </div>
    </div>
  );
;}

export function HeroSection({ isMobile }) {
  return (
    <>
      {isMobile ? <HeroSectionMobile /> : <HeroSectionDesktop />}
    </>
  );
}