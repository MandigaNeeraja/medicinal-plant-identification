import { useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const { user, register, loading, getErrorMessage } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (!loading && user) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    try {
      await register(name, email, password);
      toast.success('Account created successfully!');
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
        <h1 className="mb-2 text-3xl font-bold gradient-text">Create account</h1>
        <p className="mb-8 text-white/60">Join to explore AI-powered plant identification.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Full name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="input-field"
            required
          />
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
            placeholder="Password (min 8 characters)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
            minLength={8}
            required
          />
          <button type="submit" disabled={submitting} className="btn-primary w-full">
            {submitting ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <div className="my-6 flex items-center gap-3 text-sm text-white/40">
          <div className="h-px flex-1 bg-white/10" />
          or
          <div className="h-px flex-1 bg-white/10" />
        </div>

        <a href={`${import.meta.env.VITE_API_URL || ''}/api/auth/google/login`} className="btn-secondary w-full text-center">
          Continue with Google
        </a>

        <p className="mt-6 text-center text-sm text-white/60">
          Already have an account?{' '}
          <Link to="/login" className="text-cyan-300 hover:text-cyan-200">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
