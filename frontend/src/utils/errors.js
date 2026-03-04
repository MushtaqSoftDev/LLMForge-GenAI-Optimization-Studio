/**
 * Map API/network errors to user-friendly messages (no raw status codes).
 * @param {Error} err - Axios error or network error
 * @param {string} fallback - Default message if nothing matches
 * @returns {string}
 */
export function getFriendlyAuthError(err, fallback = "Something went wrong. Please try again.") {
  if (!err) return fallback;

  const status = err.response?.status;
  const data = err.response?.data;
  const detail = data && typeof data === "object" ? data.detail : null;

  // Server sent a message we can show (avoid showing technical text)
  const safeDetail =
    typeof detail === "string" && !/^\d{3}\b|status code|error code/i.test(detail)
      ? detail
      : null;
  if (safeDetail) return safeDetail;

  // Validation errors (array of { msg, ... })
  if (Array.isArray(detail) && detail.length) {
    const msg = detail.map((e) => e.msg || e.message).filter(Boolean).join(" ");
    if (msg) return msg;
  }

  // Map status codes to friendly messages (no raw codes like 500, 502)
  const messages = {
    400: "Invalid request. Please check your details and try again.",
    401: "Invalid username or password.",
    403: "You don't have permission to do this.",
    404: "This service is not available. Please try again later.",
    409: "This username or email is already in use.",
    500: "Something went wrong. Please try again in a moment.",
    502: "The server is temporarily unavailable. Please try again in a minute.",
    503: "Service is busy or the database is unavailable. Please try again shortly.",
    504: "The request took too long. Please try again.",
  };

  if (status && messages[status]) return messages[status];
  if (err.code === "ERR_NETWORK" || err.message === "Network Error")
    return "Could not reach the server. Check your connection and try again.";

  return fallback;
}
