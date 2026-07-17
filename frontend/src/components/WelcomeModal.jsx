import { useNavigate } from "react-router-dom";
import { needsWelcome } from "../utils/errors";

export default function WelcomeModal({ state, loading, dismissed, onDismiss }) {
  const navigate = useNavigate();

  if (dismissed || loading || !needsWelcome(state)) {
    return null;
  }

  const isFresh = !state?.drivers?.length;

  function goToRaceControl() {
    onDismiss();
    navigate("/race");
  }

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="welcome-title">
      <div className="modal-card">
        <div className="modal-card__eyebrow">Welcome to</div>
        <h2 id="welcome-title" className="modal-card__title">MMRAC1NG</h2>
        <p className="modal-card__body">
          {isFresh
            ? "You manage two drivers across a full season — tyre strategy, pit stops, and 26 AI rivals. Let's get your first race weekend ready."
            : "Your next race weekend is not set up yet. Head to Race Control to configure the weekend and start racing."}
        </p>

        <ol className="modal-steps">
          <li>Open <strong>Race Control</strong></li>
          <li>Set season length, training mode, and starting tyres</li>
          <li>Click <strong>INIT RACE</strong></li>
          <li>Each lap: choose pit strategy, confirm, then simulate</li>
        </ol>

        <div className="modal-card__actions">
          <button type="button" className="btn btn-primary" onClick={goToRaceControl}>
            Go to Race Control
          </button>
          <button type="button" className="btn" onClick={onDismiss}>
            I'll do it later
          </button>
        </div>
      </div>
    </div>
  );
}
