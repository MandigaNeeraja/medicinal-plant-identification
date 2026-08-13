import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { useAuth } from '../context/AuthContext';

export default function Profile() {
  const { user, updateProfile, getErrorMessage } = useAuth();
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setName(user?.name || '');
  }, [user]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    try {
      await updateProfile({
        name,
        password: password || undefined,
      });
      setPassword('');
      toast.success('Profile updated');
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <section className="card">
        <h1 className="text-3xl font-bold gradient-text">Profile</h1>
        <p className="mt-2 text-white/70">Manage your account details.</p>
      </section>

      <section className="card">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-2 block text-sm text-white/70">Email</label>
            <input value={user?.email || ''} disabled className="input-field opacity-70" />
          </div>
          <div>
            <label className="mb-2 block text-sm text-white/70">Name</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input-field"
              required
            />
          </div>
          {user?.has_password && (
            <div>
              <label className="mb-2 block text-sm text-white/70">New password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field"
                placeholder="Leave blank to keep current password"
                minLength={8}
              />
            </div>
          )}
          <button type="submit" disabled={submitting} className="btn-primary">
            {submitting ? 'Saving...' : 'Save changes'}
          </button>
        </form>
      </section>
    </div>
  );
}
