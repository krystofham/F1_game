import { formatApiError } from "../utils/errors";

export default function ErrorMessage({ error, context, compact, action }) {
  if (!error) return null;

  const message = formatApiError(error, context);

  if (compact) {
    return (
      <div className="error-banner error-banner--compact">
        <span className="error-banner__icon" aria-hidden>⚠</span>
        <span className="error-banner__text">{message}</span>
        {action}
      </div>
    );
  }

  return (
    <div className="error-banner">
      <div className="error-banner__title">Something went wrong</div>
      <p className="error-banner__text">{message}</p>
      {action}
    </div>
  );
}
