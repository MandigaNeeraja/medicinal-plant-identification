export function getGoogleLoginUrl() {
  const base = import.meta.env.VITE_API_URL || window.location.origin;
  return `${base.replace(/\/$/, '')}/api/auth/google/login`;
}
