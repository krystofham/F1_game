import React, { useEffect, useState } from 'react';
import { api } from '../utils/api';

export default function StatsPage() {
  const [records, setRecords] = useState([]);
  const [raceHistory, setRaceHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.getTrackRecords(), api.getBiggestLaps()])
      .then(([recordsData, historyData]) => {
        setRecords(recordsData);
        // Extracting all position 1 placements as the definitive victory record
        setRaceHistory(historyData.filter(item => item.position === "1"));
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load historical CSV statistics:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="loading">LOADING HISTORICAL DATA</div>;
  }

  if (records.length === 0 && raceHistory.length === 0) {
    return <div className="empty">NO RECORDED STATS FOUND IN CSV FILES</div>;
  }

  return (
    <div className="main-content">
      {/* Page Heading matching layout definitions */}
      <div className="page-header">
        <div className="page-eyebrow">Database Records</div>
        <h1 className="page-title">Game <span>Statistics</span></h1>
      </div>

      <div className="section-title">Absolute Track Records</div>
      <div className="card mb-6">
        <table className="data-table">
          <thead>
            <tr>
              <th>Circuit </th>
              <th>Driver</th>
              <th>Team</th>
              <th style={{ textAlign: 'right' }}>Lap Time</th>
              <th style={{ textAlign: 'center' }}>Season</th>
            </tr>
          </thead>
          <tbody>
            {records.map((row, index) => (
              <tr key={index}>
                <td style={{ fontWeight: '700' }}>{row.track}</td>
                <td>{row.driver}</td>
                <td className="text-muted">{row.team}</td>
                <td style={{ textAlign: 'right' }} className="text-yellow text-mono">
                  {parseFloat(row.lap_time).toFixed(4)}s
                </td>
                <td style={{ textAlign: 'center' }} className="text-mono">{row.season}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Section: Historical Grand Prix Winners */}
      <div className="section-title">Historical GP Winners</div>
      <div className="card">
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ textAlign: 'center' }}>Season</th>
              <th>Grand Prix Event</th>
              <th>Winner</th>
              <th>Team Name</th>
              <th>Weather</th>
              <th style={{ textAlign: 'right' }}>Total Time</th>
            </tr>
          </thead>
          <tbody>
            {raceHistory.map((row, index) => (
              <tr key={index}>
                <td style={{ textAlign: 'center' }} className="text-mono">{row.season}</td>
                <td style={{ fontWeight: '700' }}>{row.race}</td>
                <td className=" flex items-center gap-2">
                  {row.driver}
                </td>
                <td className="text-muted">{row.team}</td>
                <td className="text-mono" style={{ textTransform: 'uppercase' }}>{row.weather}</td>
                <td style={{ textAlign: 'right' }} className="text-mono">
                  {parseFloat(row.total_time).toFixed(3)}s
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}