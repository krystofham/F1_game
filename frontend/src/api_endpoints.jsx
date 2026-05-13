export const simLap = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/sim_lap", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    console.log("Odpověď:", data);
  } catch (error) {
    console.error("Chyba:", error);
  }
};

export const initRace = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/init_race", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    console.log("Odpověď:", data);
  } catch (error) {
    console.error("Chyba:", error);
  }
};

export const postRace = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/post_race", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    console.log("Odpověď:", data);
  } catch (error) {
    console.error("Chyba:", error);
  }
};

export const postChampionship = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/post_championship", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    console.log("Odpověď:", data);
  } catch (error) {
    console.error("Chyba:", error);
  }
};