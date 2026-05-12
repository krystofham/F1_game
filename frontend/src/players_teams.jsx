function Team({ data }) {
  return (
    <div className="team-card">
      <h2>{data.name}</h2>
      <p><b>Position: {data.position}</b></p>
      <ul>
        {data.drivers.map((d, i) => <li key={i}>{d}</li>)}
      </ul>
      <p>Points: {data.points}</p>
    </div>
  )
}

function Player({ data }) {
  return (
    <div className='player-card'>
      <h2>{data.name}</h2>
      <p><b>Position: {data.position}</b></p>
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
  if (!data) return <div>Loading teams</div>;
  return (
    <>
      <h1>Teams</h1>
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
  if (!data) return <div>Loading drivers</div>;
  return (
    <>
      <h1>Drivers</h1>
      {data.drivers.map((driversData, index) => (
        <Player key={index} data={driversData} />
      ))}
    </>
  );
}
