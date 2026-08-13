import { useCallback, useEffect, useRef, useState } from "react";
import { checkEngine } from "../utils/api";

const MAX_ATTEMPTS = 40;
const RETRY_MS = 500;

function isDesktopApp() {
  return typeof window !== "undefined" && window.desktopEnv?.isDesktop;
}

export default function EngineGate({ children }) {
  const [status, setStatus] = useState("connecting"); // connecting | ready | failed
  const [attempt, setAttempt] = useState(0);
  const [detail, setDetail] = useState("");
  const restartingRef = useRef(false);

  const waitForEngine = useCallback(async () => {
    for (let i = 0; i < MAX_ATTEMPTS; i++) {
      setAttempt(i + 1);
      try {
        await checkEngine();
        setStatus("ready");
        setDetail("");
        return true;
      } catch {
        await new Promise((r) => setTimeout(r, RETRY_MS));
      }
    }
    return false;
  }, []);

  const probe = useCallback(
    async ({ restart = false } = {}) => {
      setStatus("connecting");
      setAttempt(0);
      setDetail("");

      if (restart && isDesktopApp()) {
        restartingRef.current = true;
        try {
          const result = await window.desktopEnv.restartEngine();
          if (!result?.ok) {
            setDetail(result?.error || "The engine process could not be restarted.");
            setStatus("failed");
            return;
          }
          // i když main čekal na health, ještě jednou ověř z rendereru
          const ok = await waitForEngine();
          if (!ok) {
            setDetail("Engine restarted, but health check still failed.");
            setStatus("failed");
          }
        } finally {
          restartingRef.current = false;
        }
        return;
      }

      if (isDesktopApp() && window.desktopEnv.getEngineSpawnError) {
        const spawnError = await window.desktopEnv.getEngineSpawnError();
        if (spawnError) {
          setDetail(spawnError);
          setStatus("failed");
          return;
        }
      }

      const ok = await waitForEngine();
      if (!ok) {
        setStatus("failed");
        setDetail(
          (isDesktopApp() &&
            (await window.desktopEnv.getEngineSpawnError?.())) ||
            "The simulation server did not respond in time."
        );
      }
    },
    [waitForEngine]
  );

  useEffect(() => {
    probe();
  }, [probe]);

  useEffect(() => {
    if (!isDesktopApp() || !window.desktopEnv.onEngineStopped) return undefined;

    const unsubscribe = window.desktopEnv.onEngineStopped((reason) => {
      // při záměrném restartu ignoruj "stopped"
      if (restartingRef.current) return;

      const message =
        reason?.error ||
        (reason?.code != null ? `Engine exited (code ${reason.code}).` : "") ||
        (reason?.signal ? `Engine stopped (${reason.signal}).` : "") ||
        "The game engine stopped unexpectedly.";

      setDetail(message);
      setStatus("failed");
    });

    return unsubscribe;
  }, []);

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
            <p className="engine-gate__meta">
              Attempt {attempt} of {MAX_ATTEMPTS}
            </p>
          </>
        )}

        {status === "failed" && (
          <>
            <h1 className="engine-gate__title engine-gate__title--error">
              Could not start the game engine
            </h1>
            <p className="engine-gate__hint">
              {detail ||
                "The simulation server did not respond. Click Try again to restart it, or quit and reopen MMRAC1NG."}
            </p>

            {!isDesktopApp() && (
              <p className="engine-gate__hint engine-gate__hint--secondary">
                Running from source? Install Python dependencies (
                <code>pip install -r requirements.txt</code>) and make sure port
                8000 is free, or use <code>npm run desktop:dev</code> so the app
                starts the engine for you.
              </p>
            )}

            <button
              type="button"
              className="btn btn-primary"
              onClick={() => probe({ restart: isDesktopApp() })}
            >
              Try again
            </button>
          </>
        )}
      </div>
    </div>
  );
}
