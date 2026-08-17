import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import About from './pages/About';
import Chat from './pages/Chat';
import Dashboard from './pages/Dashboard';
import History from './pages/History';
import Identify from './pages/Identify';
import Login from './pages/Login';
import AuthCallback from './pages/AuthCallback';
import PlantDetail from './pages/PlantDetail';
import Profile from './pages/Profile';
import Register from './pages/Register';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Toaster position="top-right" />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/auth/callback" element={<AuthCallback />} />

          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/identify" element={<Identify />} />
              <Route path="/plant/:name" element={<PlantDetail />} />
              <Route path="/chat/:name" element={<Chat />} />
              <Route path="/history" element={<History />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/about" element={<About />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
