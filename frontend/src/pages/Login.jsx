import { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import api from '../api/client';
import GoogleSignInButton from '../components/GoogleSignInButton';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const { user, login, loading, getErrorMessage } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [googleEnabled, setGoogleEnabled] = useState(false);

  useEffect(() => {
    api.get('/auth/google/enabled')
      .then((res) => setGoogleEnabled(Boolean(res.data.data?.enabled)))
      .catch(() => setGoogleEnabled(false));
  }, []);

  if (!loading && user) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    try {
      await login(email, password);
      toast.success('Welcome back!');
      navigate('/dashboard');
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-10">
      <div className="card w-full max-w-md">
        <h1 className="mb-2 text-3xl font-bold gradient-text">Welcome back</h1>
        <p className="mb-8 text-white/60">Sign in to identify medicinal plants with AI.</p>

        <GoogleSignInButton disabled={!googleEnabled} />

        <div className="my-6 flex items-center gap-3 text-sm text-white/40">
          <div className="h-px flex-1 bg-white/10" />
          or sign in with email
          <div className="h-px flex-1 bg-white/10" />
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input-field"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
            required
          />
          <button type="submit" disabled={submitting} className="btn-primary w-full">
            {submitting ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        {!googleEnabled && (
          <p className="mt-4 text-center text-xs text-white/45">
            To enable Google sign-in, add credentials to `.env` — see `docs/GOOGLE_OAUTH_SETUP.md`
          </p>
        )}

        <p className="mt-6 text-center text-sm text-white/60">
          No account?{' '}
          <Link to="/register" className="text-cyan-300 hover:text-cyan-200">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
