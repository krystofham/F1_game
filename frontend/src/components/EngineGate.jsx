import { useCallback, useEffect, useState } from "react";
import { checkEngine } from "../utils/api";

const MAX_ATTEMPTS = 30;
const RETRY_MS = 1000;

export default function EngineGate({ children }) {
  const [status, setStatus] = useState("connecting");
  const [attempt, setAttempt] = useState(0);

  const probe = useCallback(async () => {
    setStatus("connecting");
    for (let i = 0; i < MAX_ATTEMPTS; i++) {
      setAttempt(i + 1);
      try {
        await checkEngine();
        setStatus("ready");
        return;
      } catch {
        await new Promise((r) => setTimeout(r, RETRY_MS));
      }
    }
    setStatus("failed");
  }, []);

  useEffect(() => {
    probe();
  }, [probe]);

  if (status === "ready") {
    return children;
  }

  return (
    <div className="engine-gate">
      <div className="engine-gate__panel">
        <div className="engine-gate__logo">MMRAC1NG</div>

        {status === "connecting" && (
          <>
            <div className="engine-gate__spinner" aria-hidden />
            <h1 className="engine-gate__title">Starting game engine</h1>
            <p className="engine-gate__hint">
              This usually takes a few seconds. Please wait…
            </p>
            <p className="engine-gate__meta">Attempt {attempt} of {MAX_ATTEMPTS}</p>
          </>
        )}

        {status === "failed" && (
          <>
            <h1 className="engine-gate__title engine-gate__title--error">
              Could not start the game engine
            </h1>
            <p className="engine-gate__hint">
              The app could not connect to the simulation server on your computer.
              Restart MMRAC1NG. If you installed from source, make sure Python and
              the engine dependencies are installed.
            </p>
            <button type="button" className="btn btn-primary" onClick={probe}>
              Try again
            </button>
          </>
        )}
      </div>
    </div>
  );
}
