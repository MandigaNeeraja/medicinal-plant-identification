import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { setAccessToken } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function AuthCallback() {
  const navigate = useNavigate();
  const { refreshUser } = useAuth();

  useEffect(() => {
    const hash = window.location.hash.startsWith('#')
      ? window.location.hash.slice(1)
      : window.location.hash;
    const params = new URLSearchParams(hash);
    const accessToken = params.get('access_token');

    if (accessToken) {
      setAccessToken(accessToken);
      refreshUser().then(() => {
        toast.success('Signed in with Google');
        navigate('/dashboard', { replace: true });
      });
      return;
    }

    toast.error('Google sign-in failed');
    navigate('/login', { replace: true });
  }, [navigate, refreshUser]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="h-12 w-12 animate-spin rounded-full border-4 border-purple-500/30 border-t-purple-400" />
    </div>
  );
}
