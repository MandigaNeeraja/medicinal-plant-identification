import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const navItems = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/identify', label: 'Identify' },
  { to: '/history', label: 'History' },
  { to: '/about', label: 'About' },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen">
      <nav className="sticky top-0 z-50 border-b border-white/10 bg-black/70 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
          <Link to="/dashboard" className="text-lg font-bold gradient-text">
            Medicinal Plant Identifier
          </Link>

          <div className="hidden items-center gap-6 md:flex">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `text-sm font-medium transition ${isActive ? 'text-cyan-300' : 'text-white/70 hover:text-white'}`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <Link to="/profile" className="hidden text-sm text-white/80 hover:text-white sm:block">
              {user?.name}
            </Link>
            <button type="button" onClick={handleLogout} className="btn-secondary px-4 py-2 text-sm">
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        <Outlet />
      </main>
    </div>
  );
}
